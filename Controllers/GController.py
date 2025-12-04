from View.GView import GView
from Controllers.BController import BController
from Controllers.SController import SController
import tkinter as tk
from tkinter import messagebox

class GController:
    def __init__(self, gmodel):
        self.gmodel = gmodel

        self.barnc = BController(gmodel, self)
        self.shopc = SController(gmodel, self)

        self.gview = GView(self)
        self.images = {} 
        self.load_images()
        self.gmodel.controller = self

    def start(self):
        self.gview.start()

    def get_money(self):
        return self.gmodel.money

    def get_fertilizer(self):
        return self.gmodel.fertilizer

    def get_plot(self, plot_index):
        return self.gmodel.plots[plot_index]

    def open_shop(self):
        self.shopc.open_shop()

    def open_barn(self):
        self.barnc.open_barn()

    def open_plant_menu(self, plot_index):
        plant_menu = tk.Toplevel()
        plant_menu.title("Select Plant")
        self.gview.center(plant_menu, 300, 250)
        tk.Label(plant_menu, text="Select a plant to grow:").pack(pady=10)
        for plant in self.gmodel.plants:
            frame = tk.Frame(plant_menu)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{plant.name} - Growth time: {plant.base_time // 1000} seconds").pack(side="left", padx=5)
            price = self.gmodel.buy_prices[plant.id]
            plant_btn = tk.Button(frame, text=f"${price}", command=lambda p=plant: self.start_growing(plot_index, p, plant_menu))
            plant_btn.pack(side="right", padx=5)

    def _start_plot_loop(self, plot_index):
        plot = self.gmodel.plots[plot_index]

        if plot.remaining <= 0:
            plot.state = "ready"
            self.gview.update_plot(plot_index)
            return

        total_time = plot.plant.base_time
        done = total_time - plot.remaining
        stage = min(3, int(done / (total_time / 4)))

        img_key = f"{plot.plant.name}_{stage}"
        img = self.images.get(img_key)
        if img:
            self.gview.update_growing_plot(plot_index, img)

        plot.remaining -= 1000

        self.gview.root.after(1000, lambda: self._start_plot_loop(plot_index))

    def start_growing(self, plot_index, plant, menu_window):
        price = self.gmodel.buy_prices[plant.id]
        if self.gmodel.money >= price:
            self.gmodel.money -= price

            use_fertilizer = self.gmodel.fertilizer > 0
            if use_fertilizer:
                self.gmodel.fertilizer -= 1

            self.gmodel.start_thread(plant.id, plot_index, fertilizer_available=use_fertilizer)

            self.gview.update_money()
            self.gview.update_plot(plot_index)

            menu_window.destroy()

            self._start_plot_loop(plot_index)
        else:
            messagebox.showwarning("Not enough money", "You don't have enough money to buy this plant!")

    def on_plot_button_press(self, plot_index):
        plot = self.gmodel.plots[plot_index]

        if plot.state == "empty":
            self.open_plant_menu(plot_index)
        elif plot.state == "growing":
            from tkinter import messagebox
            messagebox.showinfo(
                "Plot Status",
                f"Plot {plot_index + 1} is still growing. Time left: {plot.remaining // 1000} seconds."
            )
        elif plot.state == "ready":
            plot_name = plot.plant.name 
            self.gmodel.harvest(plot_index)
            self.gview.update_plot(plot_index)
            from tkinter import messagebox

    def load_images(self):
        IMAGE_W, IMAGE_H = 150, 350
        plant_names = [plant.name for plant in self.gmodel.plants]
        stages = 4  
        for i in range(stages):
            for name in plant_names:
                img_path = f"img/{name}_{i}.png"
                try:
                    img = tk.PhotoImage(file=img_path)
                    self.images[f"{name}_{i}"] = img
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
        self.images["placeholder"] = tk.PhotoImage(width=IMAGE_W, height=IMAGE_H)

    def on_tick_update(self, plot_index):
        plot = self.get_plot(plot_index)

        total = plot.plant.base_time
        done = total - plot.remaining

        stage = min(3, int(done / (total / 4))) 

        img_key = f"{plot.plant.name}_{stage}"
        if img_key in self.images:
            self.gview.update_growing_plot(plot_index, self.images[img_key])

    def sell_plant(self, plant_name, price):
        self.shopc.sell_plant(plant_name, price)

    def buy_fertilizer(self, price):
        self.shopc.buy_fertilizer(price)

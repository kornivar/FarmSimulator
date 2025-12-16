from View.GView import GView
from Controllers.BController import BController
from Controllers.SController import SController
from Services.ResourceService import ResourceService
from Services.AutosaveService import AutosaveService
from DTO.PlotPurchaseDTO import PlotPurchaseDTO
from DTO.PlotMapper import PlotMapper

import tkinter as tk
from tkinter import messagebox

class GController:
    def __init__(self, gmodel):
        self.gmodel = gmodel

        self.barnc = BController(gmodel, self)
        self.shopc = SController(gmodel, self)

        self.autosave_service = AutosaveService(gmodel)

        self.gview = GView(self)
        self.gmodel.controller = self

        self.images = {} 
        self.load_images()  

        self.autosave_service.load_game()
        self.autosave()
        self.unlock_base_plots()
        

    def start(self):
        self.gview.start()

    def load_images(self):
        ResourceService.init()
        IMAGE_W, IMAGE_H = 150, 350
        plant_names = [plant.name for plant in self.gmodel.plants]
        stages = 4  
        for i in range(stages):         
            for name in plant_names:
                img_path = ResourceService.get_resource(f"{name}_{i}")
                try:
                    img = tk.PhotoImage(file=img_path)
                    self.images[f"{name}_{i}"] = img
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
        self.images["placeholder"] = tk.PhotoImage(width=IMAGE_W, height=IMAGE_H)

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

    def on_plot_button_press(self, plot_index):
        plot = self.gmodel.plots[plot_index]

        if plot.state == "locked":
            self.purchase_plot(plot_index)
        elif plot.state == "empty":
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
            plant_btn = tk.Button(frame, text=f"${price}", command=lambda p=plant: self.grow_init(plot_index, p, plant_menu))
            plant_btn.pack(side="right", padx=5)

    def on_tick_update(self, plot_index):
        plot = self.get_plot(plot_index)

        total = plot.plant.base_time
        done = total - plot.remaining

        stage = min(3, int(done / (total / 4))) 

        img_key = f"{plot.plant.name}_{stage}"
        if img_key in self.images:
            self.gview.update_growing_plot(plot_index, self.images[img_key])

    def purchase_plot(self, plot_index):
        answer = messagebox.askyesno("Unlock Plot", "Unlocking this plot costs $600.")
        if not answer:
            return
        else:
            plot_price = 600
            if self.gmodel.money >= plot_price:
                self.gmodel.money -= plot_price
                dto = PlotPurchaseDTO(has_upgrade=True, plot_type="upgrade")
                new_plot = PlotMapper.from_purchase(dto, plot_index)
                new_plot.unlock()
                self.gmodel.plots[plot_index] = new_plot
                self.gview.update_money()
                self.gview.update_plot(plot_index)
            else:
                messagebox.showwarning("Not enough money", "You don't have enough money to unlock this plot!")

    def unlock_base_plots(self):
        for i in range(3):
            plot = self.gmodel.plots[i]
            if plot.state == "locked":
                plot.state = "empty"

    def grow_init(self, plot_index, plant, menu_window):
        # Check for fertilizer charges on the upgraded plot
        fert_charges = self.gmodel.plots[plot_index].fertilizer_charges > 0
        use_fertilizer = False

        if fert_charges:
            messagebox.showinfo("Fertilizer Available", f"This plot has fertilizer charges available and will use them first. \
                \n{self.gmodel.plots[plot_index].fertilizer_charges} remaining")

        price = self.gmodel.buy_prices[plant.id]
        if self.gmodel.money >= price:
            self.gmodel.money -= price

            # Use fertilizer from plot charges first, then from global stock
            if not fert_charges:
                use_fertilizer = self.gmodel.fertilizer > 0
                if use_fertilizer:
                    self.gmodel.fertilizer -= 1

            self.gmodel.plot_init(plant.id, plot_index, fertilizer_available=use_fertilizer)

            self.gview.update_money()
            self.gview.update_plot(plot_index)

            menu_window.destroy()

            self.start_plot_loop(plot_index)
        else:
            messagebox.showwarning("Not enough money", "You don't have enough money to buy this plant!")

    def start_plot_loop(self, plot_index):
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

        self.gview.root.after(1000, lambda: self.start_plot_loop(plot_index))

    def sell_plant(self, plant_name, price):
        self.shopc.sell_plant(plant_name, price)

    def buy_fertilizer(self, price):
        self.shopc.buy_fertilizer(price)

    def resume_growth(self, plot):
        plot_index = self.gmodel.plots.index(plot)
        self.start_plot_loop(plot_index)

    def autosave(self):
        self.autosave_service.save_game()
        self.gview.root.after(1000, self.autosave)


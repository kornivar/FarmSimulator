import tkinter as tk
from tkinter import messagebox

class SController:
    def __init__(self, gmodel, main_controller):
        self.gmodel = gmodel
        self.main = main_controller
        self.view = None
        self.shop_labels = {}

    def open_shop(self):
        shop_window = tk.Toplevel()
        shop_window.title("Shop / Sell Plants")
        self.main.gview.center(shop_window, 300, 275)

        tk.Label(shop_window, text="Sell Your Plants or Buy Fertilizer").pack(pady=10)

        tk.Label(shop_window, text="Plants:").pack(pady=5)
        for plant in self.gmodel.plants:
            frame = tk.Frame(shop_window)
            frame.pack(pady=2)

            amount_in_barn = self.gmodel.barn.get(plant.name, 0)
            price = self.gmodel.sell_prices[plant.id]

            label = tk.Label(frame, text=f"{plant.name}: {amount_in_barn} - ${price} each")
            label.pack(side="left", padx=5)

            self.shop_labels[plant.name] = label
            sell_btn = tk.Button(frame, text="Sell 1", command=lambda n=plant.name, p=price: self.sell_plant(n, p))
            sell_btn.pack(side="right", padx=5)

        fert_frame = tk.Frame(shop_window)
        fert_frame.pack(pady=10)
        fertilizer_price = 5
        tk.Label(fert_frame, text=f"Fertilizer - ${fertilizer_price}").pack(side="left", padx=5)
        fert_btn = tk.Button(fert_frame, text="Buy Fertilizer", command=lambda: self.buy_fertilizer(fertilizer_price))
        fert_btn.pack(side="right", padx=5)

    def sell_plant(self, plant_name, price):
        if self.gmodel.barn.get(plant_name, 0) > 0:
            self.gmodel.barn[plant_name] -= 1
            self.gmodel.money += price

            self.main.gview.update_money()

            if plant_name in self.shop_labels:
                amount = self.gmodel.barn.get(plant_name, 0)
                label = self.shop_labels[plant_name]
                label.config(text=f"{plant_name}: {amount} - ${price} each")

            if self.gmodel.barn[plant_name] == 0:
                del self.gmodel.barn[plant_name]

        else:
            messagebox.showwarning("Cannot sell", f"You don't have any {plant_name} in barn!")

    def buy_fertilizer(self, price):
        if self.gmodel.money >= price:
            self.gmodel.money -= price
            self.gmodel.fertilizer += 1
            self.main.gview.update_money()
            return True
        else:
            messagebox.showwarning("Not enough money", "You don't have enough money!")
            return False





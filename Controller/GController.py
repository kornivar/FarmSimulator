from View.GView import GView
import tkinter as tk
from tkinter import messagebox

class GController:
    def __init__(self, gmodel):
        self.gmodel = gmodel
        self.gview = None

    def start(self):
        from View.GView import GView
        self.gview = GView(self)
        self.gview.start()

    def get_money(self):
        return self.gmodel.money

    def get_fertilizer(self):
        return self.gmodel.fertilizer

    def open_shop(self):
        shop_window = tk.Toplevel()
        shop_window.title("Shop / Sell Plants")
        shop_window.geometry("300x275")
        tk.Label(shop_window, text="Sell Your Plants or Buy Fertilizer").pack(pady=10)

        tk.Label(shop_window, text="Plants:").pack(pady=5)
        for plant in self.gmodel.plants:
            frame = tk.Frame(shop_window)
            frame.pack(pady=2)

            amount_in_barn = self.gmodel.barn.get(plant.name, 0)
            price = self.gmodel.sell_prices[plant.id]

            tk.Label(frame, text=f"{plant.name}: {amount_in_barn} - ${price} each").pack(side="left", padx=5)
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
            if self.gmodel.barn[plant_name] == 0:
                del self.gmodel.barn[plant_name]
            self.gview.update_money()
        else:
            messagebox.showwarning("Cannot sell", f"You don't have any {plant_name} in barn!")

    def buy_fertilizer(self, price):
        if self.gmodel.money >= price:
            self.gmodel.money -= price
            self.gmodel.fertilizer += 1
            self.gview.update_money()
        else:
            messagebox.showwarning("Not enough money", "You don't have enough money!")

    def open_barn(self):
        barn_window = tk.Toplevel()
        barn_window.title("Barn")
        barn_window.geometry("400x375")

        tk.Label(barn_window, text="Barn Contents").pack(pady=10)

        if not self.gmodel.barn:
            tk.Label(barn_window, text="Barn is empty").pack()
            return

        for name, amount in self.gmodel.barn.items():
            tk.Label(barn_window, text=f"{name}: {amount}").pack()





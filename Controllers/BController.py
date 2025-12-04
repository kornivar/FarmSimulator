import tkinter as tk

class BController:
    def __init__(self, gmodel, main_controller):
        self.gmodel = gmodel
        self.main = main_controller
        self.view = None

    def open_barn(self):
        barn_window = tk.Toplevel()
        barn_window.title("Barn")
        self.main.gview.center(barn_window, 400, 375)

        tk.Label(barn_window, text="Barn Contents").pack(pady=10)

        if not self.gmodel.barn:
            tk.Label(barn_window, text="Barn is empty").pack()
            return

        for name, amount in self.gmodel.barn.items():
            tk.Label(barn_window, text=f"{name}: {amount}").pack()





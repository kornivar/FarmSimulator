import tkinter as tk

class GView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Farm Simulator")
        self.window_width = 650
        self.window_height = 375
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Top frame with info
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", pady=10)

        self.fertilizer = self.controller.get_fertilizer()
        self.label_fertilizer = tk.Label(self.top_frame, text=f"Fertilizer left: {self.fertilizer}")
        self.label_fertilizer.pack(side="left", padx=20)

        self.money = self.controller.get_money()
        self.label_money = tk.Label(self.top_frame, text=f"Money left: {self.money}")
        self.label_money.pack(side="right", padx=20)

        # Center frame with plots
        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(expand=True, pady=20)

        self.plots = []
        for i in range(5):
            plot_frame = tk.Frame(self.center_frame)
            plot_frame.grid(row=0, column=i, padx=10)

            plant_label = tk.Label(plot_frame, text=f"Plot {i+1}", width=12, height=6, relief="ridge", bg="lightgreen")
            plant_label.pack()

            btn = tk.Button(plot_frame, text="Plant")
            btn.pack(pady=5)

            self.plots.append((plant_label, btn))

        # Lower frame with buttons
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.storage_button = tk.Button(self.bottom_frame, text="Storage")
        self.storage_button.pack(side="left", padx=20)

        self.shop_button = tk.Button(self.bottom_frame, text="Shop")
        self.shop_button.pack(side="right", padx=20)

    def start(self):
        self.root.mainloop()

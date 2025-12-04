import tkinter as tk


class GView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Farm Simulator")
        self.window_width = 400
        self.window_height = 375
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Top grid frame
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", pady=10)

        self.fertilizer = self.controller.get_fertilizer()
        self.label_fertilizer = tk.Label(self.top_frame, text=f"Fertilizer left: {self.fertilizer}")
        self.label_fertilizer.pack(side="left", padx=20)

        self.money = self.controller.get_money()
        self.label_money = tk.Label(self.top_frame, text=f"Money left: {self.money}")
        self.label_money.pack(side="right", padx=20)

        # Middle grid frame
        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(expand=True)  

        self.sub_frame = tk.Frame(self.center_frame)
        self.sub_frame.pack()

        for r in range(5):
            self.sub_frame.rowconfigure(r, weight=1)
            for c in range(5):
                self.sub_frame.columnconfigure(c, weight=1)
                btn = tk.Button(self.sub_frame, text=f"{r}:{c}", width=4, height=2)
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # Bottom grid frame
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.storage_button = tk.Button(self.bottom_frame, text="Storage")
        self.storage_button.pack(side="left", padx=20)

        self.shop_button = tk.Button(self.bottom_frame, text="Shop")
        self.shop_button.pack(side="right", padx=20)

    def start(self):
        self.root.mainloop()



import tkinter as tk

class GView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Farm Simulator")
        self.window_width = 1050
        self.window_height = 675
        self.button_plots = []
        
        self.center(self.root, self.window_width, self.window_height)

    def center(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_interface(self):
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

        IMAGE_W, IMAGE_H = 150, 350

        #Plots creation
        for i in range(5):
            plot_frame = tk.Frame(self.center_frame)
            plot_frame.grid(row=0, column=i, padx=10)

            image_holder = tk.Frame(plot_frame, width=IMAGE_W, height=IMAGE_H)
            image_holder.pack()
            image_holder.pack_propagate(False)  

            plant_label = tk.Label(image_holder, text="Locked", bg="gray",
                                   compound="center", wraplength=IMAGE_W-10)
            plant_label.pack(fill="both", expand=True)

            btn = tk.Button(plot_frame, text="Unlock", state="normal")
            btn.pack(pady=5)

            self.button_plots.append({
                "holder": image_holder,
                "label": plant_label,
                "button": btn,
            })

        for i, plot in enumerate(self.button_plots):
            plot["button"].config(command=lambda i=i: self.controller.on_plot_button_press(i))

        # Lower frame with buttons
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.storage_button = tk.Button(self.bottom_frame, text="Storage", command=self.controller.open_barn)
        self.storage_button.pack(side="left", padx=20)

        self.shop_button = tk.Button(self.bottom_frame, text="Shop", command = self.controller.open_shop)
        self.shop_button.pack(side="right", padx=20)

    def update_money(self):
        self.label_money.config(text=f"Money left: {self.controller.get_money()}")
        self.label_fertilizer.config(text=f"Fertilizer left: {self.controller.get_fertilizer()}")

    def update_plot(self, plot_index):
        plot = self.controller.get_plot(plot_index)
        ui = self.button_plots[plot_index]
        placeholder = self.controller.images.get("placeholder")

        if plot.state == "locked":
            ui["label"].config(image="", text="$600", bg="gray")
            ui["button"].config(text="Unlock", state="normal")
            return


        if plot.state == "empty":
            if placeholder:
                ui["label"].config(image=placeholder, text="", bg="lightgreen")
                ui["label"].image = placeholder
            else:
                ui["label"].config(image="", text=f"Plot {plot_index+1}", bg="lightgreen")
            ui["button"].config(text="Plant", state="normal")
            return

        plant = plot.plant.name

        if plot.state == "growing":
            ui["button"].config(text="Growing...", state="disabled")
            img = self.controller.images.get(f"{plant}_0")
            if img:
                ui["label"].config(image=img, text="", bg=self.root["bg"])  
                ui["label"].image = img
            return

        if plot.state == "ready":
            img = self.controller.images.get(f"{plant}_3")
            if img:
                ui["label"].config(image=img, text="", bg=self.root["bg"])  
                ui["label"].image = img
            ui["button"].config(text="Harvest", state="normal")

    def update_growing_plot(self, plot_index, img):
        ui = self.button_plots[plot_index]
        ui["label"].config(image=img, text="", bg=self.root["bg"])
        ui["label"].image = img

    def start(self):
        self.create_interface()

        # Initial plot updates(locked/empty)
        for i in range(5):
            self.update_plot(i)

        # Resume growth on growing plots
        for plot in self.controller.gmodel.plots:
            if plot.state == "growing" and plot.remaining > 0:
                self.controller.resume_growth(plot)

        self.root.mainloop()

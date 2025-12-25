import logging
logger = logging.getLogger(__name__)
from View.GView import GView
from Controllers.BController import BController
from Controllers.SController import SController
from Controllers.MissionController import MissionController
from Services.ResourceService import ResourceService
from Services.AutosaveService import AutosaveService
from DTO.PlotPurchaseDTO import PlotPurchaseDTO
from DTO.PlotMapper import PlotMapper

import tkinter as tk
from tkinter import messagebox

class GController:
    def __init__(self, gmodel):
        self.gmodel = gmodel
        logger.info("Initializing Game Controller...")

        self.barnc = BController(gmodel, self)
        self.shopc = SController(gmodel, self)
        self.missionc = MissionController(gmodel)

        self.autosave_service = AutosaveService(gmodel)

        self.gview = GView(self)
        self.gmodel.controller = self

        # track achievements window for live refresh
        self.achievements_window = None

        self.images = {} 
        self.load_images()  

        self.autosave_service.load_game()
        self.autosave()
        self.unlock_base_plots()
        try:
            self.missionc.update_missions()
        except Exception:
            pass
        logger.info("Game Controller initialized.")
        

    def start(self):
        logger.info("Starting Game View...")
        self.gview.start()

    def load_images(self):
        logger.info("Loading plant images...")
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
                    logger.info(f"Loaded image: {img_path}")
                except Exception as e:
                    logger.error(f"Error loading image {img_path}: {e}")

        self.images["placeholder"] = tk.PhotoImage(width=IMAGE_W, height=IMAGE_H)
        logger.info("Plant images loaded.")

    def get_money(self):
        logger.info("Getting current money...")
        return self.gmodel.money

    def get_fertilizer(self):
        logger.info("Getting current fertilizer...")
        return self.gmodel.fertilizer

    def get_plot(self, plot_index):
        logger.info(f"Getting plot at index {plot_index}...")
        return self.gmodel.plots[plot_index]

    def open_shop(self):
        logger.info("Opening shop...")
        self.shopc.open_shop()

    def open_barn(self):
        logger.info("Opening barn...")
        self.barnc.open_barn()

    def on_plot_button_press(self, plot_index):
        logger.info(f"Plot button pressed for plot index {plot_index}...")
        try:
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
                self.missionc.on_plant_collected(plot_name)
                # update missions state and refresh UI
                try:
                    self.missionc.update_missions()
                except Exception:
                    pass
                self.gview.update_plot(plot_index)
                self.gview.update_money()
                self.refresh_achievements_if_open()
                from tkinter import messagebox
        except Exception as e:
            logger.error(f"Error handling plot button press: {e}")

    def open_plant_menu(self, plot_index):
        logger.info(f"Opening plant selection menu for plot index {plot_index}...")
        try:
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
        except Exception as e:
            logger.error(f"Error opening plant menu: {e}")

    def open_achievements(self):
        logger.info("Opening achievements...")
        try:
            # ensure missions are up to date before building UI
            try:
                self.missionc.update_missions()
            except Exception:
                pass
            # If achievements window already exists, destroy it to refresh
            try:
                if self.achievements_window is not None and self.achievements_window.winfo_exists():
                    self.achievements_window.destroy()
            except Exception:
                pass

            window = tk.Toplevel(self.gview.root)
            self.achievements_window = window
            window.title("Achievements")
            self.gview.center(window, 500, 400)

            container = tk.Frame(window)
            container.pack(fill="both", expand=True, padx=10, pady=10)

            for mission in self.gmodel.missions.values():
                self._create_mission_row(container, mission)
        except Exception as e:
            logger.error(f"Error opening achievements: {e}")

    def refresh_achievements_if_open(self):
        try:
            if self.achievements_window is not None and self.achievements_window.winfo_exists():
                self.open_achievements()
        except Exception:
            pass

    def _create_mission_row(self, parent, mission):
        bg_color = "#b6fcb6" if mission.completed else "#f0f0f0"

        frame = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
        frame.pack(fill="x", pady=5)

        text_frame = tk.Frame(frame, bg=bg_color)
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            text_frame,
            text=mission.name,
            font=("Arial", 12, "bold"),
            bg=bg_color
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=mission.description,
            bg=bg_color,
            wraplength=300,
            justify="left"
        ).pack(anchor="w")

        reward_btn = tk.Button(
            frame,
            text=f"Get reward ({mission.reward_gold}$)"
        )
        # configure command after creation to avoid referencing before assignment
        reward_btn.config(command=lambda m=mission, b=reward_btn: self._claim_mission_reward(m, b))

        if mission.completed and not mission.reward_given:
            reward_btn.config(state="normal")
        else:
            reward_btn.config(state="disabled")

        reward_btn.pack(side="right", padx=10, pady=10)

    def _claim_mission_reward(self, mission, button):
        try:
            claimed = self.missionc.claim_reward(mission)
            if claimed:
                self.gview.update_money()
                button.config(state="disabled")
        except Exception as e:
            logger.error(f"Error claiming mission reward: {e}")
     
    def on_tick_update(self, plot_index):
        logger.info(f"Tick update for plot index {plot_index}...")
        try:
            plot = self.get_plot(plot_index)

            total = plot.plant.base_time
            done = total - plot.remaining

            stage = min(3, int(done / (total / 4))) 

            img_key = f"{plot.plant.name}_{stage}"
            if img_key in self.images:
                self.gview.update_growing_plot(plot_index, self.images[img_key])
        except Exception as e:
            logger.error(f"Error during tick update: {e}")

    def purchase_plot(self, plot_index):
        logger.info(f"Purchasing plot at index {plot_index}...")
        answer = messagebox.askyesno("Unlock Plot", "Unlocking this plot costs $600.")
        if not answer:
            return
        else:
            plot_price = 600
            if self.gmodel.money >= plot_price:
                try:
                    self.gmodel.money -= plot_price
                    dto = PlotPurchaseDTO(has_upgrade=True, plot_type="upgrade")
                    new_plot = PlotMapper.from_purchase(dto, plot_index)
                    new_plot.unlock()
                    self.gmodel.plots[plot_index] = new_plot
                    self.gview.update_money()
                    self.gview.update_plot(plot_index)
                    self.missionc.on_plot_unlocked()
                    try:
                        self.missionc.update_missions()
                    except Exception:
                        pass
                    self.refresh_achievements_if_open()
                except Exception as e:
                    logger.error(f"Error purchasing plot: {e}")
            else:
                messagebox.showwarning("Not enough money", "You don't have enough money to unlock this plot!")

    def unlock_base_plots(self):
        logger.info("Unlocking base plots...")
        try:
            for i in range(3):
                plot = self.gmodel.plots[i]
                if plot.state == "locked":
                    plot.state = "empty"
        except Exception as e:
            logger.error(f"Error unlocking base plots: {e}")

    def grow_init(self, plot_index, plant, menu_window):
        # Check for fertilizer charges on the upgraded plot
        logger.info(f"Initializing growth of {plant.name} on plot index {plot_index}...")

        fert_charges = self.gmodel.plots[plot_index].fertilizer_charges > 0
        use_fertilizer = False

        if fert_charges:
            messagebox.showinfo("Fertilizer Available", f"This plot has fertilizer charges available and will use them first. \
                \n{self.gmodel.plots[plot_index].fertilizer_charges} remaining")

        try:
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
        except Exception as e:
            logger.error(f"Error initializing growth: {e}")

    def start_plot_loop(self, plot_index):
        logger.info(f"Starting growth loop for plot index {plot_index}...")
        plot = self.gmodel.plots[plot_index]

        if plot.remaining <= 0:
            plot.state = "ready"
            self.gview.update_plot(plot_index)
            return

        total_time = plot.plant.base_time
        done = total_time - plot.remaining
        stage = min(3, int(done / (total_time / 4)))

        try:
            img_key = f"{plot.plant.name}_{stage}"
            img = self.images.get(img_key)
            if img:
                self.gview.update_growing_plot(plot_index, img)
        except Exception as e:
            logger.error(f"Error updating growing plot image: {e}")

        plot.remaining -= 1000

        self.gview.root.after(1000, lambda: self.start_plot_loop(plot_index))

    def sell_plant(self, plant_name, price):
        logger.info(f"Selling plant {plant_name} for price {price}...")
        self.shopc.sell_plant(plant_name, price)

    def buy_fertilizer(self, price):
        logger.info(f"Buying fertilizer for price {price}...")
        is_able = self.shopc.buy_fertilizer(price)
        if is_able:
            self.missionc.on_fertilizer_bought()
            try:
                self.missionc.update_missions()
            except Exception:
                pass
            self.gview.update_money()
            self.refresh_achievements_if_open()

    def resume_growth(self, plot):
        logger.info(f"Resuming growth for plot {plot}")
        plot_index = self.gmodel.plots.index(plot)
        self.start_plot_loop(plot_index)

    def autosave(self):
        logger.info("Autosaving game...")
        self.autosave_service.save_game()
        self.gview.root.after(1000, self.autosave)


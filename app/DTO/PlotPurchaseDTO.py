class PlotPurchaseDTO:
    def __init__(self, plot_type: str, has_upgrade: bool):
        self.plot_type = plot_type
        self.has_upgrade = has_upgrade
from View.GView import GView
from Model.GModel import GModel

class GController:
    def __init__(self):
        self.gview = GView(self)
        self.gmodel = GModel()

    def start(self):
        self.gview.start()

    def get_money(self):
        return self.gmodel.money

    def get_fertilizer(self):
        return self.gmodel.fertilizer




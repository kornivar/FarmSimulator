from View.GView import GView

class GController:
    def __init__(self, gmodel):
        self.gmodel = gmodel
        self.gview = GView(self)

    def start(self):
        self.gview.start()

    def get_money(self):
        return self.gmodel.money

    def get_fertilizer(self):
        return self.gmodel.fertilizer




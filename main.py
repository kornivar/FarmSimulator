from Controllers.GController import GController
from Models.GModel import GModel

gmodel = GModel()
gcontroller  = GController(gmodel)
gcontroller.start()

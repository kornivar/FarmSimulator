from Controllers.GController import GController
from Models.GModel import GModel
from Services.LogService import LogService

LogService.init()

gmodel = GModel()
gcontroller  = GController(gmodel)
gcontroller.start()

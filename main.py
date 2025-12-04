from Controllers.GController import GController
from Models.GModel import GModel

model = GModel()
console = GController(model)
console.start()
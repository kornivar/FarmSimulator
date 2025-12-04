from Controller.GController import GController
from Model.GModel import GModel

model = GModel()
console = GController(model)
console.start()
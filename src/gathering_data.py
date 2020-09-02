from modicar import Car
import modi

car = Car()
bundle = modi.MODI()
mot = bundle.motors[0]
dial = bundle.dials[0]
btn = bundle.buttons[0]

print("press button to start")
while True:
    if btn.toggled:
        car.run(mot, dial.degree)
    else:
        mot.speed = 0,0
from modicar import Car
import modi
import time

car = Car()
bundle = modi.MODI()
mot = bundle.motors[0]
dial = bundle.dials[0]
ir1 = bundle.irs[0]
ir2 = bundle.irs[1]
btn = bundle.buttons[0]

mot.speed = 100,-100
time.sleep(0.5)
mot.speed = 0,0

car.collect_data(mot, ir1, ir2, btn, dial)

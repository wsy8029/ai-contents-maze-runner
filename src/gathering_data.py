import modi
from IPython.display import clear_output
import time

bundle = modi.MODI()
mot = bundle.motors[0]
dial = bundle.dials[0]

base_speed = -20, 20

while True:
    mot.speed = base_speed
    degree = (dial.degree - 50) // 1
    print(degree)

    if degree <= 0:
        mod_speed = base_speed[0], (base_speed[1] + abs(degree))
        mot.speed = mod_speed
        print(mod_speed)
    else:
        mod_speed = (base_speed[0] - abs(degree)), base_speed[1]
        mot.speed = mod_speed
        print(mod_speed)

    clear_output(wait=True)
    # time.sleep(0.001)
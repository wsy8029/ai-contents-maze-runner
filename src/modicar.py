

class Car(object):
    def __init__(self):
        self.base_speed = -20, 20
        pass

    def run(self, mot, degree_original):
        mot.speed = self.base_speed
        degree = (degree_original - 50)//1
        print(degree)

        if degree <= 0:
            mod_speed = self.base_speed[0], (self.base_speed[1] + abs(degree))
            mot.speed = mod_speed
            print(mod_speed)
        else:
            mod_speed = (self.base_speed[0] - abs(degree)), self.base_speed[1]
            mot.speed = mod_speed
            print(mod_speed)


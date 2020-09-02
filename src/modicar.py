import time
import pandas as pd

class Car(object):
    def __init__(self):
        self.base_speed = -25, 25
        self.data = []
        

    def run(self, mot, ir1, ir2, degree_original):
        
        
        mot.speed = self.base_speed
        degree = ((degree_original - 50)*1.5)//1
        print(degree)
        self.data.append([ir1.proximity, ir2.proximity, degree_original])

        if degree <= 0:
            mod_speed = self.base_speed[0], (self.base_speed[1] + abs(degree))
            mot.speed = mod_speed
            print(mod_speed)
        else:
            mod_speed = (self.base_speed[0] - abs(degree)), self.base_speed[1]
            mot.speed = mod_speed
            print(mod_speed)
            
    def save(self):
        df = pd.DataFrame(self.data, columns=['ir1', 'ir2', 'degree']) 
        self.path = '../data/data.csv'
        df.to_csv(self.path, sep=',')
        

import time
import pandas as pd
from IPython.display import clear_output
import os
import tensorflow as tf
from train import Model
import modi

class Car(object):
    def __init__(self, bundle):
        self.bundle = bundle
        self.mot = self.bundle.motors[0]
        self.ir1 = self.bundle.irs[0]
        self.ir2 = self.bundle.irs[1]
        self.degree = 3
        
        self.base_speed = -25, 25
#         self.data = []
        self.m = None
        
    def collect_data(self):
        dial = self.bundle.dials[0]
        btn = self.bundle.buttons[0]
        
        self.shake()
        print("데이터를 수집하려면 버튼을 한번 누르세요")
        
        while True:
            if btn.clicked:
                print("수집을 시작합니다. 다이얼을 움직여 조종하세요")
                time.sleep(1)
                while True:
                    time.sleep(0.01)
                    if btn.clicked:
                        print("수집을 중지합니다. 수집을 마치려면 버튼을 두번 클릭하세요.")
                        self.stop()
                        time.sleep(1)
                        break
                    else:
                        dg = dial.degree
                        if dg <= 20:
                            self.left_fast()
                            self.degree = 1
                        elif dg > 20 and dg <= 40:
                            self.left_slow()
                            self.degree = 2
                        elif dg > 40 and dg <= 60:
                            self.straight()
                            self.degree = 3
                        elif dg > 60 and dg <= 80:
                            self.right_slow()
                            self.degree = 4
                        elif dg > 80:
                            self.right_fast()
                            self.degree = 5
                        
                        ir_L = self.ir1.proximity
                        ir_R = self.ir2.proximity
                        tmp = []
                        tmp.append([ir_L, ir_R, self.degree])
                        df = pd.DataFrame(tmp, columns=['ir_L', 'ir_R', 'degree'])
                        df.to_csv('/home/pi/workspace/ai-contents-maze-runner/data/data_new.csv', index=False, mode='a', header=False)

            elif btn.double_clicked:
                print("데이터 수집을 종료합니다.")
                break
        
        
    def run(self, mot, degree_original):
        
        
        mot.speed = self.base_speed
        degree = ((degree_original - 50)*1.5)//1
#         ir_L = ir1.proximity
#         ir_R = ir2.proximity
#         print(f"[각도] {degree}\n[ir_왼쪽] {ir_L} [ir_오른쪽] {ir_R} \n[속도] ", end='\r')
#         self.data.append([ir_L, ir_R, degree_original])

        if degree <= 0:
            mod_speed = self.base_speed[0], (self.base_speed[1] + abs(degree))
            mot.speed = mod_speed
            print("[속도] ", mod_speed)
        else:
            mod_speed = (self.base_speed[0] - abs(degree)), self.base_speed[1]
            mot.speed = mod_speed
            print("[속도] ", mod_speed)
            
        clear_output(wait=True)
            
    def save(self):
        df = pd.DataFrame(self.data, columns=['ir_L', 'ir_R', 'degree']) 
        self.path = '/home/pi/workspace/ai-contents-maze-runner/data/data.csv'
        if not os.path.exists(self.path):
            df.to_csv(self.path, index=False, mode='a')
        else:
            df.to_csv(self.path, index=False, mode='a', header=False)
        #df.to_csv(self.path, sep=',')
        time.sleep(3)
        
    def collect_datas(self, mot, ir1, ir2, btn, dial):
        while True:
            # exit data collect loop
            if btn.double_clicked:
                clear_output(wait=True)
#                 self.save()
                print("데이터 수집을 종료합니다.")
#                 time.sleep(3)
                break
                
            print("데이터 수집을 시작하려면 버튼을 한번 클릭하세요. ", 
                  "데이터를 수집을 종료하려면 버튼을 더블클릭하세요.", end='\r')
            time.sleep(0.2)
            
            if btn.clicked:
                clear_output(wait=True)
                print("데이터 수집을 시작합니다.")
                print('ready')
                time.sleep(0.3)
                print('3')
                time.sleep(0.3)
                print('2')
                time.sleep(0.3)
                print('1')
                time.sleep(0.3)
                print('start!')
                clear_output(wait=True)
                
                while True:
                    degree_original = dial.degree
                    self.run(mot, degree_original)
                    ir_L = ir1.proximity
                    ir_R = ir2.proximity
                    tmp = []
                    tmp.append([ir_L, ir_R, degree_original])
                    df = pd.DataFrame(tmp, columns=['ir_L', 'ir_R', 'degree'])
                    df.to_csv('/home/pi/workspace/ai-contents-maze-runner/data/data.csv', index=False, mode='a', header=False)
#                     with open('/home/pi/workspace/ai-contents-maze-runner/data/data.csv','a') as fd:
#                         tmp = []
#                         tmp.append([ir1, ir2, degree_original])
#                         fd.write(tmp)
                    
                    if btn.clicked:
                        mot.speed = 0,0
                        print("데이터 수집이 중지되었습니다.")
                        break
            clear_output(wait=True)
            
    def learn(self):
        self.m = Model("/home/pi/workspace/ai-contents-maze-runner/data/data.csv")
        self.m.feature_engineering()
        self.m.set_data()
        self.m.train()
        
    def start(self, mot, ir1, ir2):
        model = tf.keras.models.load_model('/home/pi/workspace/ai-contents-maze-runner/model/model.h5')
        while True:
            ir_L = ir1.proximity
            ir_R = ir2.proximity
            if ir_L == 0:
                ir_L = 0.01
            if ir_R == 0:
                ir_R = 0.01
            
            ir_RL = ir_R - ir_L
            ir_LR = ir_L / ir_R
            data = [ir_L, ir_R, ir_RL, ir_LR]

            degree = model.predict([[data]])[0][0]
            data1 = []
            data1.append([ir_L, ir_R, degree])
            df = pd.DataFrame(data1, columns=['ir_L', 'ir_R', 'degree'])
            df.to_csv('/home/pi/workspace/ai-contents-maze-runner/data/data_inference.csv', index=False, mode='a', header=False)

            if degree > 30:
                degree += 5
            else:
                degree -= 5
                
            if degree >= 100:
                degree = 100
            if degree <= 0:
                degree = 0
            print(degree)
            self.run(mot, degree)
            
            
    def straight(self):
        self.mot.speed = -25,25
    
    def left_slow(self):
        self.mot.speed = -25,70
    
    def left_fast(self):
        self.mot.speed = -25,100
    
    def right_slow(self):
        self.mot.speed = -70,25
        
    def right_fast(self):
        self.mot.speed = -100,25
    
    def stop(self):
        self.mot.speed = 0,0
        
    def shake(self):
        self.left_fast()
        time.sleep(0.2)
        self.right_fast()
        time.sleep(0.2)
        self.stop()
        
        
            
            

def main():
    
    bundle = modi.MODI()
    car = Car()

    mot = bundle.motors[0]
    ir1 = bundle.irs[0]
    ir2 = bundle.irs[1]
    
    car.start(mot, ir1, ir2)


if __name__ == "__main__":
    main()   
            
                        
                
        

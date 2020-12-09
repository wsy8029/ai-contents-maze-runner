import time
import pandas as pd
from IPython.display import clear_output
import os
import tensorflow as tf
from train import Model
import modi
from datetime import datetime
import numpy as np
import joblib

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
                        tmp.append([ir_L, ir_R, self.degree, datetime.now().time()])
                        df = pd.DataFrame(tmp, columns=['ir_L', 'ir_R', 'degree', 'time'])
                        df.to_csv('/home/pi/workspace/ai-contents-maze-runner/data/data_new4.csv', index=False, mode='a', header=False)

            elif btn.double_clicked:
                print("데이터 수집을 종료합니다.")
                break
        
        
    def run(self):
        model = Model()
        model.train()
         
        # pickled binary file 형태로 저장된 객체를 로딩한다 
        file_name = '/home/pi/workspace/ai-contents-maze-runner/model/rf.pkl' 
        rfmodel = joblib.load(file_name) 
        
        while True:
            time.sleep(0.01)
            ir1 = self.ir1.proximity
            ir2 = self.ir2.proximity
            if ir2 == 0:
                pass
            else:
                pred = rfmodel.predict([[ir1, ir2, ir1-ir2, ir1/ir2]])
                print("예측값 : ",pred)

                if pred[0] == 1:
                    self.left_fast()
                elif pred[0] == 2:
                    self.left_slow()
                elif pred[0] == 3:
                    self.straight()
                elif pred[0] == 4:
                    self.right_slow()
                elif pred[0] == 5:
                    self.right_fast()
                
    
            
            
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
    



if __name__ == "__main__":
    main()   
            
                        
                
        

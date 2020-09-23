import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

class Model(object):
    def __init__(self,csv):
        
        

    def train(self):
        df = pd.read_csv("../data/data_new1.csv")
        df['ir_1-2'] = df['ir1'] - df['ir2']
        df['ir_1/2'] = df['ir1'] / df['ir2']

        df = df[df !=0]
        df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(axis=0)

        df = df.loc[:, ['ir1', 'ir2', 'degree', 'ir_1-2', 'ir_1/2']]
        
        
        # Original Data
        df_inputs = df.loc[:,['ir1', 'ir2', 'ir_1-2', 'ir_1/2']]
        df_outputs = df.loc[:,['degree']]

        # Normalized Data
        # df_inputs = df_n.loc[:,['ir_L', 'ir_R']]
        # df_outputs = df_n.loc[:,['degree']]
        # df_inputs = df_n.loc[:,['ir_L', 'ir_R', 'ir_1-2', 'ir_1/2']]
        # df_outputs = df_n.loc[:,['degree']]

        inputs = np.array(df_inputs)
        outputs = np.array(df_outputs)
        
        
        num_data = len(inputs)
        TRAIN_SPLIT = int(0.6 * num_data)
        TEST_SPLIT = int(0.2 * num_data + TRAIN_SPLIT)
        inputs_train, inputs_test, inputs_validate = np.split(inputs, [TRAIN_SPLIT, TEST_SPLIT])
        outputs_train, outputs_test, outputs_validate = np.split(outputs, [TRAIN_SPLIT, TEST_SPLIT])
        
        rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
        rf.fit(inputs_train, outputs_train)
        
        
         
        # 객체를 pickled binary file 형태로 저장한다 
        file_name = '/home/pi/workspace/ai-contents-maze-runner/model/rf.pkl' 
        joblib.dump(rf, file_name)
        
  
        
def main():
    
    pass

    


if __name__ == "__main__":
    main()        
        
        
        
        

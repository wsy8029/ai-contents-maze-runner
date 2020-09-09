import numpy as np
import pandas as pd
import tensorflow as tf

class Model(object):
    def __init__(self,csv):
        self.df = pd.read_csv(csv)
        self.inputs_train = []
        self.inputs_test = []
        self.innputs_validate = []
        self.outputs_train = []
        self.outputs_test = []
        self.outputs_validate = []
        self.model = None
        self.outputs_predict = []
        self.model_path='/home/pi/workspace/ai-contents-maze-runner/model/model.h5'
        
    
    def set_data(self):
        print("[Split dataset for training..]")
        df_inputs = self.df.loc[:,['ir_L', 'ir_R', 'ir_R-L', 'ir_L/R']]
        df_outputs = self.df.loc[:,['degree']]
        
        
        inputs = np.array(df_inputs)
        outputs = np.array(df_outputs)

        num_data = len(inputs)
        TRAIN_SPLIT = int(0.6 * num_data)
        TEST_SPLIT = int(0.2 * num_data + TRAIN_SPLIT)

        self.inputs_train, self.inputs_test, self.inputs_validate = np.split(inputs, [TRAIN_SPLIT, TEST_SPLIT])
        self.outputs_train, self.outputs_test, self.outputs_validate = np.split(outputs, [TRAIN_SPLIT, TEST_SPLIT])
        
    def train(self):
        print("[Start Training..]")
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.Input(shape = self.inputs_train.shape[1]))
        self.model.add(tf.keras.layers.Dense(50, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(rate=.2))
        # self.model.add(tf.keras.layers.Dense(10, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(rate=.2))

        self.model.add(tf.keras.layers.Dense(1, activation='relu'))



        # self.model.compile(optimizer='adam', loss='mae', metrics=['mae']) # mse / mae
        self.model.compile(optimizer='adam', loss='mse', metrics=['mse']) # mse / mae
        self.model.summary()
        
        history = self.model.fit(self.inputs_train, self.outputs_train, epochs=1, batch_size=1, 
                                 validation_data=(self.inputs_validate, self.outputs_validate))
        
        self.outputs_predict = self.model.predict(self.inputs_test)
        
        self.model.save(self.model_path)
        print("model saved at ", self.model_path)
        
        
    def feature_engineering(self):
        print("[Feature Engineering..]")
        # Extract motor speed from dial degree
        def chdeg(degree_original):
            degree = ((degree_original - 50)*1.5)//1
            if degree <= 0:
                left = 25
                right = 25 + abs(degree)
            else:
                left = 25 - abs(degree)
                right = 25
            return left, right

        left = []
        right = []
        for i in range(len(self.df)):
            left.append(chdeg(self.df['degree'][i])[0])
            right.append(chdeg(self.df['degree'][i])[1])

        self.df['mot_L'] = left
        self.df['mot_R'] = right
        
        # Add Feature difference and ratio of mot_L and mot_R
        self.df['ir_R-L'] = self.df['ir_R'] - self.df['ir_L']
        self.df['ir_L/R'] = self.df['ir_L'] / self.df['ir_R']
        
def main():
    
    m = Model("../data/data.csv")
    m.feature_engineering()
    m.set_data()
    m.train()

    


if __name__ == "__main__":
    main()        
        
        
        
        

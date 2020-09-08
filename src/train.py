import numpy as np
import tensorflow as tf

class Model(object):
    def __init__(self):
        self.inputs_train = []
        self.inputs_test = []
        self.innputs_validate = []
        self.outputs_train = []
        self.outputs_test = []
        self.outputs_validate = []
        self.model = None
        self.outputs_predict = []
    
    def set_data(self, df):
        df_inputs = df.loc[:,['ir_L', 'ir_R', 'ir_R-L', 'ir_L/R']]
        df_outputs = df.loc[:,['degree']]
        
        
        inputs = np.array(df_inputs)
        outputs = np.array(df_outputs)

        num_data = len(inputs)
        TRAIN_SPLIT = int(0.6 * num_data)
        TEST_SPLIT = int(0.2 * num_data + TRAIN_SPLIT)

        self.inputs_train, self.inputs_test, self.inputs_validate = np.split(inputs, [TRAIN_SPLIT, TEST_SPLIT])
        self.outputs_train, self.outputs_test, self.outputs_validate = np.split(outputs, [TRAIN_SPLIT, TEST_SPLIT])
        
    def train(self):
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.Input(shape = inputs_train.shape[1]))
        self.model.add(tf.keras.layers.Dense(50, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(rate=.2))
        # self.model.add(tf.keras.layers.Dense(10, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(rate=.2))

        self.model.add(tf.keras.layers.Dense(1, activation='relu'))



        # self.model.compile(optimizer='adam', loss='mae', metrics=['mae']) # mse / mae
        self.model.compile(optimizer='adam', loss='mse', metrics=['mse']) # mse / mae
        self.model.summary()
        
        history = self.model.fit(inputs_train, outputs_train, epochs=1, batch_size=1, 
                                 validation_data=(inputs_validate, outputs_validate))
        
        self.outputs_predict = self.model.predict(self.inputs_test)
        
        
        

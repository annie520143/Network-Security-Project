import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

#import the training data
def load_data(file):
    #file = "../dataset/NUSW_mix.csv"
    dataset_raw = pd.read_csv(file, low_memory=False)

    return dataset_raw


def seperate(dataset):
    
    #處理缺失值
    dataset.fillna(value=0, inplace=True)
    #dataset.isnull().sum() -> see NULL in key

    key_len = dataset.shape[1] #how many features
    feature_name = dataset.keys().tolist()
    feature_name.remove('Label')
    
    dataset_temp, label = dataset.iloc[:, : key_len-1].values,  dataset.iloc[:,  key_len-1].values
    dataset_train, dataset_test, label_tr, label_ts = train_test_split(dataset_temp, label, test_size=0.25, random_state=2)  # 隨機選25趴當測試，剩下當訓練
    #print(dataset_train.dtype)
    np.random.shuffle(dataset_train)
    np.random.shuffle(dataset_test)
    dataset_train = pd.DataFrame(dataset_train, columns=feature_name)
    dataset_test = pd.DataFrame(dataset_test, columns=feature_name)
    """ label_tr = pd.DataFrame(label_tr, columns = ['Label'])
    label_ts = pd.DataFrame(label_ts, columns = ['Label']) """
    
    return dataset_train, dataset_test, label_tr, label_ts









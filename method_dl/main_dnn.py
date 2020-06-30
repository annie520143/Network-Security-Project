import numpy as np
import pandas as pd
import sys

"""
callback function
"""
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping

"""
preprocessing
"""
import preprocessing as prep
"""
Keras Method
"""
from keras.models import Sequential
import method_dnn as dnn 
#import temp_iptable as iptable

normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    packets = prep.proto_to_value(packets)    
    #packets = prep.state_to_value(packets)   
    del packets['state'] 
    packets = prep.service_to_value(packets)
    #packets, srcip = prep.ip_to_value(packets)
    
    packets, label, attack_cat = prep.seperate_attcat_lab(packets)

    #if we want to do get specfic
    packets = prep.get_imp(packets)
    
    return packets, label, attack_cat

#create np array for label
def label_to_nparr(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0])
        elif(label_list[i] == 1):
            label_np.append([0, 1])
        
    return label_np

#create np array for label
def attackcat_to_nparr(label_list):

    label_np = []
    for i in range(label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1,0,0,0,0,0,0,0,0,0])
        elif(label_list[i] == 1):
            label_np.append([0,1,0,0,0,0,0,0,0,0])
        elif(label_list[i] == 2):
            label_np.append([0,0,1,0,0,0,0,0,0,0])
        elif(label_list[i] == 3):
            label_np.append([0,0,0,1,0,0,0,0,0,0])
        elif(label_list[i] == 4):
            label_np.append([0,0,0,0,1,0,0,0,0,0])
        elif(label_list[i] == 5):
            label_np.append([0,0,0,0,0,1,0,0,0,0])
        elif(label_list[i] == 6):
            label_np.append([0,0,0,0,0,0,1,0,0,0])
        elif(label_list[i] == 7):
            label_np.append([0,0,0,0,0,0,0,1,0,0])
        elif(label_list[i] == 8):
            label_np.append([0,0,0,0,0,0,0,0,1,0])
        elif(label_list[i] == 9):
            label_np.append([0,0,0,0,0,0,0,0,0,1])

    label_np = np.array(label_np)

    return label_np

def processed_data(datapath):
    data_df = pd.read_csv(datapath, low_memory=False)

    data_df, label_list, attcat_list = init(data_df)
    #print("1 ", type(data_srcip))

    #transforming datatype
    data_df_transtype = prep.trans_datatype(data_df)
    #print("2 ", type(data_df))

    #scaling (data type changes after scaling, i.e. df -> np)
    data_df_scale = prep.feature_scaling(data_df_transtype)
    #print("3 ", type(data_df))

    #create an one-hot list for label list
    datalabel_list_oneHot = label_to_nparr(label_list)
    attcat_list_oneHot = attackcat_to_nparr(attcat_list)

    #turn dataframe and list to np array
    label_np, attcat_np, data_np = np.array(datalabel_list_oneHot), np.array(attcat_list_oneHot), np.array(data_df_scale)
    
    #deal with problem of key 'ct_ftp_cmd'
    data_np = prep.np_fillna(data_np)

    return data_np, label_np, label_list, attcat_np, attcat_list

    

if __name__ == "__main__":
    train_path = "../dataset/2_0w4_1w4_yshf_notime.csv"
    test_path = "../dataset/1_10-18_mix_time.csv"

    train_np, trainlabel_np, trainlabel_list, trainattcat_np, trainattcat_list = processed_data(train_path)
    test_np, testlabel_np, testlabel_list, testattcat_np, testattcat_list, = processed_data(test_path)
    #print(len(train_attackcat[0]))
    print('train attack_np: ', trainattcat_np)
    print('train attack_list: ', trainattcat_list)

    """ pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(train_df.head()) """

    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np.shape[1] # how mant features

    # simpleDNN(feature_dim, units, atv, loss)
    #model = dnn.simpleDNN(feature_dim, 15, 'relu', 'mse')


    # simpleDNN_dropout(feature_dim, units, atv, loss)
    model = dnn.simpleDNN_dropout(feature_dim, 15, 'relu', 'mse')

    # Setting callback functions
    csv_logger = CSVLogger('training.log')

    checkpoint = ModelCheckpoint(filepath='dnn_best.h5',
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=6,
                                verbose=1,
                                mode='max')

    #training
    model.fit(train_np, trainattcat_np, batch_size=100, epochs=10, callbacks=[
            earlystopping, checkpoint, csv_logger], shuffle=True)
    #model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, shuffle=True)

    result = model.evaluate(train_np,  trainattcat_np)
    print("testing accuracy = ", result[1])

    #testing_predict(model, testlabel_list, test_srcip) 

    predictLabel = model.predict_classes(train_np)
    np.set_printoptions(threshold=sys.maxsize)
    #print(predictLabel)
    dnn.detailAccuracyDNN(predictLabel, trainattcat_list)
    #bad_index_list = dnn.detailAccuracyDNN(predictLabel, testattcat_list)
    #print(bad_index_list)

    """ result = model.evaluate(test_np,  testattcat_np)
    print("testing accuracy = ", result[1])

    #testing_predict(model, testlabel_list, test_srcip) 

    predictLabel = model.predict_classes(test_np)
    np.set_printoptions(threshold=sys.maxsize)
    #print(predictLabel)
    dnn.detailAccuracyDNN(predictLabel, testattcat_list)
    #bad_index_list = dnn.detailAccuracyDNN(predictLabel, testattcat_list)
    #print(bad_index_list) """


    """
    bad_srcip_list, temp = [], []
    for index in bad_index_list:
        srcip = test_srcip[index]

        if temp.count(srcip) == 0:
            if test_srcip.count(srcip) >= 50:
                temp.append(srcip)
                bad_srcip_list.append(srcip)
        elif temp.count(srcip) != 0:
            print("exist before")
            #have been counted, do nothing

    print(bad_srcip_list) """

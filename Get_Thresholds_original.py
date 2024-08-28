import numpy as np
from matplotlib import pyplot as plt 
import os
import json
import datetime
import requests

#D:\Get_Thresholds_original.py

def extract_PID_data(data, PROTOCOL,LABEL):
    
    if (PROTOCOL == 'SAE'):

        if LABEL == 'IMAP':
            PID_TAG = '106'
        elif LABEL == 'ENGINE LOAD':
            PID_TAG = '92'
        elif LABEL == 'OIL PRESSURE':
            PID_TAG = '100'
        elif LABEL == 'ENGINE RPM':
            PID_TAG = '190'
        elif LABEL == 'FUEL RATE':
            PID_TAG = '183'
        elif LABEL == 'MAF':
            PID_TAG = '132'
        elif LABEL == 'BOOST':
            PID_TAG = '102'
        elif LABEL == 'BAROMETER':
            PID_TAG = '108'
        elif LABEL == 'THROTTLE':
            PID_TAG = '91'
        elif LABEL == 'ATGMF': # Eaxuast Gas Flow Rate
            PID_TAG = '3236'
        elif LABEL == 'DPFDP': # DPF Diffrential Pressure (across DPF)
            #PID_TAG = '7ABC'#'3251'
            PID_TAG = '3251'
        elif LABEL == 'SCRT':   # SCR Catalyst Temperature Before Catalyst (DPF out)
            PID_TAG = '4360'
        elif LABEL == 'SPEED': # Wheep based Vehicle Speed
            PID_TAG = '84'
        elif LABEL == 'DPFINT':# DPF in Temperature Before DPF (DOC out)
            #PID_TAG = '4766' #4766 #3250
            PID_TAG = '3250' #4766 #3250
            #PID_TAG = '7CBC' #4766 #3250
        elif LABEL == 'IS': #  regen inhibited
            PID_TAG = '3703'        
        elif LABEL == 'FUEL USE': #  Total fuel used (high precision)
            PID_TAG = '5054'        
        elif LABEL == 'DISTANCE': #  Total distance travelled (high precision)
            PID_TAG = '917' # 245
        elif LABEL == 'SOOTLOAD':
            PID_TAG = '5466' # 245 #3719 generic check       
        elif LABEL == 'ACTIVEREGEN':
            PID_TAG = '3700' # 245

    elif(PROTOCOL == 'SAE_AVG'):

        if LABEL == 'ENGINE LOAD':
            PID_TAG = 'dff_92_avg'
        elif LABEL == 'ENGINE RPM':
            PID_TAG = 'dff_190_avg'
        elif LABEL == 'THROTTLE':
            PID_TAG = 'dff_91_avg'
        elif LABEL == 'ATGMF': # Eaxuast Gas Flow Rate
            PID_TAG = 'dff_3236_avg'
        elif LABEL == 'DPFDP': # DPF Diffrential Pressure (across DPF)
            PID_TAG = 'dff_3251_avg'
        elif LABEL == 'SPEED': # Wheep based Vehicle Speed
            PID_TAG = 'dff_84_avg'
        elif LABEL == 'DPFINT':# DPF in Temperature Before DPF (DOC out)
            PID_TAG = 'dff_3250_avg' #'dff_3250_avg #4766
            #PID_TAG = 'dff_4766_avg' #'dff_3250_avg #4766
        elif LABEL == 'IS': #  regen inhibited
            PID_TAG = '3703'        
        elif LABEL == 'SOOTLOAD':
            PID_TAG = '5466' #  #3719 generic check 
        elif LABEL == 'ACTIVEREGEN':
            PID_TAG = '3700' # 245

    elif(PROTOCOL == 'SAE_AVG_SPN'):

        if LABEL == 'ENGINE LOAD':
            PID_TAG = 'spn_92_avg'
        elif LABEL == 'ENGINE RPM':
            PID_TAG = 'spn_190_avg'
        elif LABEL == 'THROTTLE':
            PID_TAG = 'spn_91_avg'
        elif LABEL == 'ATGMF': # Eaxuast Gas Flow Rate
            PID_TAG = 'spn_3236_avg'
        elif LABEL == 'DPFDP': # DPF Diffrential Pressure (across DPF)
            PID_TAG = 'spn_3251_avg'
        elif LABEL == 'SPEED': # Wheep based Vehicle Speed
            PID_TAG = 'spn_84_avg'
        elif LABEL == 'DPFINT':# DPF in Temperature Before DPF (DOC out)
            PID_TAG = 'spn_3250_avg' #'dff_3250_avg #4766
            #PID_TAG = 'spn_4766_avg' #'dff_3250_avg #4766
        elif LABEL == 'IS': #  regen inhibited
            PID_TAG = 'spn_3703_avg'        
        elif LABEL == 'SOOTLOAD':
            PID_TAG = 'spn_5466_avg' #  #3719 generic check 5466
        elif LABEL == 'ACTIVEREGEN':
            PID_TAG = 'spn_3700_avg' # 245
            #PID_TAG = '3700' # 245

    elif(PROTOCOL == 'ISO'):

        if LABEL == 'IMAP':
            PID_TAG = '87BC'#MODIFY the "if PID_TAG in State1:" loop (append for loop on top)  
        elif LABEL == 'ENGINE LOAD':
            PID_TAG = '04'
        elif LABEL == 'ENGINE RPM':
            PID_TAG = '0C'
        elif LABEL == 'FUEL RATE':
            PID_TAG = '5E'
        elif LABEL == 'MAF':
            PID_TAG = '10'
        elif LABEL == 'BOOST':
            PID_TAG = '102'
        elif LABEL == 'BAROMETER':
            PID_TAG = '33'
        elif LABEL == 'THROTTLE':
            PID_TAG = '11'#MODIFY the "if PID_TAG in State1:" loop (append for loop on top)
        elif LABEL == 'DPFDP': # DPF Diffrential Pressure (across DPF)
            PID_TAG = '7A'

    #print(LABEL)
    print("PID TAG is-->" + LABEL + " ," +PROTOCOL,"Mapping is --->", PID_TAG)

    Time_vec = []
    Val_vec = []
    #print(len(data[0]))
    #print(len(data))
    for data_cnt in range(0,len(data[0])):
        if "pids" in data[0][data_cnt]:
            if len(data[0][data_cnt]['pids'])>0:
                for sub_pid_cnt in range(0,len(data[0][data_cnt]['pids'])):  #this loop
                    State = data[0][data_cnt]['pids'][sub_pid_cnt]
                    #print(State)
                    #print(data_cnt)
                    #for state_cnt in range(0,len(State)):
                    if PID_TAG in State:
                        #print("--------------------------------------------IN----------------------------------")
                        Time_vec.append(np.array(State[PID_TAG]['timestamp'], dtype=np.int64))
                        Val_vec.append(np.array(State[PID_TAG]['value'], dtype=float))

    print("Number of time stamp avilables are--->",len(Val_vec))

    
    return Time_vec,Val_vec

if __name__ == '__main__':

    #dir_list = os.listdir('D:/Work/Timeseries_models/DATA/NB/DATA/')
    dir_list = ['1311448262007324672']
    PROTOCOL = 'SAE_AVG'

    for file in dir_list:
        print("Viechle ID-------", file)
        #OBD_data_path = 'D:/Work/Timeseries_models/DATA/NB/AdamTools/' + file
        #OBD_data_path = 'D:/Work/Timeseries_models/DATA/TH_DATA/Mahindra/T/' + file
        #OBD_data_path = 'D:/Work/FRP/DATA/FOTA/EBT/Freightliner Cascadia - DD13/' + file
        # OBD_data_path = "D:/products/Fuel_Rail_Pressure/temp/1720569600000_1296957128686174208_1723334340000.json"
        # print(OBD_data_path)
        # OBD_data = [json.loads(line) for line in open(OBD_data_path, 'r')]
        vehicle_id = '1311448262007324672'
        Start_TS =   1722384000000
        End_TS = 1722643140000
        country_FLAG = 'US'

        if country_FLAG == 'US':
            OBD_data_path = 'https://old-data-downloader.intangles-aws-us-east-1.intangles.us/download/' + str(vehicle_id) +  "/" + str(Start_TS) + "/" + str(End_TS)
        elif country_FLAG == 'IN':
            OBD_data_path = 'http://data-download.intangles.com:1883/download/' + str(vehicle_id) +  "/" + str(Start_TS) + "/" + str(End_TS) 
        r = requests.get(OBD_data_path, stream=True)
        OBD_data = r.json()    


        LABEL = 'DPFDP'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)
        print(np.array(X_Time[0:5]))
        print(np.array(X_Time[0]))
        print(np.array(X_Time[-1]))

        print("Mean of DP----------------->",np.mean(X_Value))
        print("95th percentile of DP----------------->",np.percentile(X_Value, 95))
        # Mean to 90th Percentile is divided in 4 DP thresholds

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        #fig, ax1 = plt.subplots()
        #ax1.plot(TS,X_Value,'.')
        #ax1.axhline(y=10, xmin=0, xmax=len(X_Value), color='g',linestyle='--')
        #ax1.axhline(y=20, xmin=0, xmax=len(X_Value), color='y',linestyle='--')
        #ax1.axhline(y=30, xmin=0, xmax=len(X_Value), color='r',linestyle='--')
        #ax1.set_ylabel('Differential Pressure across DPF (Kpa)')
        #ax1.set_xlabel('Time Stamp')
        #ax1.grid()
        #plt.show()
        #exit(0)

        plt.subplot(8, 1, 1)
        plt.plot(TS,X_Value,'.b')
        #plt.plot(X_Time[2950:3650],X_Value[2950:3650],'.b')
        plt.axhline(y=7, xmin=0, xmax=len(X_Value), color='r',linestyle='--')
        plt.title(LABEL)


        LABEL = 'DPFINT'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)


        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        #fig, ax2 = plt.subplots()
        #ax2.plot(TS,X_Value,'.')
        #ax2.axhline(y=500, xmin=0, xmax=len(X_Value), color='r',linestyle='--')
        #ax2.axhline(y=400, xmin=0, xmax=len(X_Value), color='y',linestyle='--')
        #ax2.axhline(y=350, xmin=0, xmax=len(X_Value), color='g',linestyle='--')
        #plt.title(LABEL)
        #plt.show()
        #exit(0)

        plt.subplot(8, 1, 2)
        plt.plot(TS,X_Value,'.b')
        #plt.plot(X_Time[2950:3650],X_Value[2950:3650],'.b')
        #plt.ylim((0, 600)) 
        plt.axhline(y=500, xmin=0, xmax=len(X_Value), color='r',linestyle='--')
        plt.title(LABEL)


        LABEL = 'ENGINE RPM'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        
        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        print("5th percentile of RPM----------------->",np.percentile(X_Value, 5))
        print("90th percentile of RPM----------------->",np.percentile(X_Value, 90))
        #print(np.array(X_Time[813:816])) #1187552386416115712
        #print(np.array(X_Time[3698:3719])) # 1187552386416115712
        plt.subplot(8, 1, 3)
        plt.plot(TS,X_Value,'.b')
        plt.title(LABEL)

 
        LABEL = 'ENGINE LOAD'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        print("Mean of ENGINE LOAD----------------->",np.mean(X_Value))
        plt.subplot(8, 1, 4)
        plt.plot(TS,X_Value,'.b')
        plt.title(LABEL)

        LABEL = 'SPEED'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        plt.subplot(8, 1, 5)
        plt.plot(TS,X_Value,'.b')
        plt.title(LABEL)
  

        LABEL = 'SOOTLOAD'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)

        plt.subplot(8, 1, 6)
        plt.plot(TS,X_Value,'b')
        plt.title(LABEL)

        #SL = np.array(X_Value[1:-1]) - np.array(X_Value[0:-2])
        #plt.subplot(8, 1, 7)
        #plt.plot(np.array(TS[1:-1]),SL)
        
        

        LABEL = 'ACTIVEREGEN'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)
            
        plt.subplot(8, 1, 7)
        plt.plot(TS,X_Value,'.b')
        plt.title(LABEL)
        #plt.show()
        #exit(0)


        LABEL = 'IS'
        X_Time, X_Value = extract_PID_data(OBD_data,PROTOCOL,LABEL)

        TS = []
        for cnt in range(0,len(X_Time)):
            TEMP = datetime.datetime.fromtimestamp((X_Time[cnt] + 19800*1000) / 1000.0, tz=datetime.timezone.utc)
            TS.append(TEMP)
            
        plt.subplot(8, 1, 8)
        plt.plot(TS,X_Value,'.b')
        plt.title(LABEL)

        #plt.tight_layout()

        plt.show()
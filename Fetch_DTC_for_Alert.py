import requests 
import csv
import json
import pandas as pd
from datetime import datetime, timezone
import os
from pathlib import Path





# for US vehicles set the url as "http://algo-internal-apis.intangles-aws-us-east-1.intangles.us:1234/dashboard_apis/fetch"
# for Indian vehicles set the url as "http://internal-apis.intangles.com/dashboard_apis/fetch"

url =  "https://algo-internal-apis.intangles-aws-us-east-1.intangles.us/dashboard_apis/fetch/"

# enter the output path where you want the output to be written
output_path = "D:/Work/FRP/CODE/"


def fetch_dtc_data(Veichle_ID, start_ts, end_ts):
    
    df_all_dtcs = pd.DataFrame()
    start_batch_time = start_ts 
    end_batch_time = start_batch_time + 24*1*60*60*1000 

    
    while end_batch_time <= end_ts:
        print("starting timestamp ", start_batch_time) 
        print("ending timestamp ", end_batch_time)
        headers = {
                'Content-Type': 'application/json',
            }
        vehicle_dtc_data = {"report": "default",
            "filter":[
                {
                    "fault_log.timestamp":{
                        "gt": start_batch_time,
                        "lt": end_batch_time
                    }
                },
                {
                'vehicle.id': Veichle_ID
                }

            ],
            "select":{
                "fault_log.status":{
                    "value":True,
                    "as":"status"
                },
                "fault_log.code":{
                    "value":True,
                    "as":"code"
                },
                "fault_code.severity":{
                    "value":True,
                    "as":"severity"
                },
                "vehicle.id":{
                    "value":True,
                    "as":"vehicle_id"
                },
                "fault_log.vehicle_id":{
                    "value":True,
                    "as":"vehicle_id1"
                },
                "vehicle.account_id": {
                    "value": True,
                    "as": "account_id"
                },
                "vehicle.tag":{
                    "value":True,
                    "as":"vehicle_plate"
                },
                "fault_log.timestamp":{
                    "value":True,
                    "as":"time"
                },
                "spec.manufacturer":{
                    "value":True,
                    "as":"manufacturer"
                },
                "spec.max_load_capacity":{
                    "value":True,
                    "as": "max_load_capacity"
                },
                "fault_code.description":{
                    "value":True,
                    "as":"description"
                }
            }
            }
   
        dtc_response = requests.post(url, json=vehicle_dtc_data, headers=headers)
        print(dtc_response)
        dtc_csv_filename = 'dtc.csv'
        if dtc_response.status_code == 200:
            # Parse the JSON response
            dtc_json_data = dtc_response.json()
            dtc_headers = dtc_json_data['result']['fields']
            with open(dtc_csv_filename, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=dtc_headers)
                
                # Write headers to the CSV file
                csv_writer.writeheader()
                
                # Write each JSON item as a row in the CSV file
                csv_writer.writerows(dtc_json_data['result']['output'])
        else:
            print(f"Failed to fetch the dtc data. Status code: {dtc_response.status_code}")
        df_dtc = pd.read_csv(dtc_csv_filename, encoding='unicode_escape') 

        start_batch_time += 24*1*60*60*1000 
        end_batch_time = start_batch_time + 24*1*60*60*1000

        df_all_dtcs= pd.concat([df_all_dtcs, df_dtc], ignore_index=True)

    return df_all_dtcs



def miliseconds_to_utc(time_ms):
    time_seconds = time_ms / 1000.0
    # Create a UTC datetime object
    trip_time_utc = datetime.utcfromtimestamp(time_seconds).replace(tzinfo=timezone.utc)
    formatted_trip_time_utc = trip_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return formatted_trip_time_utc

def alert_matching(Next_five_hr_DTC, DTC_LIST):

    match_flag = False
    #for dtc_cnt in range(0,len(DTC_LIST)):
    for fetch_dtc_cnt in range(0,len(Next_five_hr_DTC)):
        if Next_five_hr_DTC[fetch_dtc_cnt] in DTC_LIST:
            match_flag = True
    return match_flag


def utc_to_miliseconds(utc_date_string):
    # Parse the UTC date string into a datetime object
    utc_datetime = datetime.strptime(utc_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Convert seconds to milliseconds
    milliseconds = int(utc_datetime.timestamp() * 1000)

    return milliseconds

def ist_to_miliseconds(utc_date_string):
    # Parse the UTC date string into a datetime object
    #utc_datetime = datetime.strptime(utc_date_string, '%Y-%m-%d %H:%M:%S+00')
    utc_datetime = datetime.strptime(utc_date_string, '%Y-%m-%d %H:%M:%S%z')
    # Convert seconds to milliseconds
    milliseconds = int(utc_datetime.timestamp() * 1000)

    return milliseconds


#2024-08-14 13:19:56+00

# enter the start time and end time between which you want the dtc

#AID_DTC_LIST = ['523000-2','DB040E']
AID_DTC_LIST = ['P0402', 'P0401']
ECT_DTC_LIST =  ['523000-2','DB040E']
DPF_DTC_LIST = ['P2003', 'P244B']
BAT_DTC_LIST = ['P2003', 'P244B']
FUEL_TRIM_DTC_LIST = ['523000-2','DB040E']


df_alert = pd.read_csv("C:/Users/Bhushan.Patil/Downloads/UPS_Predictive_Alert.csv", dtype={'vehicle_id':'int64'})
df_alert['time_miliseconds'] = df_alert['timestamp'].apply(ist_to_miliseconds)

print(df_alert)


# Alert_ts =  1722418630354
# end_ts =    Alert_ts + 432000000

# Veichle_ID = '1259309728429768704'
# df_dtc = fetch_dtc_data(Veichle_ID, Alert_ts, end_ts)
# df_dtc = df_dtc.drop_duplicates(keep='first')
# df_dtc['time_miliseconds'] = df_dtc['time'].apply(utc_to_miliseconds)

# df_dtc = df_dtc.drop_duplicates()

# Next_five_hr_DTC = df_dtc["code"]

# print("this is the next five hours dtc ", Next_five_hr_DTC)
# print("this is the AID dtc list ", AID_DTC_LIST)


#ALERT-matching for AID

for i in arnge(df_alert.shape[0]):
    Alert_ts =  df_alert.iloc[i,'timestamp_ms']
    end_ts =    Alert_ts + 432000000
    Veichle_ID = str(df_alert.iloc[i,'vehicle_id'])
    df_dtc = fetch_dtc_data(Veichle_ID, Alert_ts, end_ts)
    df_dtc = df_dtc.drop_duplicates(keep='first')
    df_dtc['time_miliseconds'] = df_dtc['time'].apply(utc_to_miliseconds)
    df_dtc = df_dtc.drop_duplicates()
    Next_five_hr_DTC = df_dtc["code"]
    print(Next_five_hr_DTC)
    if df_alert.iloc[i, 'algo_name'] == 'bat':
        MATCH_FLAG = alert_matching(Next_five_hr_DTC,BAT_DTC_LIST)
        df_alert.iloc[i, 'true/false_dtc'] = MATCH_FLAG
    elif  df_alert.iloc[i, 'algo_name'] == 'aid':
        MATCH_FLAG = alert_matching(Next_five_hr_DTC,AID_DTC_LIST)
        df_alert.iloc[i, 'true/false_dtc'] = MATCH_FLAG
    elif  df_alert.iloc[i, 'algo_name'] == 'ect':
        MATCH_FLAG = alert_matching(Next_five_hr_DTC,ECT_DTC_LIST)
        df_alert.iloc[i, 'true/false_dtc'] = MATCH_FLAG 
    elif  df_alert.iloc[i, 'algo_name'] == 'fuel_trim_analysis':
        MATCH_FLAG = alert_matching(Next_five_hr_DTC,FUEL_DTC_LIST)
        df_alert.iloc[i, 'true/false_dtc'] = MATCH_FLAG        
             
    print(MATCH_FLAG)
    break    

#df_dtc.to_csv(output_path + Veichle_ID + "_"+ str(Alert_ts)  + "_" + str(end_ts) + ".csv") 
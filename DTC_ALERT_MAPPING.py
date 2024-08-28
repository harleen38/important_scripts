import requests 
import csv
import json
import pandas as pd
from datetime import datetime, timezone
import os
from pathlib import Path

#D:\DTC_ALERT_MAPPING.py


# for US vehicles set the url as "http://algo-internal-apis.intangles-aws-us-east-1.intangles.us:1234/dashboard_apis/fetch"
# for Indian vehicles set the url as "http://internal-apis.intangles.com/dashboard_apis/fetch"

url =  "https://algo-internal-apis.intangles-aws-us-east-1.intangles.us/dashboard_apis/fetch/"

# enter the output path where you want the output to be written
output_path = "D:/Work/FRP/CODE/"


def fetch_dtc_data(start_ts, end_ts, vehicle_id, country_flag='US'):
  

    if country_flag == 'US':
        url = "https://algo-internal-apis.intangles-aws-us-east-1.intangles.us/dashboard_apis/fetch/"
    if country_flag == 'IN':    
        url = "http://internal-apis.intangles.com/dashboard_apis/fetch/"
    
    df_all_dtcs = pd.DataFrame()
    
    headers = {
            'Content-Type': 'application/json',
        }
    vehicle_dtc_data = {"report": "default",
        "filter":[
            {
                "fault_log.timestamp":{
                    "gt": start_ts,
                    "lt": end_ts
                }
            },
            {
                "fault_log.vehicle_id": str(vehicle_id)
            },
            # {
            #     "fault_log.status": 'active'
            # }
        ],
        "select":{
            "vehicle.id":{
                "value":True,
                "as":"vehicle_id"
            },
            "vehicle.account_id": {
                "value": True,
                "as": "account_id"
            },
            "vehicle.tag":{
                "value":True,
                "as":"vehicle_plate"
            },
            "fault_log.status":{
                "value":True,
                "as":"status"
            },
            "fault_log.code":{
                "value":True,
                "as":"code"
            },
            "fault_log.timestamp":{
                "value":True,
                "as":"time"
            },
            "spec.manufacturer":{
                "value":True,
                "as":"manufacturer"
            },
            "spec.model":{
                "value":True,
                "as":"model"
            },
            "spec.max_load_capacity":{
                "value":True,
                "as": "max_load_capacity"
            }
        }
        }

    dtc_response = requests.post(url, json=vehicle_dtc_data, headers=headers)
    print(dtc_response)
    print(start_ts)
    print(end_ts)
    dtc_csv_filename = 'dtc.csv'
    if dtc_response.status_code == 200:
        # Parse the JSON response
        dtc_json_data = dtc_response.json()
        print(dtc_json_data)
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
def alert_matching_v2(Next_five_hr_DTC, DTC_LIST):

    match_flag = False
    for dtc_cnt in range(0,len(DTC_LIST)):
        for fetch_dtc_cnt in range(0,len(Next_five_hr_DTC)):
            if (DTC_LIST[dtc_cnt] in Next_five_hr_DTC[fetch_dtc_cnt]) or (Next_five_hr_DTC[fetch_dtc_cnt] in DTC_LIST[dtc_cnt]):
                match_flag = True
                break
        if match_flag == True:
            break
    return match_flag        




def utc_to_miliseconds(utc_date_string):
    # Parse the UTC date string into a datetime object
    utc_datetime = datetime.strptime(utc_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Convert seconds to milliseconds
    milliseconds = int(utc_datetime.timestamp() * 1000)

    return milliseconds

def datetime_to_milliseconds(datetime_str):
    # Parse the datetime string to a datetime object
    # if datetime_str.endswith('+00'):
    #     datetime_str = datetime_str[:-3] + '+00:00'
    dt = datetime.strptime(datetime_str, "%Y-%m-%d")
    # Convert the datetime object to milliseconds since epoch
    milliseconds = int(dt.timestamp() * 1000) + (5*60+30)*60*1000
    return milliseconds

def strip_time(datetime_str):
    date_part = datetime_str.split(' ')[0]
    return date_part

  
# enter the start time and end time between which you want the dtc

#AID_DTC_LIST = ['523000-2','DB040E']
AID_DTC_LIST =  ["P0243",
                "P0244",
                "P0245",
                "P0246",
                "P0247",
                "P0248",
                "P0249",
                "P0250",
                "1188-4",
                "1188-7",
                "1188-8",
                "1188-9",
                "1188-10",
                "1188-11",
                "102-17",
                "8706",
                "8704",
                "1127-17",
                "1176-1",
                "1176-4",
                "1176-17",
                "1176-18",
                "261703",
                "261704",
                "26170D",
                "26170E",
                "261715",
                "580",
                "564",
                "46848",
                "P1238",
                "641-4",
                "641-7",
                "641-8",
                "641-9",
                "641-10",
                "641-11",
                "521012-1",
                "521012-17",
                "521012-18",
                "P0299",
                "102-1",
                "102-18",
                "1127-1",
                "1127-18",
                "470A01",
                "660012",
                "660001",
                "8802",
                "P226C",
                "EB0D12"
            ]
ECT_DTC_LIST =  ['P2183',
'P2185',
'4193',
'P00B4',
'P00B5',
'P2560',
'P2182',
'P2600',
'P0119',
'P0118',
'P2603',
'P2601',
'111',
'P0117',
'1659',
'4194',
'7423',
'P2B9D',
'P26A6',
'P050C',
'P2556',
'P2602',
'20',
'P2681',
'P2682',
'P2683',
'P2AAA',
'P26AA',
'5708',
'P26D6']
DPF_DTC_LIST = ['P2003', 'P244B']
#BAT_DTC_LIST = ['P0562', 'P0563', 'P0620', 'P0621', 'P0630']
BAT_DTC_LIST = ['39',
'158',
'P0560',
'677',
'P2500',
'P0616',
'168',
'P0615',
'1321',
'251',
'P0617',
'1795',
'8447',
'115',
'1122',
'P26E6',
'P3020',
'P3030',
'P3000',
'P058A',
'P26E5',
'P26E4',
'2634']
FUEL_TRIM_DTC_LIST = ['P0170' ,'P0171', 'P0172', 'P0173', 'P0174', 'P0175']


df_alert = pd.read_csv("D:/UPS_Predictive_Alert (1).csv", dtype={'vehicle_id':'int64'})
#df_alert['time_miliseconds'] = df_alert['timestamp'].apply(datetime_to_milliseconds)
# Apply the function to the 'timestamp' column
df_alert['date'] = df_alert['timestamp'].apply(strip_time)  
df_alert['timestamp_ms'] = df_alert['date'].apply(datetime_to_milliseconds)


for i in range(len(df_alert)):
    Alert_ts =  int(df_alert.loc[i,'timestamp_ms'])
    # end_ts 5 days after
    end_ts =    int(Alert_ts + 432000000)  # Alert_ts + 5*24*60*60*1000
    Veichle_ID = str(df_alert.loc[i,'vehicle_id'])  
    # getting the dtcs in the 5days
    df_dtc = fetch_dtc_data(Alert_ts, end_ts, Veichle_ID)
    df_dtc = df_dtc.drop_duplicates(keep='first')
    df_dtc['time_miliseconds'] = df_dtc['time'].apply(utc_to_miliseconds)
    df_dtc = df_dtc.drop_duplicates()
    Next_five_hr_DTC = df_dtc["code"].tolist()
    df_alert.loc[i,"Next_5_hr_dtcs"] = str(Next_five_hr_DTC)
    # checking if the alert-type is bat
    if df_alert.loc[i, 'algo_name'] == 'bat':    
        MATCH_FLAG = alert_matching_v2(Next_five_hr_DTC,BAT_DTC_LIST)
        df_alert.loc[i, 'true/false_dtc'] = MATCH_FLAG
    # checking if the alert-type is aid    
    elif  df_alert.loc[i, 'algo_name'] == 'aid':
        MATCH_FLAG = alert_matching_v2(Next_five_hr_DTC,AID_DTC_LIST)
        df_alert.loc[i, 'true/false_dtc'] = MATCH_FLAG
    # checking if the alert-type is ect    
    elif  df_alert.loc[i, 'algo_name'] == 'ect':
        MATCH_FLAG = alert_matching_v2(Next_five_hr_DTC,ECT_DTC_LIST)
        df_alert.loc[i, 'true/false_dtc'] = MATCH_FLAG
    # checking if the alert-type is  fuel_trim_anlaysis
    elif  df_alert.loc[i, 'algo_name'] == 'fuel_trim_analysis':
        MATCH_FLAG = alert_matching_v2(Next_five_hr_DTC,FUEL_TRIM_DTC_LIST)
        df_alert.loc[i, 'true/false_dtc'] = MATCH_FLAG      
    print(i, " loop ", "complete")  
df_alert.to_excel("D:/DTC_ALERT_MAPPING/" + "UPS_VEHICLES"  + ".xlsx")
    
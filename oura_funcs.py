#import the libraries
from oura import OuraClient
import notebooks_config #I store all my credentials in a notebooks_config.py file. This file is then included in the .gitignore list so I can share the notebooks on GitHub.  
import datetime
from datetime import date
from dateutil import parser
import pandas as pd
import numpy as np

def oura_load(start_date, end_date):
    oura_pat = notebooks_config.oura_pat #
    oura_client_id = notebooks_config.oura_client_id
    oura_client_secret = notebooks_config.oura_client_secret

    client = OuraClient(personal_access_token=oura_pat)
    oura = OuraClient(oura_client_id, oura_client_secret, oura_pat)
    result = oura.sleep_summary(start= start_date, end= end_date)
    data = result['sleep'][0] #select the first item from the list
    return data
def start_time(start_date, end_date):
    #get the start and endtime as strings
    data = oura_load(start_date, end_date)
    start_time = data['bedtime_start']
    end_time = data['bedtime_end']
    # convert strings to datetime using dateutil
    start_time_dt = parser.parse(start_time)
    end_time_dt = parser.parse(end_time)
    #remove timezones
    start_time_dt = start_time_dt.replace(tzinfo=None)
    end_time_dt = end_time_dt.replace(tzinfo=None)
    return start_time_dt
    #('start time is '+ str(start_time_dt) + ' and end time is ' + str(end_time_dt))
def end_time(start_date, end_date):
    #get the start and endtime as strings
    data = oura_load(start_date, end_date)
    start_time = data['bedtime_start']
    end_time = data['bedtime_end']
    # convert strings to datetime using dateutil
    start_time_dt = parser.parse(start_time)
    end_time_dt = parser.parse(end_time)
    #remove timezones
    start_time_dt = start_time_dt.replace(tzinfo=None)
    end_time_dt = end_time_dt.replace(tzinfo=None)
    return end_time_dt
def sleep_total(start_date, end_date):
    my_start_time = start_time(start_date, end_date)
    my_end_time = end_time(start_date, end_date)
    sleep_total = my_end_time - my_start_time
    return sleep_total
def startintervals(start_date, end_date):
    start_time_dt = start_time(start_date, end_date)
    time_change = datetime.timedelta(minutes=5)
    my_startivs = [start_time_dt]
    new_iv=start_time_dt
    my_stages = hypnogram(start_date, end_date)
    for i in range(len(my_stages)-1):
        new_iv= new_iv+time_change
        my_startivs.append(new_iv)
    return my_startivs
def hypnogram(start_date, end_date):
    #get the hypnogram as one long string
    data = oura_load(start_date, end_date)
    hypnogram = data['hypnogram_5min']
    # convert the hypnogram to a list of strings
    string_list=[]
    string_list[:0]=hypnogram
    # convert the list of strings to a list of integers
    my_stages=[] #create an empty list for the sleep stages
    for i in range(len(string_list)):
        integer = int(string_list[i])
        my_stages.append(integer)
    return my_stages
def hr(start_date, end_date):
    data = oura_load(start_date, end_date)
    my_hr = data['hr_5min']
    return my_hr
def HRV(start_date, end_date):
    data = oura_load(start_date, end_date)
    my_HRV = data['rmssd_5min']
    return my_HRV
def make_df(start_date, end_date):
    sleep_df = pd.DataFrame() #create an empty data frame
    # Add columns with their data to the df
    sleep_df['Start_time']=startintervals(str(start_date), str(end_date))
    sleep_df['Stage']= hypnogram(str(start_date), str(end_date))
    sleep_df['hr']=pd.Series(hr(str(start_date), str(end_date)))
    sleep_df['HRV']=pd.Series(HRV(str(start_date), str(end_date)))
    sleep_df = sleep_df.replace(0, np.NaN) # replace 0 with NaN
    return sleep_df
def deepsleep(start_date, end_date):
    deep_sleep = hypnogram(start_date, end_date).count(1)
    deep_sleep_perc= round((deep_sleep/len(hypnogram(start_date, end_date))*100),2)
    return deep_sleep*5, deep_sleep_perc
def stats(start_date, end_date):
    data=oura_load(start_date, end_date)
    breath = data['breath_average']
    temp_dev = data['temperature_deviation']
    restless = data['restless']
    return breath, temp_dev, restless
def stages(start_date,end_date):
    my_stages =[]
    data = oura_load(start_date, end_date)
    awake = data['awake']/60
    rem = data['rem']/60
    light=data['light']/60
    deep= data['deep']/60
    my_stages.append(awake)
    my_stages.append(rem)
    my_stages.append(light)
    my_stages.append(deep)
    return my_stages
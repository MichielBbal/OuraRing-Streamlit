#snoring_funcs
import datetime
from datetime import date
import pandas as pd
import influxdb 
from influxdb import DataFrameClient
import oura_funcs # import the oura functions
import notebooks_config

# setup the influx client
def influxclient():
    try:
        host = notebooks_config.red_rpi_ip
        mydf_client = DataFrameClient(host=host, port=8086, database='SNORING')# this is my raspberry ip on a local network
        return mydf_client
    except:
        return print('RPI not available')
#helper function to make the query string:
def query_string(start_date, end_date):
    start_time_dt = oura_funcs.start_time(start_date, end_date)
    end_time_dt = oura_funcs.end_time(start_date, end_date)
    base_string = "SELECT * FROM my_snoring WHERE time >= '"
    middle_string = "' AND time <='"
    end_string = "'"
    query_string = base_string + str(start_time_dt) + middle_string + str(end_time_dt)+end_string
    return query_string
def create_snoring_df(start_date, end_date):
    mydf_client = influxclient()
    mydf_client.switch_database('SNORING')   
    helper_df=pd.DataFrame()
    snoring_df=pd.DataFrame()
    my_query_string = query_string(start_date, end_date)
    helper_df = mydf_client.query(my_query_string)
    snoring_df =helper_df['my_snoring']
    return snoring_df
def snoring_stats(start_date, end_date):
    stats_df = pd.DataFrame()
    snoring_df = create_snoring_df(start_date, end_date)
    snoring_df['bins'] = pd.cut(snoring_df['snoring'], bins=[0.0, 0.10, 0.50, 1.00],
                    labels=['no snoring', 'light snoring', 'loud snoring']) 
    stats_df['count'] =snoring_df['bins'].value_counts()
    #stats_df['minutes']= round(snoring_df['bins'].value_counts()/60,1)
    total_length = snoring_df['bins'].count()
    stats_df['percentage']=round(stats_df['count']/total_length *100,1)
    return stats_df

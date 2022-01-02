import streamlit as st
import pandas as pd
import oura_funcs
from datetime import date
import datetime
import numpy as np

st.title('My oura sleep data')

# Sidebar inputs
st.sidebar.header('Oura data')
st.sidebar.write('Select the date of waking up and click the "Load" button')
end_date = st.sidebar.date_input('End date', date.today())
start_date = end_date - datetime.timedelta(days=1)

if st.sidebar.button('Load'):
    st.write("The start date is: "+ str(start_date))
    st.write('The end date is: '+ str(end_date))

    sleep_df = pd.DataFrame() #create an empty data frame

    # Add the columns with data to the df
    sleep_df['Start_time']=oura_funcs.startintervals(str(start_date), str(end_date))
    sleep_df['Stage']= oura_funcs.hypnogram(str(start_date), str(end_date))
    sleep_df['hr']=oura_funcs.hr(str(start_date), str(end_date))
    sleep_df['HRV']=oura_funcs.HRV(str(start_date), str(end_date))
    sleep_df = sleep_df.replace(0, np.NaN) # replace 0 with NaN

    #create the graphs
    st.bar_chart(sleep_df['Stage'])
    st.line_chart(sleep_df['HRV'])
    st.line_chart(sleep_df['hr'])

    #show the dataframe
    st.write('And this is the data:')
    st.dataframe(sleep_df)
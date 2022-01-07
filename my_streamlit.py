import streamlit as st
import pandas as pd
import oura_funcs
from datetime import date
import datetime
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.title('Oura sleep data')


# Sidebar inputs
st.sidebar.header('Oura data')
st.sidebar.write('Select the date of waking up and click the "Load" button')
end_date = st.sidebar.date_input('End date', date.today())
start_date = end_date - datetime.timedelta(days=1)

if st.sidebar.button('Load'):
    
       
    
    #define columns
    col1, col2 = st.columns(2)

    with col1:
        st.write("The start date is: "+ str(start_date))
        st.write('The end date is: '+ str(end_date))
    
        # show start and endtimes
        start_time = oura_funcs.start_time(str(start_date), str(end_date))
        end_time = oura_funcs.end_time(str(start_date), str(end_date))
        st.write('You fell asleep at: '+ str(start_time))
        st.write('You woke up at: ' + str(end_time))
        #calculate time in deep sleep
        st.write('Your deep sleep was ' + str(oura_funcs.deepsleep(str(start_date), str(end_date))[0]) + ' minutes')
        st.write('That is ' + str(oura_funcs.deepsleep(str(start_date), str(end_date))[1]) + '% of the time')
    
        sleep_df = oura_funcs.make_df(start_date, end_date)
       
        #first graph 
        st.bar_chart(sleep_df['Stage'])
        with st.expander("See explanation"):
            st.write("""
            4 = Awake 3 = REM-sleep 2 = Light sleep 1 = Deep sleep
            """)
        st.line_chart(sleep_df['HRV'])    
    with col2:
        #calculate and show averages
        hr_mean = sleep_df['hr'].mean()
        HRV_mean=sleep_df['HRV'].mean()
        st.write('average hr: ' + str(round(hr_mean)))
        st.write('average HRV: ' + str(round(HRV_mean)))

        #calculate and show minimal values
        hr_min =sleep_df['hr'].min()
        HRV_min=sleep_df['HRV'].min()
        st.write('minimum hr: ' + str(round(hr_min)))
        st.write('minimum HRV: ' + str(round(HRV_min)))
        #calculate and show maximum values
        hr_max =sleep_df['hr'].max()
        HRV_max=sleep_df['HRV'].max()
        st.write('maximum hr: ' + str(round(hr_max)))
        st.write('maximum HRV: ' + str(round(HRV_max)))
        st.line_chart(sleep_df['hr'])
        #show the dataframe
        st.write('And this is the data:')
        st.dataframe(sleep_df)
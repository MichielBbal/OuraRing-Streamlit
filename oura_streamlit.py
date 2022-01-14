import streamlit as st
import pandas as pd
import datetime
from datetime import date
import matplotlib.pyplot as plt
#import the other python files
import oura_funcs #oura functions
import snoring_funcs # snoring functions

# Setting page to wide mode and showing dashboard title
st.set_page_config(layout="wide")
st.title('Oura sleep data')

# Sidebar inputs
st.sidebar.header('Oura data')
st.sidebar.write('Select the date of waking up and click the "Load" button')
end_date = st.sidebar.date_input('End date', date.today())
start_date = end_date - datetime.timedelta(days=1)

#instantiate the dataframes
sleep_df = oura_funcs.make_df(start_date, end_date)

if st.sidebar.button('Load'):
    snoring_df = snoring_funcs.create_snoring_df(str(start_date), str(end_date))
    stats_df = snoring_funcs.snoring_stats(str(start_date), str(end_date))
    st.write(stats_df)
    #define columns
    col1, col2 = st.columns(2)

    with col1:
        # show start and endtimes
        start_time = oura_funcs.start_time(str(start_date), str(end_date))
        end_time = oura_funcs.end_time(str(start_date), str(end_date))
        sleep_total = oura_funcs.sleep_total(str(start_date), str(end_date))
        st.write('You fell asleep at: '+ str(start_time))
        st.write('You woke up at: ' + str(end_time))
        st.write("Your total sleep time was: "+ str(sleep_total))
        #calculate time in deep sleep
        st.write('Your deep sleep was ' + str(oura_funcs.deepsleep(str(start_date), str(end_date))[0]) + ' minutes. That is ' + str(oura_funcs.deepsleep(str(start_date), str(end_date))[1]) + '% of the time') 
        #other stats
        breath = oura_funcs.stats(str(start_date), str(end_date))[0]
        temp_dev = oura_funcs.stats(str(start_date), str(end_date))[1]
        restless = oura_funcs.stats (str(start_date), str(end_date))[2]
        st.write('Average breathing: '+ str(breath))
        st.write('Temperature deviation: '+ str(temp_dev))
        st.write('Restlessness %: ' + str(restless)) 
       
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
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Awake', 'Rem', 'Light', 'Deep'
        sleep = oura_funcs.stages(str(start_date), str(end_date))
        #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sleep, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle. explode=explode, 
        st.pyplot(fig1)

        #show the dataframe
        st.write('And this is the data:')
        st.dataframe(sleep_df)

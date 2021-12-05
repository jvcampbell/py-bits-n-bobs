# Description: Scrapes timesheet entries from Toggl.com and then fills in the timesheet form at beyondrecruitment.co.nz

import pandas as pd
import numpy as np
import datetime
import requests
import base64
import urllib.parse as ul

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import time

## Parameters
Start_Date = '2021-11-29'
End_Date = str(datetime.date.today())
Api_Key = '<api key>'


Start_Date = Start_Date + 'T00:00:00+12:00'
Start_Date = ul.quote(Start_Date)
End_Date = End_Date + 'T23:59:59+12:00'
End_Date = ul.quote(End_Date)


def getTogglEntries(toggl_api_key, Start_Date, End_Date):
    #       https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md


    toggl_url =  'https://api.track.toggl.com/api/v8/time_entries' \
                        + '?start_date=' + Start_Date \
                        + '&end_date=' + End_Date

    auth_header = toggl_api_key + ":" + "api_token"
    auth_header = "Basic {}".format(base64.b64encode(bytes(auth_header, "utf-8")).decode("ascii"))
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "jupytertry",
    }

    response = requests.get(toggl_url,headers=headers)

    #GET https://api.track.toggl.com/api/v8/time_entries/{time_entry_id}

    dict_response = response.json()

    return pd.DataFrame(dict_response)


# Get & Clean the Time Entries

df_toggl_raw_entries = getTogglEntries(Api_Key,Start_Date, End_Date)

df_time_entries = pd.DataFrame(index=df_toggl_raw_entries.index)
df_time_entries['StartDateTime'] = df_toggl_raw_entries['start'].astype('datetime64').dt.tz_localize('UCT').dt.tz_convert('Pacific/Auckland')
df_time_entries['EndDateTime'] = df_toggl_raw_entries['stop'].astype('datetime64').dt.tz_localize('UCT').dt.tz_convert('Pacific/Auckland')
df_time_entries['StartDate'] = df_time_entries['StartDateTime'].dt.date
df_time_entries['Duration'] = df_toggl_raw_entries['duration'].astype('timedelta64[s]')
 
df_daily_time = df_time_entries.groupby('StartDate').agg({'StartDateTime':'min','EndDateTime':'max',                                                        
                                                        'Duration':'sum'})
df_daily_time['Total_Potentional_Duration'] = df_daily_time['EndDateTime'] - df_daily_time['StartDateTime']

#Add a minute to the break. The seconds are cut off when entering into the form which slightly inflates my work time.
df_daily_time['Break_Duration'] = (df_daily_time['Total_Potentional_Duration'] - df_daily_time['Duration']) + datetime.timedelta(minutes=1)

df_daily_time['StartTime'] = df_daily_time['StartDateTime'].dt.time
df_daily_time['EndTime'] = df_daily_time['EndDateTime'].dt.time

# Display Entries
print()
print("Entries")
print("-------")
print()

print(df_daily_time[['StartTime','Break_Duration','EndTime','Duration']])

# Display Summary
seconds = df_daily_time['Duration'].dt.total_seconds().sum()
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

print("Total")
print("-----")
print("Hours and Minutes          --> %d:%d" %(hours,minutes))

df_daily_time['Duration'].mean()


###    Submit form

# https://www.youtube.com/watch?v=ZLkx-cAxrgg

def date_from_timedelta(x):
    ts = x.total_seconds()
    hours, remainder = divmod(ts, 3600)
    minutes, seconds = divmod(remainder, 60)
    return ('{}:{:02d}:{:02d}').format(int(hours), int(minutes), int(seconds)) 

# Login

driver = webdriver.Safari()
driver.get('<target website>')
time.sleep(1)

input_email = driver.find_element_by_id('ctl00_MainContentPlaceHolder_txtLogin')
input_password = driver.find_element_by_id('ctl00_MainContentPlaceHolder_txtPassword')
btn_login = driver.find_element_by_id('ctl00_MainContentPlaceHolder_LoginButton')

input_email.send_keys('<email>')
input_password.send_keys('<password>')
btn_login.click()

time.sleep(4)
ids = driver.find_elements_by_xpath('//*[@id]')

## Get the date elements

ls_date_ids = []
ls_date_values = []

#date header ids
for i in ids:
    if(i.get_attribute('id').startswith('dh')):
        ls_date_ids.append(i.get_attribute('id'))
        
#corresponding dates        
for i in ls_date_ids:
    ls_date_values.append(driver.find_element_by_id(i).text)
        
df_page_elements = pd.DataFrame(data=ls_date_ids,columns=['Date_Header_Id'])
df_page_elements['Base_Id'] = df_page_elements['Date_Header_Id'].apply(lambda x: x[2:])
df_page_elements['Row_Date_Value'] = pd.DataFrame(ls_date_values)
df_page_elements['Row_Date_Value'] = pd.to_datetime(df_page_elements['Row_Date_Value'],format='%d/%m/%Y')
df_page_elements.set_index('Row_Date_Value', inplace=True)

df_page_elements = df_page_elements.join(df_daily_time[['StartTime','Break_Duration','EndTime','Duration']])
df_page_elements.dropna(subset=['EndTime'],inplace=True)

df_page_elements['Break_Duration'] = df_page_elements['Break_Duration'].apply(date_from_timedelta)

df_page_elements['Break_Duration_Hr'] = df_page_elements['Break_Duration'] \
                                        .astype('datetime64').dt.hour \
                                        .astype('str')
df_page_elements['Break_Duration_Min'] = df_page_elements['Break_Duration'] \
                                        .astype('datetime64').dt.minute \
                                        .astype('str')


## Fill out the form

for idx in df_page_elements.index:
    print(idx, df_page_elements['Base_Id'][idx])
    
    
    dd_Pay_Item = driver.find_element_by_name('pi' + df_page_elements['Base_Id'][idx])
    driver.execute_script("arguments[0].scrollIntoView();", dd_Pay_Item)
    actions = ActionChains(driver)
    actions.move_to_element(dd_Pay_Item).perform()
    Select(dd_Pay_Item).select_by_visible_text('Normal')
    
    fld_Start_Hour = driver.find_element_by_name('sh' + df_page_elements['Base_Id'][idx])
    fld_Start_Hour.send_keys(df_page_elements['StartTime'][idx].hour)
    
    fld_Start_Min = driver.find_element_by_name('sm' + df_page_elements['Base_Id'][idx])
    fld_Start_Min.send_keys(df_page_elements['StartTime'][idx].minute)
    
    fld_Break_Hour = driver.find_element_by_name('bh' + df_page_elements['Base_Id'][idx])
    fld_Break_Hour.send_keys(df_page_elements['Break_Duration_Hr'][idx]) 
    
    fld_Break_Min = driver.find_element_by_name('bm' + df_page_elements['Base_Id'][idx])
    fld_Break_Min.send_keys(df_page_elements['Break_Duration_Min'][idx])
    
    fld_End_Hour = driver.find_element_by_name('eh' + df_page_elements['Base_Id'][idx])
    fld_End_Hour.send_keys(df_page_elements['EndTime'][idx].hour)
    
    fld_End_Min = driver.find_element_by_name('em' + df_page_elements['Base_Id'][idx])
    fld_End_Min.send_keys(df_page_elements['EndTime'][idx].minute)  
    
   
    

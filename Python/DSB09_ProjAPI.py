#!/usr/bin/env python
# coding: utf-8

# # Import & Prep data

# In[ ]:


# https://data.tmd.go.th/api/DailySeismicEvent/v1/?uid=api&ukey=api12345


# In[63]:


import requests
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[7]:


url = "https://data.tmd.go.th/api/DailySeismicEvent/v1/?uid=api&ukey=api12345&format=json"


# In[91]:


respone = requests.get(url)
# 200 get data ok


# In[89]:


if respone.status_code == 200: 
    print("200: get data ok")
else:
    print("please check your url again.")


# In[87]:


# fetch data
event = respone.json()


# In[233]:


len_ = len(event['DailyEarthquakes'])
print(f"Length of json: {len_}")

title = []
dt_utc = []
dt_tha = [] 
depth = []
magnitude = []
lat = [] 
long = []


# In[235]:


for i in range(0, len_):
    tit_ = event['DailyEarthquakes'][i]['TitleThai']
    utc_ = event['DailyEarthquakes'][i]['DateTimeUTC'] 
    tha_ = event['DailyEarthquakes'][i]['DateTimeThai'] 
    dep_ = event['DailyEarthquakes'][i]['Depth'] 
    mag_ = event['DailyEarthquakes'][i]['Magnitude'] 
    lat_ = event['DailyEarthquakes'][i]['Latitude'] 
    lon_ = event['DailyEarthquakes'][i]['Longitude']

    title.append(tit_)
    dt_utc.append(utc_)
    dt_tha.append(tha_)
    depth.append(dep_)
    magnitude.append(mag_)
    lat.append(lat_)
    long.append(lon_)
    
print("Successfully get request")


# In[237]:


# สร้าง Dictionary
data_dict = {
    'title': title,
    'dt_utc': dt_utc,
    'dt_tha': dt_tha,
    'depth': depth,
    'magnitude': magnitude,
    'lat': lat,
    'long': long
}


# In[239]:


earthquakes_df = pd.DataFrame(data_dict)


# In[240]:


earthquakes_df


# In[243]:


earthquakes_df['country'] = earthquakes_df['title'].str.extract(r'ประเทศ([^\s]+)')
earthquakes_df['province'] = earthquakes_df['title'].str.extract(r'จ\.([^\s]+)')
earthquakes_df['amphoe'] = earthquakes_df['title'].str.extract(r'อ\.([^\s]+)')
earthquakes_df['tambon'] = earthquakes_df['title'].str.extract(r'ต\.([^\s]+)')
earthquakes_df.sample(5)


# In[332]:


# แปลงคอลัมน์เป็น datetime
earthquakes_df['dt_utc'] = pd.to_datetime(earthquakes_df['dt_utc'])
earthquakes_df['dt_tha'] = pd.to_datetime(earthquakes_df['dt_tha'])
# แปลงคอลัมน์เป็น numeric
earthquakes_df['depth'] = pd.to_numeric(earthquakes_df['depth'])
earthquakes_df['magnitude'] = pd.to_numeric(earthquakes_df['magnitude'])

earthquakes_df['country'] = earthquakes_df['country'].replace(np.nan, 'ไทย')

earthquakes_df['year'] = earthquakes_df['dt_tha'].dt.year
earthquakes_df['month'] = earthquakes_df['dt_tha'].dt.month
earthquakes_df['month_id'] = earthquakes_df['year'].astype(str) + '-' + earthquakes_df['month'].astype(str)
earthquakes_df.sample(5)


# In[246]:


earthquakes_df.info()


# In[248]:


event['DailyEarthquakes'][408]['TitleThai']


# # EDA

# In[284]:


import matplotlib.font_manager as fm
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
for font in font_list:
    if 'thai' in font.lower():
        print(font)


# In[310]:


# กำหนด path ของฟอนต์
font_path = r'C:\Users\User\AppData\Local\Microsoft\Windows\Fonts\NotoSansThai-SemiBold.ttf'

# สร้าง FontProperties object
font_prop = fm.FontProperties(fname=font_path)

# ตั้งค่าฟอนต์ให้กับ Matplotlib
plt.rcParams['font.family'] = font_prop.get_name()


# In[273]:


# depth
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
sns.boxplot(data=earthquakes_df, x="depth", ax=axes[0]) # กราฟ Boxplot
earthquakes_df["depth"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[314]:


# magnitude
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
sns.boxplot(data=earthquakes_df, x="magnitude", ax=axes[0]) # กราฟ Boxplot
earthquakes_df["magnitude"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[316]:


print(earthquakes_df.shape)
g_country = earthquakes_df.groupby(['country']).agg({'country':'count'})\
    .rename(columns={'country': 'count'})\
    .sort_values(by='count', ascending=False)
g_country = g_country.reset_index()

print(g_country)
plt.figure(figsize=(5,3))
sns.countplot(data=earthquakes_df, x="country")
plt.show()


# In[320]:


print(earthquakes_df.shape)
g_province = earthquakes_df.groupby(['province']).agg({'province':'count'})\
    .rename(columns={'province': 'count'})\
    .sort_values(by='count', ascending=False)
g_province = g_province.reset_index()

print(g_province)
plt.figure(figsize=(10,3))
sns.countplot(data=earthquakes_df, x="province")
plt.show()


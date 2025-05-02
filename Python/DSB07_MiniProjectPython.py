#!/usr/bin/env python
# coding: utf-8

# # Final Project - Analyzing Sales Data

# In[2]:


import pandas as pd
pd.options.display.max_columns = None
import warnings
warnings.filterwarnings("ignore")
import numpy as np


# In[3]:


df = pd.read_csv("Ref/Data Files/sample-store.csv") 
print(df.shape )
df.head() 


# In[4]:


# see data frame information using .info() 
df.info() 


# In[5]:


# We can use pd.to_datetime() function to convert columns 'Order Date' and 'Ship Date' to datetime.
# example of pd.to_datetime() function 
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y') 
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y') 


# In[6]:


df.sample(3)


# In[7]:


# TODO - convert order date and ship date to datetime in the original dataframe
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y') 
print(f"The data type of 'Order Date' is {df['Order Date'].dtype}.")
print(f"The data type of 'Ship Date' is {df['Ship Date'].dtype}.")
df.sample(3)


# In[8]:


# TODO - count nan in postal code column
nan_postal = df['Postal Code'].isna().sum()
print(f"The number of NaN in postal code column is {nan_postal} records")


# In[9]:


df.isna().sum()


# In[10]:


# TODO - filter rows with missing values
miss_val = df[ df['Postal Code'].isna() ]
print(f"the number of rows with missing values are {miss_val.shape[0]} rows.")
miss_val.sample(3)


# In[11]:


# TODO - Explore this dataset on your owns, ask your own questions 
# How many records are grouped by Category and Sub-Category?
grouped_df = df.groupby(["Category", "Sub-Category"])['Row ID'].agg(['count']).reset_index()
grouped_df.sort_values(['Category', 'count'], ascending=[True, False])


# ## Data Analysis Part

# Answer 10 below questions to get credit from this course. Write pandas code to find answers.

# In[14]:


# TODO 01 - how many columns, rows in this dataset
print(f"the number of rows are {df.shape[0]} rows.")
print(f"the number of columns are {df.shape[1]} columns.")


# In[15]:


# TODO 02 - is there any missing values?, if there is, which colunm? how many nan values? 
miss_df = df.isna().sum()
miss_df = pd.DataFrame(miss_df).reset_index()
miss_df.columns = ['index', 'count_nan']
miss_df.query('count_nan > 0')


# In[16]:


# TODO 03 - your friend ask for `California` data, filter it and export csv for him 
ca_df = df[df['State'] == 'California']
ca_df.to_csv("ExportFiles/california_df.csv")


# In[18]:


# TODO 04 - your friend ask for all order data in `California` and `Texas` in 2017 (look at Order Date), send him csv file
ca_tx_df = df[ ((df['State'] == 'California') | (df['State'] == 'Texas')) & (df['Order Date'].dt.year == 2017)]
ca_tx_df.to_csv("ExportFiles/california_texas_2017_df.csv")


# In[29]:


# TODO 05 - how much total sales, average sales, and standard deviation of sales your company make in 2017 
df_2017 = df[df['Order Date'].dt.year == 2017]
# df_2017 = df.copy()
df_2017['year'] = df['Order Date'].dt.year
df_2017.groupby('year')['Sales'].agg(['sum', 'mean', 'std']).reset_index()


# In[31]:


# TODO 06 - which Segment has the highest profit in 2018
df_2018 = df[df['Order Date'].dt.year == 2018]
df_2018['year'] = df['Order Date'].dt.year


# In[33]:


hg_profit = df_2018.groupby(['year', 'Segment'])['Profit'].agg(['sum']).reset_index()\
    .sort_values('sum', ascending=False)
print(f"The highest profit in 2018 is the {hg_profit.iloc[0, 1]} segment. That make a profit of ${hg_profit.iloc[0, 2]}")
hg_profit


# In[35]:


# TODO 07 - which top 5 States have the least total sales between 15 April 2019 - 31 December 2019 
date_str = pd.to_datetime('2019-04-15')
date_end = pd.to_datetime('2019-12-31')
range_df = df[ (df['Order Date'] >= date_str) & (df['Order Date'] <= date_end) ][['State', 'Sales']]
top5_least = range_df.groupby(['State'])['Sales'].agg(['sum']).reset_index()\
    .sort_values('sum', ascending=True).head(5)
top5_least


# In[37]:


# TODO 08 - what is the proportion of total sales (%) in West + Central in 2019 e.g. 25% 
df_2019 = df[ (df['Order Date'].dt.year == 2019) ][['Order Date', 'Region', 'Sales']]
df_2019['year'] = df['Order Date'].dt.year
df_2019 = df_2019.groupby(['Region']).agg(total_sales=('Sales', 'sum')).reset_index()

# คำนวณร้อยละ
all_sales = df_2019['total_sales'].sum()
df_2019['percentage'] = (df_2019['total_sales'] / all_sales) * 100

# slice value for West & Central
west_prop = df_2019.query("Region == 'West'")['percentage'].values[0]
cent_prop = df_2019.query("Region == 'Central'")['percentage'].values[0]
print(f"The proportion of total sales in West & Central in 2019 is {round(west_prop+cent_prop, 2)} %")
df_2019


# In[39]:


# TODO 09 - find top 10 popular products in terms of number of orders vs. total sales during 2019-2020
df_prod = df[ (df['Order Date'].dt.year >= 2019) | (df['Order Date'].dt.year <= 2020) ][['Order Date', 'Product Name', 'Order ID', 'Sales']]

# terms of number of orders
n_order = df_prod.groupby(['Product Name']).agg(n_orders=('Order ID', 'count'))\
    .reset_index().sort_values('n_orders', ascending=False).head(10)
n_order['top_n'] = pd.RangeIndex(10)

# terms of total sales
t_sale = df_prod.groupby(['Product Name']).agg(t_sales=('Sales', 'sum'))\
    .reset_index().sort_values('t_sales', ascending=False).head(10)
t_sale['top_n'] = pd.RangeIndex(10)

top_10 = pd.merge(n_order, t_sale, on='top_n')
top_10 = top_10[['top_n', 'Product Name_x', 'n_orders', 'Product Name_y', 't_sales']] # re-columns
top_10 = top_10.rename(columns={"Product Name_x": "Product_byOrders", "Product Name_y": "Product_bySales"}) # rename-columns
top_10


# In[41]:


# TODO 10 - plot at least 2 plots, any plot you think interesting :)
df_plot = df[ df['Order Date'].dt.year == 2020 ][['Order Date', 'Segment', 'Sales', 'Profit']]

# graph 1: Total sales by Segment in 2020
segment_sales = df_plot.groupby(['Segment']).agg(t_sales=('Sales', 'sum')).reset_index()
segment_sales[['Segment', 't_sales']].plot(x='Segment', y='t_sales' ,kind='barh', color=['salmon', 'orange', 'gold']);


# In[43]:


# graph 2: Total Profit Trend in 2020
df_plot['month_'] = df_plot['Order Date'].dt.month
date_profit = df_plot.groupby(['month_']).agg(t_profit=('Profit', 'sum')).reset_index()
date_profit[['month_', 't_profit']].plot(x='month_', y='t_profit' ,kind='line', color='darkgreen');


# In[45]:


# TODO Bonus - use np.where() to create new column in dataframe to help you answer your own questions
import numpy as np
# segment_sales = { high : > 5000, middle : < 5000 & >= 100, low : < 100 }
df['segment_sales'] = np.where(df['Sales'] > 5000, 'high', np.where(df['Sales'] < 100, 'low', 'middle'))

# Number of product orders grouped by sales segments at high, middle and low levels
seg_sale = df[ ['Sales', 'segment_sales'] ]
seg_sale.groupby(['segment_sales']).agg(n_value=('segment_sales', 'count')).reset_index()


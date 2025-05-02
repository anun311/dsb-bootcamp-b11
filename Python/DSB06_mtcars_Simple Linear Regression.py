#!/usr/bin/env python
# coding: utf-8

# ## Simple Linear Regression

# In[219]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import math
import seaborn as sns


# In[342]:


import pickle
# ใช้ไลบรารี pickle ใน Python เพื่อบันทึกโมเดลเป็นไฟล์ .pkl


# In[260]:


# โหลดชุดข้อมูล mtcars จากไฟล์ CSV (หรือใช้จากไลบรารี statsmodels)
url = 'ref/mtcars.csv'
mtcars = pd.read_csv(url)

# กำหนดตัวแปรต้น (X) และตัวแปรตาม (y)
X = mtcars[['hp', 'wt', 'am']]
y = mtcars['mpg']


# sm.add_constant(X): เป็นการเพิ่มคอลัมน์ของค่าคงที่ (intercept) ให้กับ X ซึ่งจำเป็นสำหรับการวิเคราะห์ทางสถิติใน statsmodels

# In[262]:


# เพิ่มค่าคงที่ (constant) ให้กับ X (จำเป็นสำหรับ statsmodels)
X = sm.add_constant(X)


# In[264]:


model = sm.OLS(y, X).fit()


# sm.OLS(y, X).fit(): สร้างและฝึกโมเดล Ordinary Least Squares (OLS) Regression ซึ่งเป็นรูปแบบหนึ่งของ Linear Regression

# In[266]:


print(model.summary2())


# In[270]:


X = mtcars[['hp', 'wt', 'am']]
y = mtcars['mpg']


# In[143]:


# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[272]:


model = LinearRegression()
model.fit(X, y)


# In[274]:


y_pred = model.predict(X)


# In[300]:


y_pred


# In[278]:


mse = mean_squared_error(y, y_pred)
rmse = math.sqrt(mse)
r2 = r2_score(y, y_pred)

print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)
print("R-squared:", r2)


# In[280]:


print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)


# In[346]:


# บันทึกโมเดลเป็นไฟล์ .pkl
with open('mtcar_linear_reg_model.pkl', 'wb') as f:
    pickle.dump(model, f)


# In[284]:


inter_ = model.intercept_
hp_coef = model.coef_[0]
wt_coef = model.coef_[1]
am_coef = model.coef_[2]


# In[286]:


var_hp = 200
var_wt = 3.5
var_am = 1
mpg_ = inter_ + (hp_coef * var_hp) + (wt_coef * var_wt) + (am_coef * var_am)
mpg_


# In[288]:


plt.figure(figsize=(4,3), dpi=120)
sns.scatterplot(mtcars, x="hp", y="mpg", s=20)
plt.show()


# In[314]:


y_pred_df = pd.DataFrame(y_pred, index=y.index, columns=['mpg_predicted'])


# In[316]:


result_df = pd.concat([X, y, y_pred_df], axis=1)


# In[332]:


result_df['error_res'] = result_df['mpg'] -  result_df['mpg_predicted']
result_df['square_error'] = result_df['error_res'] ** 2


# In[334]:


result_df


# In[336]:


plt.figure(figsize=(4,3), dpi=120)
sns.scatterplot(result_df, x="hp", y="mpg_predicted", s=20)
# sns.lineplot(x=X, y=y, color="red")
plt.show()


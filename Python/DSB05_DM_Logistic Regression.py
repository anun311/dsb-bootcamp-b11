#!/usr/bin/env python
# coding: utf-8

# ## Logistic Regression

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score, recall_score, f1_score
import statsmodels.api as sm

import pickle
# ใช้ไลบรารี pickle ใน Python เพื่อบันทึกโมเดลของเราเป็นไฟล์ .pkl


# ## Load data set

# In[4]:


url = 'ref/diabetes.csv'
dm = pd.read_csv(url)
dm.head()


# In[5]:


# ปรับหัวคอลัมน์เป็น lower case
dm.columns = dm.columns.str.lower()
dm.head()


# ## Explore data

# In[7]:


print(dm.shape)
dm.describe().T


# In[8]:


# Outcome
outcome_grouped = dm.groupby(['outcome']).agg({'outcome':'count'}).rename(columns={'outcome': 'count'})
outcome_grouped = outcome_grouped.reset_index()
outcome_grouped 


# In[9]:


# pregnancies
print("pregnancies มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['pregnancies']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="pregnancies", ax=axes[0]) # กราฟ Boxplot
dm["pregnancies"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[10]:


# glucose
print("glucose มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['glucose']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="glucose", ax=axes[0]) # กราฟ Boxplot
dm["glucose"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[11]:


# bloodpressure
print("bloodpressure มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['bloodpressure']==0]), "รายการ")
print("bloodpressure มีค่า >= 100 mmHg จำนวน:", len(dm[dm['bloodpressure']>= 100]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="bloodpressure", ax=axes[0]) # กราฟ Boxplot
dm["bloodpressure"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[12]:


# skinthickness
print("skinthickness มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['skinthickness']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="skinthickness", ax=axes[0]) # กราฟ Boxplot
dm["skinthickness"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[13]:


# insulin
print("insulin มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['insulin']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="insulin", ax=axes[0]) # กราฟ Boxplot
dm["insulin"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[14]:


# bmi
print("bmi มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['bmi']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="bmi", ax=axes[0]) # กราฟ Boxplot
dm["bmi"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[15]:


# diabetespedigreefunction
print("diabetespedigreefunction มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['diabetespedigreefunction']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="diabetespedigreefunction", ax=axes[0]) # กราฟ Boxplot
dm["diabetespedigreefunction"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# In[16]:


# age
print("age มีค่าเป็นศูนย์ จำนวน:", len(dm[dm['age']==0]), "รายการ")
fig, axes = plt.subplots(1, 2, figsize=(10, 2))
sns.boxplot(data=dm, x="age", ax=axes[0]) # กราฟ Boxplot
dm["age"].plot.hist(ax=axes[1]) # กราฟ Histogram
plt.tight_layout() 
plt.show()


# ## ทดสอบ features

# In[18]:


X = dm[['pregnancies', 'glucose', 'bloodpressure', 'insulin',  'bmi', 'diabetespedigreefunction', 'age']]
y = dm['outcome']
# เพิ่มค่าคงที่ (constant) ให้กับ X (จำเป็นสำหรับ statsmodels)
X = sm.add_constant(X)
model = sm.Logit(y, X).fit()
print(model.summary())


# In[19]:


# กำหนดตัวแปรต้น (X) และตัวแปรตาม (y)
X = dm[['pregnancies', 'glucose', 'bloodpressure', 'bmi', 'diabetespedigreefunction']]
y = dm['outcome']


# ## แบ่งข้อมูลเป็นชุดฝึก (train) และชุดทดสอบ (test)

# In[21]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=137)


# ## สร้างและฝึกโมเดล Logistic Regression

# In[23]:


# สร้างและฝึกโมเดล Logistic Regression
model = LogisticRegression(max_iter=1000)  # เพิ่ม max_iter เพื่อให้แน่ใจว่าคอนเวอร์จ
model.fit(X_train, y_train)


# In[24]:


# # 4.1 การเลือกคุณลักษณะ (sklearn RFE)
# from sklearn.feature_selection import RFE
# model_rfe = LogisticRegression(max_iter=1000)
# rfe = RFE(model_rfe, n_features_to_select=5) # เลือก 5 ตัวแปรที่ดีที่สุด
# rfe = rfe.fit(X, y)
# print("Selected features:", X.columns[rfe.support_])


# In[25]:


# 5. ทำนายผลลัพธ์บนชุดฝึก (train set)
y_train_pred = model.predict(X_train)


# In[26]:


# แสดง Confusion Matrix เป็น Heatmap 
plt.figure(figsize=(3, 2))
cm = confusion_matrix(y_train, y_train_pred) # สร้าง Confusion Matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()


# In[27]:


# แสดง Classification Report & ประเมินประสิทธิภาพของโมเดล
print("Classification Report:\n", classification_report(y_train, y_train_pred))

# แสดง Accuracy
accuracy = accuracy_score(y_train, y_train_pred)
print(f"Accuracy: {accuracy}")


# ## ทำนายผลลัพธ์บนชุดทดสอบ (Test)

# In[29]:


# ทำนายผลลัพธ์บนชุดทดสอบ
y_pred = model.predict(X_test)
y_pred


# In[30]:


# คำนวณ Sigmoid probability
y_proba = model.predict_proba(X_test)
y_proba[:, 0]


# In[31]:


# บันทึกโมเดลเป็นไฟล์ .pkl
with open('diabetes_logistic_reg_model.pkl', 'wb') as f:
    pickle.dump(model, f)


# In[32]:


proba_df = pd.DataFrame(y_proba, columns=["prob_0", "prob_1"])
proba_df


# In[33]:


y_prob_a_series = pd.Series(y_proba[:, 0], index=y_test.index, name="prob_0")
y_prob_a_series


# In[34]:


# 6. ปรับให้เป็น DataFrame ใหม่
X_test_df = pd.DataFrame(X_test, columns=X.columns)  # สร้าง DataFrame จาก X_test
y_test_df = pd.DataFrame(y_test)
# แปลง y_pred เป็น Series
y_pred_series = pd.Series(y_pred, index=y_test.index, name="pred_outcome")
y_prob_a_series = pd.Series(y_proba[:, 0], index=y_test.index, name="prob_0")
y_prob_b_series = pd.Series(y_proba[:, 1], index=y_test.index, name="prob_use_1")

# 7. รวม DataFrame เข้าด้วยกัน
result_df = pd.concat([X_test_df, y_test_df, y_prob_a_series, y_prob_b_series, y_pred_series], axis=1)


# In[35]:


result_df.sample(5)


# ## ประเมินประสิทธิภาพของโมเดล

# In[37]:


# แสดง Confusion Matrix เป็น Heatmap 
plt.figure(figsize=(3, 2))
cm = confusion_matrix(y_test, y_pred) # สร้าง Confusion Matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()


# In[38]:


# แสดง Classification Report & ประเมินประสิทธิภาพของโมเดล
print("Classification Report:\n", classification_report(y_test, y_pred))

# แสดง Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")


# ## Let's predict 

# In[40]:


# แสดงค่าสัมประสิทธิ์ของโมเดล
print("Coefficients:")
print(pd.DataFrame(model.coef_, columns=X.columns))
print("Intercept:")
print(model.intercept_)


# In[41]:


model.coef_


# In[42]:


model.coef_[0][1]


# In[43]:


# เก็บเข้าตัวแแปรเพื่อใช้ในสมการ LR
inter_ = model.intercept_
coef_pregnancies = model.coef_[0][0]
coef_glucose = model.coef_[0][1]
coef_bp = model.coef_[0][2]
coef_bmi = model.coef_[0][3]
coef_dmpedfunc = model.coef_[0][4]


# In[44]:


from random import sample
ss = range(0,len(result_df))
sss = result_df.index[sample(ss,1)]
sss[0]
fx = result_df[result_df.index == sss[0]]
result_df[result_df.index == sss[0]]


# In[45]:


# vari_pregnancies = 6
# vari_glucose = 162
# vari_bp = 62
# vari_bmi = 24.3
# vari_dmpedfunc = 0.178


# In[46]:


vari_pregnancies = fx['pregnancies'].values
vari_glucose = fx['glucose'].values
vari_bp = fx['bloodpressure'].values
vari_bmi = fx['bmi'].values
vari_dmpedfunc = fx['diabetespedigreefunction'].values


# In[47]:


pred_ = inter_ + (vari_pregnancies * coef_pregnancies) + (vari_glucose * coef_glucose) + (vari_bp * coef_bp) + (vari_bmi * coef_bmi) + (vari_dmpedfunc * coef_dmpedfunc)
print(pred_[0])


# In[48]:


# Sigmoid prob
pred_ = pred_[0]
pred_prop = math.exp(pred_)/(1+math.exp(pred_))
print(pred_prop)


# In[49]:


thershold = 0.5
if pred_prop >= thershold: 
    pred_outcome = 1
    pred_outcome_name = 'ทำนายว่าเป็น DM'
else:
    pred_outcome = 0
    pred_outcome_name = 'ทำนายว่าไม่เป็น DM'
    
print(pred_outcome)
print(pred_outcome_name)


# In[92]:


from sklearn.metrics import roc_curve, roc_auc_score


# In[94]:


# 5. คำนวณความน่าจะเป็น
y_proba = model.predict_proba(X_test)[:, 1] # เลือกความน่าจะเป็นของคลาส 1

# 6. คำนวณค่า FPR, TPR และ Threshold
fpr, tpr, thresholds = roc_curve(y_test, y_proba)

# 7. คำนวณค่า AUC
auc = roc_auc_score(y_test, y_proba)

# 8. พล็อตกราฟ ROC Curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--") # เส้นทแยงมุม
plt.xlabel("False Positive Rate (FPR)")
plt.ylabel("True Positive Rate (TPR)")
plt.title("ROC Curve")
plt.legend()
plt.show()


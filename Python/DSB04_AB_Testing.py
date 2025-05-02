#!/usr/bin/env python
# coding: utf-8

# # A/B Testing in Python

# ## Step 1: Defining Sample Size and Duration Functions

# In[2]:


import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd


# In[10]:


# ฟังก์ชันแรกจะคำนวณจำนวนผู้ใช้ที่คุณต้องการสำหรับการทดลอง
def calculate_sample_size(baseline_conversion, mde, power=0.8, significance_level=0.05):
   expected_conversion = baseline_conversion * (1 + mde)
  
   z_alpha = stats.norm.ppf(1 - significance_level/2)
   z_beta = stats.norm.ppf(power)
  
   sd1 = np.sqrt(baseline_conversion * (1 - baseline_conversion))
   sd2 = np.sqrt(expected_conversion * (1 - expected_conversion))
  
   numerator = (z_alpha * np.sqrt(2 * sd1**2) + z_beta * np.sqrt(sd1**2 + sd2**2))**2
   denominator = (expected_conversion - baseline_conversion)**2
  
   sample_size_per_variant = np.ceil(numerator / denominator)
  
   return int(sample_size_per_variant)


# In[11]:


# ฟังก์ชันที่สองจะนำเอาต์พุตของฟังก์ชันแรกมาใช้ในการคำนวณระยะเวลาการทดลอง 
# โดยพิจารณาจากจำนวนผู้ใช้รายวันที่มีอยู่ (ในกรณีนี้คือปริมาณการเข้าชมเว็บไซต์ของ ตาไมค์ รายวัน)
def calculate_experiment_duration(sample_size_per_variant, daily_visitors, traffic_allocation=0.5):
   visitors_per_variant_per_day = daily_visitors * traffic_allocation / 2
   days_required = np.ceil(sample_size_per_variant / visitors_per_variant_per_day)
  
   return int(days_required)


# ## Step 2: Calculating Sample Sizes For a Range of MDEs

# In[13]:


# Example MDE/sample size tradeoff for ตาไมค์'s website
daily_visitors = 100000 / 30  # Convert monthly to daily visitors
baseline_conversion = 0.05    # ตาไมค์'s current landing page CTR (baseline conv rate of 5%)


# In[14]:


# Create a table of sample sizes for different MDEs
mde_values = [0.01, 0.02, 0.03, 0.05, 0.10, 0.15]  # 1% to 15% change
traffic_allocations = [0.1, 0.5, 1.0]  # 10%, 50%, and 100% of website traffic


# In[15]:


results = []
for mde in mde_values:
   sample_size = calculate_sample_size(baseline_conversion, mde)
  
   for allocation in traffic_allocations:
       duration = calculate_experiment_duration(sample_size, daily_visitors, allocation)
       results.append({
           'MDE': f"{mde*100:.1f}%",
           'Traffic Allocation': f"{allocation*100:.0f}%",
           'Sample Size per Variant': f"{sample_size:,}",
           'Duration (days)': duration
       })

# Create a DataFrame and display the results
df_results = pd.DataFrame(results)
print("Sample Size and Duration for Different MDEs:")
print(df_results)


# ## Step 3: Visualizing the relationship between sample size and MDEs

# In[34]:


# Visualize the relationship between MDE and sample size
plt.figure(figsize=(10, 6))
mde_range = np.arange(0.01, 0.2, 0.01)
sample_sizes = [calculate_sample_size(baseline_conversion, mde) for mde in mde_range]

plt.plot(mde_range * 100, sample_sizes)
plt.xlabel('Minimum Detectable Effect (%)')
plt.ylabel('Required Sample Size per Variant')
plt.title('Required Sample Size vs. MDE')
plt.grid(True)
# plt.yscale('log')
plt.tight_layout()
# plt.savefig('sample_size_vs_mde.png')
plt.show()


# In[18]:


def analyze_ab_test_results(control_visitors, control_conversions,
                          treatment_visitors, treatment_conversions,
                          significance_level=0.05):

   # Calculate conversion rates
   control_rate = control_conversions / control_visitors
   treatment_rate = treatment_conversions / treatment_visitors
  
   # Calculate absolute and relative differences
   absolute_diff = treatment_rate - control_rate
   relative_diff = absolute_diff / control_rate
  
   # Calculate standard errors
   control_se = np.sqrt(control_rate * (1 - control_rate) / control_visitors)
   treatment_se = np.sqrt(treatment_rate * (1 - treatment_rate) / treatment_visitors)
  
   # Calculate z-score
   pooled_se = np.sqrt(control_se**2 + treatment_se**2)
   z_score = absolute_diff / pooled_se
  
   # Calculate p-value (two-tailed test)
   p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
  
   # Calculate confidence interval
   z_critical = stats.norm.ppf(1 - significance_level/2)
   margin_of_error = z_critical * pooled_se
   ci_lower = absolute_diff - margin_of_error
   ci_upper = absolute_diff + margin_of_error
  
   # Determine if result is statistically significant
   is_significant = p_value < significance_level
  
   return {
       'control_rate': control_rate,
       'treatment_rate': treatment_rate,
       'absolute_diff': absolute_diff,
       'relative_diff': relative_diff * 100,  # Convert to percentage
       'margin_of_error': margin_of_error,
       'z_score': z_score,
       'p_value': p_value,
       'ci_lower': ci_lower,
       'ci_upper': ci_upper,
       'is_significant': is_significant
   }


# In[30]:


analyze_ab_test_results(control_visitors = 30000, control_conversions = 1500,
                        treatment_visitors = 30000, treatment_conversions = 1650,
                        significance_level=0.05)


# In[32]:


analyze_ab_test_results(control_visitors = 30000, control_conversions = 6300,
                        treatment_visitors = 30000, treatment_conversions = 11400,
                        significance_level=0.05)


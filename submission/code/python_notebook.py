#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Import data analysis python modules
import pandas as pd
import numpy as np

data_df = pd.read_csv("../../cleandata/data_2022_2023.csv")
men_df = data_df[data_df["Gender"] == "m"]
women_df = data_df[data_df["Gender"] == "w"]
men_df.head()


# In[7]:


women_df.head()


# In[ ]:





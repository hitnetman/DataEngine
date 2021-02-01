#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Action1：求2+4+6+8+...+100的求和，用Python该如何写

# 求从0开始到N的所有偶数之和，定义函数SumEven(N)

def SumEven(N):
    sumeven = 0
    for i in range(0,N+1,2):
        sumeven = sumeven + i
    return sumeven

N = 100
print(SumEven(N))       
        


# In[ ]:





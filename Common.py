import streamlit as st
import time

# 设置登录缓存
bosslogin = False
userlogin = False
workerlogin = False
current_user_id = None
current_user_password = None

# 控制登录失败的函数
def LoginErrorHandler():
    st.error("you have no authority!")
    st.stop() 

# 控制输入无效的函数
def NoValidData():
    st.error("there is no match data") 
    st.stop()

# 控制输入无效的函数
def ISEmpty():
    st.error("there is no data")
    st.stop()


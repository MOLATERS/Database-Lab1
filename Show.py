import streamlit as st
from DataBase import Database
from Worker import WorkLogin
from Boss import BossLogin
from User import UserLogin

def ChooseView(WebViewSelect):
    DB = Database("localhost", 8888, "root", "123456", "LAB1")
    if WebViewSelect == "Boss View":
        BossLogin(DB)
    elif WebViewSelect == "User View":
        UserLogin(DB)
    return


def ShowWeb():
    WebViewSelect = st.sidebar.selectbox("Which view do you want to See", ("Boss View", "User View"))
    ChooseView(WebViewSelect)


if __name__ == "__main__":
    ShowWeb()

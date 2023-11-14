import time
import Common as glb
import streamlit as st
from Common import LoginErrorHandler


def WorkLogin(DB):
    logincontainer = st.empty()

    with logincontainer.container():
        st.title("Please Login to Check Your WORK")
        Worker_info = DB.ReadDB("SELECT employee_id FROM Workers")
        worker_idlist = Worker_info["employee_id"].to_numpy().tolist()
        worker_id = st.text_input("Please give me your worker_id")
        if worker_id:
            worker_id = int(worker_id)

        if st.button("login"):

            if worker_id not in worker_idlist:
                LoginErrorHandler()
            else:
                sql_phrase = f"SELECT employee_name FROM Workers WHERE employee_id = {int(worker_id)}"
                Worker_info = DB.ReadDB(sql_phrase)
                st.success(f"Hello {Worker_info['employee_name'][0]}")
                time.sleep(0.5)
                glb.workerlogin = True

    if glb.workerlogin:
        logincontainer.empty()
        WorkerBehavior(DB, worker_id)


def WorkerBehavior(DB, worker_id):
    st.header("It's Time to work!")
    st.subheader("Please check your work")
    st.write("尚未开发")
    return

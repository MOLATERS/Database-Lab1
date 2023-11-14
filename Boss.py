import time
import Common as glb
import streamlit as st
from Common import LoginErrorHandler

def BossLogin(DB):
    logincontainer = st.empty()
    password = "030121"

    with logincontainer.container():
        st.title("Check whether you are the BOSS")
        text = st.text_input("Enter the password")

        if st.button("login"):

            if text == password:
                st.info("Hello Slater Xu")
                time.sleep(0.5)
                glb.bosslogin = True
            else:
                LoginErrorHandler()

    if glb.bosslogin:
        logincontainer.empty()
        BossBehavior(DB)

    return


def BossCheckOrders(DB):

    # TODO 连接查询，创建视图
    create_view = f""" 
    CREATE OR REPLACE VIEW Checkbusiness(订单号,订单时间,用户名,负责职工姓名,产品名,支付方式) AS                              
    SELECT t1.order_id, t1.order_date, t2.username, t3.employee_name, t4.product_name, t5.payment_type 
    FROM Orders as t1                                                                                  
             LEFT JOIN Users as t2 ON t1.user_id = t2.user_id                                          
             LEFT JOIN Workers as t3 ON t1.employee_id = t3.employee_id                                
             LEFT JOIN Products as t4 ON t1.product_id = t4.product_id                                 
             LEFT JOIN Paymethods as t5 ON t1.payment_id = t5.payment_id                               
    ORDER BY t1.order_id;                                                                                                                                                                                 
    """
    DB.InsertDB(create_view)
    read_view = f"""                                                                                   
    SELECT *                                                                                           
    FROM Checkbusiness                                                                                 
    """
    data = DB.ReadDB(read_view)
    st.table(data)


def BossCheckIncomes(DB):

    # TODO 创建视图，分组查询
    create_view = f"""
    CREATE OR REPLACE VIEW CheckIncomes(日期,单日收入) AS
    SELECT t1.order_date,SUM(t2.product_value)
    FROM Orders AS t1
        LEFT JOIN Products AS t2 ON t1.product_id = t2.product_id
    GROUP BY t1.order_date
    """
    DB.InsertDB(create_view)

    read_view = f"""
    SELECT *
    FROM CheckIncomes
    """
    data = DB.ReadDB(read_view)
    st.table(data)

    read_income = f"""
    SELECT SUM(t1.单日收入) 
    FROM CheckIncomes as t1
    """
    data = DB.ReadDB(read_income).to_numpy().tolist()
    st.info(f"总收入达到了{data[0][0]}")
    return


def BossCheckWorkers(DB):
    worker_id = st.text_input("who you want to focus on?")
    print(worker_id)

    if worker_id:
        show_view = f"""
        SELECT 职工号,职工姓名,负责订单数
        FROM Checkworkers
        WHERE 职工号 = {worker_id}
        """
        print(show_view)
        data = DB.ReadDB(show_view)
        # TODO 错误控制，如果不存在对应的信息就不显示
        if not data.empty:
            st.table(data)
        else:
            st.info("Invalid Input")

    else:
        # TODO 创建视图
        create_view = f"""                                                                                                              
        CREATE OR REPLACE VIEW Checkworkers(职工号,职工姓名,负责订单数) AS
        SELECT t1.employee_id,t1.employee_name,COUNT(*) 
        FROM Workers as t1
            RIGHT JOIN Orders as t2 ON t1.employee_id = t2.employee_id
        GROUP BY t1.employee_id
        ORDER BY COUNT(*);
        """
        DB.InsertDB(create_view)

        read_view = f"""
        SELECT *
        FROM Checkworkers
        """
        data = DB.ReadDB(read_view)

        st.table(data)
    return

def BossLogout():
        glb.bosslogin = False
        st.info("Logout already")


def BossBehavior(DB):
    with st.sidebar:

        if st.button("Logout"):
            BossLogout()

        add_radio = st.radio(
            "What do you want to check?",
            ("Orders", "Workers", "Incomes")
        )
    st.title("Welcome Boss!")
    if add_radio == "Orders":
        st.markdown("## *Please check your orders*")
        BossCheckOrders(DB)
    if add_radio == "Workers":
        st.markdown("## *Please check your Employee's working Status*")
        BossCheckWorkers(DB)
    if add_radio == "Incomes":
        st.markdown("## *Please check your incomes*")
        BossCheckIncomes(DB)

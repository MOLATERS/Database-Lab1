import time
import Common as glb
import streamlit as st
from Common import LoginErrorHandler
from Common import NoValidData
from Common import ISEmpty
import random
import datetime


def UserLogin(DB):
    logincontainer = st.empty()
    with logincontainer.container():
        User_info = DB.ReadDB("SELECT user_id FROM LAB1.Users")
        User_idlist = User_info["user_id"].to_numpy().tolist()
        tables = st.radio(
            "What do you want to do?",
            ("Login", "Signin")
        )
        # 用户登录
        if tables == "Login":
            st.header("Login Table")
            st.write("Welcome to the Slater-Ecommerce-Platform, let's begin the journey")
            user_id = st.text_input("Please give me your id")
            user_password = st.text_input("Your password ")
            if user_id and user_password:
                password = DB.ReadDB(f"SELECT password FROM LAB1.Users WHERE user_id = {user_id}")
                # TODO 错误控制，不能查询主键为空的信息
                if password.empty:
                    print("empty")
                    NoValidData()
                else:
                    password = password.to_numpy().tolist()
                print(password[0][0])
                glb.current_user_id = user_id
                glb.current_user_password = user_password
            print(user_id, user_password)
            if user_id:
                user_id = int(user_id)
            if st.button("login"):
                if user_id not in User_idlist or password[0][0] != user_password:
                    LoginErrorHandler()
                else:
                    glb.userlogin = True
                    success = st.empty()
                    sql_phrase = f"""
                    SELECT username
                    FROM LAB1.Users
                    WHERE user_id = {glb.current_user_id}
                    """
                    print(glb.current_user_id)
                    data = DB.ReadDB(sql_phrase)
                    data = data["username"].to_numpy().tolist()
                    if data:
                        success.info(f"Welcome {data[-1]}")
                    time.sleep(0.5)
                    success.empty()

        # 用户注册
        if tables == "Signin":
            st.header("Signin table")
            st.write("Please enter your infomation")
            add_name = st.text_input("Enter a nickname")
            add_password = st.text_input("Your password")
            add_address = st.text_input("Your address")
            # 添加功能实现
            if st.button("commit"):
                if add_name:
                    InsertUser(DB, add_name, add_password, add_address)
                else:
                    NoValidData()

    # 检查缓存该用户是否登录
    if glb.userlogin:
        logincontainer.empty()
        UserBehavior(DB, glb.current_user_id)


def ShowUserOrders(DB, user_id):
    # TODO 嵌套查询，找到该user_id，再找到user_id对应的username
    sql_phrase = f"""
    SELECT bs.订单号 as 订单号,bs.订单时间 as 下单时间,bs.负责职工姓名 as 对接职工,bs.产品名 as 产品名,bs.支付方式 as 支付方式 
    FROM LAB1.Checkbusiness as bs
    WHERE bs.用户名 IN (
    SELECT username 
    FROM LAB1.Users
    WHERE user_id = {user_id}
    )
    """

    # print(sql_phrase)
    data = DB.ReadDB(sql_phrase)
    st.table(data)


def UserLogout():
    glb.userlogin = False
    glb.current_user_id = None
    glb.current_user_password = None
    st.info("Has Been Logout!")


def UserBehavior(DB, user_id):
    with st.sidebar:
        if st.button("Logout"):
            UserLogout()
        add_radio = st.radio(
            "What Service do you want?",
            ("Orders", "Change your information", "Comments", "ProductsView")
        )
    st.markdown("# Welcome User!")

    if add_radio == "Orders":
        st.markdown("## Please Check Your Orders!")
        st.subheader("Please check your information")
        ShowUserOrders(DB, user_id)

    if add_radio == "Change your information":
        st.markdown("## Here is your information")
        add_radio_2 = st.radio(
            "What do you want to check?",
            ("Change my information", "Delete my information")
        )
        if add_radio_2 == "Change my information":
            st.write("change your information here")
            UserChangeinfo(DB, user_id)
        if add_radio_2 == "Delete my information":
            st.write("delete your information here")
            UserDeleteinfo(DB, user_id)

    if add_radio == "Comments":
        st.markdown("## Your Comment on Products:")
        UserComment(DB, user_id)

    if add_radio == "ProductsView":
        UserShopping(DB, user_id)

    return


def UserShopping(DB, user_id):
    read_categories = f"""
    SELECT category_name, category_id
    FROM LAB1.Category
    """
    data = DB.ReadDB(read_categories)
    category_id = data["category_id"].to_numpy().tolist()
    category_name = data["category_name"].to_numpy().tolist()
    category_num = len(data)
    select = st.sidebar.radio("Category list", tuple(category_name))
    for i in range(0, category_num):
        if select == category_name[i]:
            st.markdown(f'## Product in {category_name[i]}')
            read_sql = f"""
            SELECT * FROM LAB1.Products
            WHERE category_id = {category_id[i]}
            """
            product_data = DB.ReadDB(read_sql)
            if product_data.empty:
                ISEmpty()
            product_name = product_data["product_name"]
            st.table(product_name)

    select_order = st.sidebar.radio("Shopping Behavior", ("Add Orders", "Delete Orders"))
    if select_order == "Add Orders":
        UserAddOrder(DB, user_id)
    if select_order == "Delete Orders":
        UserDeleteOrder(DB, user_id)


def UserAddOrder(DB, user_id):
    st.subheader("Your orders are:")
    read_user = f"""
       SELECT username from LAB1.Users
       WHERE user_id = {user_id}
       """
    name = DB.ReadDB(read_user)
    if name.empty:
        ISEmpty()
    name = name.to_numpy().tolist()
    name = name[0][0]

    checkorders = f"""
       SELECT * from LAB1.Checkbusiness
       WHERE 用户名 = '{name}'
       """
    order_view = DB.ReadDB(checkorders)
    st.table(order_view)
    st.subheader("Add New Orders")
    read_workers = f"""
    SELECT employee_id FROM LAB1.Workers
    """

    data = DB.ReadDB(read_workers).to_numpy().tolist()

    if len(data) > 0:
        employee_id = data[int(random.random()) % len(data)]
        date = datetime.date.today()
        read_payments = f"""
        SELECT * FROM LAB1.Paymethods
        """
        payment_data = DB.ReadDB(read_payments)
        paymethods = payment_data["payment_type"].to_numpy().tolist()
        payment_id = payment_data["payment_id"].to_numpy().tolist()
        select = st.selectbox("Your pay method is", tuple(paymethods))
        payid = -1
        proid = -1
        for i in range(0, len(payment_id)):
            if select == paymethods[i]:
                payid = payment_id[i]
                print("payid", i)
                break
        read_sql = f"""
        SELECT * FROM LAB1.Products
        """
        product_data = DB.ReadDB(read_sql)
        if product_data.empty:
            ISEmpty()
        product_name = product_data["product_name"].to_numpy().tolist()
        product_id = product_data["product_id"].to_numpy().tolist()
        select = st.selectbox("Your wanting product", tuple(product_name))
        for i in range(0, len(product_name)):
            if select == product_name[i]:
                proid = product_id[i]
                print("proid", i)
                break

        if st.button("Commit"):
            if payid != -1 and proid != -1:
                insert_data = f"""
                INSERT INTO LAB1.Orders (order_date, user_id, employee_id, product_id, payment_id)
                    VALUES ('{date}', {user_id}, {employee_id[0]}, {proid}, {payid});
                """
                print(insert_data)
                DB.InsertDB(insert_data)
                st.info("Add data successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                pass
    else:
        ISEmpty()


def UserDeleteOrder(DB, user_id):
    st.subheader("Choose your Order to delete")
    st.subheader("Your current order is:")
    read_orders = f"""
    SELECT * from LAB1.Orders
    WHERE user_id = {user_id}
    """
    order_data = DB.ReadDB(read_orders)

    read_user_delete = f"""
    SELECT username from LAB1.Users
    WHERE user_id = {user_id}
    """
    name = DB.ReadDB(read_user_delete)
    if name.empty:
        ISEmpty()
    name = name.to_numpy().tolist()
    name = name[0][0]

    checkorders = f"""
    SELECT * from LAB1.Checkbusiness
    WHERE 用户名 = '{name}'
    """
    order_view = DB.ReadDB(checkorders)
    st.table(order_view)
    select = st.selectbox("Choose Order id", tuple(order_data["order_id"].to_numpy().tolist()))
    delete_data = f"""
    DELETE FROM LAB1.Orders where order_id = {select}
    """
    if st.button("Delete Now"):
        DB.DeleteDB(delete_data)
        st.info("Delete Successful!")


def UserChangeinfo(DB, user_id):
    st.markdown("### your current information is")
    current_table = st.empty()
    # TODO 连接查询，构建需要的虚拟视图
    read_current = f"""
    SELECT t1.user_id as 账号, t1.username as 用户名, t1.password as 密码, t2.address_details as 地址
    FROM LAB1.Users as t1
        LEFT JOIN LAB1.Address as t2 ON t1.user_id = t2.user_id
    WHERE t1.user_id = {user_id}
    """
    print(read_current)
    data = DB.ReadDB(read_current)
    # TODO 如果没有该成员的信息就不进行删除或者修改操作
    if data.empty:
        glb.userlogin = False
        LoginErrorHandler()
    current_table.table(data)
    new_name = st.text_input("please enter your new name")
    new_password = st.text_input("please enter your new password")
    new_address = st.text_input("please enter your new address")
    if new_password and new_name and new_address and st.button("Commit Changes"):
        # TODO 事务处理，更新
        phrase1 = f"""
        UPDATE LAB1.Users
        SET Users.username = '{new_name}', Users.password = {new_password}
        WHERE Users.user_id = {user_id};
        """
        phrase2 = f"""
        UPDATE LAB1.Address
        SET LAB1.Address.address_details = '{new_address}'
        WHERE LAB1.Address.user_id = {user_id};
        """

        DB.SetTaskDB([phrase1, phrase2])

        read_current = f"""
        SELECT t1.user_id as 账号, t1.username as 用户名, t1.password as 密码, t2.address_details as 地址
        FROM LAB1.Users as t1
            LEFT JOIN LAB1.Address as t2 ON t1.user_id = t2.user_id
        WHERE t1.user_id = {user_id}
        """

        print(read_current)
        data = DB.ReadDB(read_current)
        current_table.table(data)
    pass


def UserDeleteinfo(DB, user_id):
    st.markdown("## Make Sure You want to Delete")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            # TODO 事务处理，删除
            sql_phrase_address = f"DELETE FROM LAB1.Address WHERE Address.user_id = {user_id}"
            sql_phrase_comment = f"DELETE FROM LAB1.Comments WHERE  Comments.user_id = {user_id}"
            sql_phrase_orders = f"DELETE FROM LAB1.Orders WHERE Orders.user_id = {user_id}"
            sql_phrase_user = f"DELETE FROM LAB1.Users WHERE Users.user_id = {user_id}"
            DB.SetTaskDB([sql_phrase_orders, sql_phrase_comment, sql_phrase_address, sql_phrase_user])
            st.info("the record has been deleted, next time you won't have authority")
            st.rerun()
    with col2:
        if st.button("No"):
            st.rerun()


def UserComment(DB, user_id):
    read_phrase = f"""
    SELECT DISTINCT t1.product_id as 产品号, t2.product_name as 产品名 
    FROM LAB1.Orders as t1
        left join LAB1.Products as t2 ON t1.product_id = t2.product_id
    WHERE user_id = {user_id}
    ORDER BY t1.product_id
    """

    data = DB.ReadDB(read_phrase)
    product_id = data["产品号"].to_numpy().tolist()
    print(product_id)
    product_name = data["产品名"].to_numpy().tolist()
    print(product_name)
    product_num = len(product_id)
    print(product_num)
    if product_num == 0:
        ISEmpty()
    for i in range(0, product_num):
        st.subheader(f"Comments on {product_name[i]}")
        read_phrase = f"""
        SELECT comment_text
        FROM LAB1.Comments
        WHERE user_id = {user_id} and product_id = {product_id[i]}
        """
        print(read_phrase)
        data = DB.ReadDB(read_phrase)
        if data.empty:
            st.write("no comments here")
            continue
        st.table(data)

    select = st.selectbox("Which product you want to choose", tuple(product_name[0::]))
    modify = st.sidebar.radio("Want to modify your comments?", ("Add", "Delete"))

    if modify == "Add":
        comments = st.text_input("Input your comment")
        if st.button("Commit"):
            read_phrase = f"""
            SELECT product_id
            FROM LAB1.Products
            WHERE product_name = '{select}'
            ORDER BY product_id
            """
            data = DB.ReadDB(read_phrase)
            if data.empty:
                ISEmpty()
            data = data.to_numpy().tolist()[0][0]
            add_comment = f"""
            INSERT INTO LAB1.Comments (user_id, product_id, comment_text)
            VALUES ({user_id}, {data}, '{comments}');
            """
            DB.InsertDB(add_comment)
            st.info("the data has been added")
            time.sleep(1)
            st.rerun()

    if modify == "Delete":
        st.subheader("Make sure you want to delete all comments")
        if st.button("Commit"):
            read_phrase = f"""
            SELECT product_id
            FROM LAB1.Products
            WHERE product_name = '{select}'
            """
            data = DB.ReadDB(read_phrase)
            if data.empty:
                ISEmpty()
            data = data.to_numpy().tolist()[0][0]

            delete = f"""
            DELETE
            FROM LAB1.Comments
            WHERE user_id = {user_id} and product_id = {data};
            """
            DB.DeleteDB(delete)
            st.info(f"the comments on {select} are all deleted")
            time.sleep(1)
            st.rerun()


def InsertUser(DB, username, password, address):
    Insert = st.empty()
    # TODO 插入操作
    sql_phrase = f"""
    INSERT INTO LAB1.Users (username,password) 
    VALUES('{username}','{password}');
    """
    st.echo(sql_phrase)

    print(sql_phrase)
    DB.InsertDB(sql_phrase)

    read_phrase = f"""
    SELECT user_id 
    FROM LAB1.Users
    WHERE username = '{username}' and password = '{password}'
    """

    st.echo(read_phrase)
    print(read_phrase)
    data = DB.ReadDB(read_phrase).to_numpy().tolist()
    user_id = data[-1]

    address = f"""
    INSERT INTO LAB1.Address (user_id,address_details)
    VALUES({user_id[0]},'{address}');
    """

    st.echo(address)
    print(address)
    DB.InsertDB(address)

    Insert.info("Inset Success!")
    st.info(f"Your current id is: {user_id[0]}")
    time.sleep(1)
    Insert.empty()

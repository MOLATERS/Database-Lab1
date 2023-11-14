import pymysql
import pandas as pd
from sqlalchemy import create_engine


class Database():

    def __str__(self):
        return f'[INFO] host:{self.host},port:{self.port},user:{self.user},password:{self.password},database:{self.database},connection:{self.DB_handler}'

    def ConnectDB(self):
        # 建立数据库连接
        connection_handler = pymysql.connect(
            host=self.host,  # 主机名或 IP 地址
            port=self.port,
            user=self.user,  # 用户名
            password=self.password,  # 密码
            database=self.database  # 数据库名称
        )
        # 创建游标对象
        cursor = connection_handler.cursor()
        return cursor, connection_handler

    def __init__(self, host, port, user, password, database) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.cursor, self.DB_handler = self.ConnectDB()

    def SetTaskDB(self, details):
        size = len(details)
        count = 0
        try:
            while (count < size):
                self.cursor.execute(details[count])
                print(details[count])
                print(f"[INFO] task {count} done")
                count = count + 1
            print(f"[INFO] {size} task has been done")
            self.DB_handler.commit()
            return
        except:
            print(f"[ERRO] task error at the line {count}")
            self.DB_handler.rollback()
            self.DB_handler.commit()

    def CloseDB(self):
        self.cursor.close()
        self.DB_handler.close()
        return

    def InsertDB(self, sql_phrase):
        try:
            self.cursor.execute(sql_phrase)
            self.DB_handler.commit()
            print("[INFO] insert commit success!")
            return True
        except:
            self.DB_handler.rollback()
            self.DB_handler.commit()
            print("[INFO] insert commit failed!")
            return False

    def ReadDB(self, sql_phrase):
        try:
            conn = create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{str(self.port)}/{self.database}?charset=utf8')
        except:
            print("[ERRO] connection failed!")
            return None
        data = pd.read_sql(sql_phrase, conn)
        print("[INFO] read from database success!")
        if data.empty:
            print("[INFO] it's empty")
        return data

    def DeleteDB(self, sql_phrase):
        try:
            self.cursor.execute(sql_phrase)
            self.DB_handler.commit()
            print(f"[INFO] delete commit {sql_phrase} success!")
        except:
            self.DB_handler.rollback()
            self.DB_handler.commit()
            print(f"[INFO] delete commit {sql_phrase} failed!")
        return

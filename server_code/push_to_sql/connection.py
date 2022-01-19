import pymssql #引入pymssql模块
import time

def conn():
    connect = pymssql.connect('Your mssql host', 'Your mssql user', 'Your mssql password', 'Your mssql database name') #服务器名,账户,密码,数据库名
    if connect:
        print("connect successfully!")
    return connect

if __name__ == "__main__":


    pass

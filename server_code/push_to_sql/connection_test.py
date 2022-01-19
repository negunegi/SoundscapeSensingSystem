import pymssql 


def conn():
    connect = pymssql.connect('Your mssql host', 'Your mssql user', 'Your mssql password', 'Your mssql database name') #服务器名,账户,密码,数据库名
    if connect:
        print("connect successfully!")
    return connect


if __name__ == '__main__':
    conn = conn()
    if conn:
        print("connect successfully!")
    cursor = conn.cursor()  
    sql = "select * from iue001"
    cursor.execute(sql)   
    row = cursor.fetchone()  
    while row:              
        print("id=%s, dev_id=%s" % (row[0],row[1]))  
        row = cursor.fetchone()

    cursor.close()   
    conn.close()
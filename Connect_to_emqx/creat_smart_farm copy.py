from pymysql import Connection

con = None
try:
    # 连接数据库
    con = Connection(
            host='cloud-5plus.dxh-wds.top',
            user='root',
            password='wdsshy0320',
            database='smart_farm',  # 指定数据库
        )
    print("连接成功")
    print(con)


    sql = """
    CREATE TABLE Smart_factory_status(
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature FLOAT,
    humidness FLOAT,
    illumination FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """

    #使用游标对象执行sql语句
    con.cursor().execute(sql)


except Exception as e:
    print("连接失败")
    print(e)
finally:
    con.close()

import paho.mqtt.client as mqtt
import json
from pymysql import Connection

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('test_topic')

# 消息接收回调
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # 解析 JSON 数据
    data = json.loads(msg.payload)
    
    # 从解析的数据中提取温度、湿度和照明度
    temperature = data.get("temperature", "")
    humidness = data.get("humidness", "")
    illumination = data.get("illumination", "")
    
    # 将数据插入到数据库
    try:
        # 连接数据库
        con = Connection(
            host='cloud-5plus.dxh-wds.top',
            user='root',
            password='wdsshy0320',
            database='smart_farm',  # 指定数据库
        )
        print("数据库连接成功")

        # 插入数据的 SQL 语句
        sql = """
        INSERT INTO Smart_factory_status(temperature, humidness, 照明度)
        VALUES(%s, %s, %s)
        """
        # 使用游标对象执行 SQL 语句并获取结果
        with con.cursor() as cursor:
            cursor.execute(sql, (temperature, humidness, illumination))
            # 插入数据后需要提交
            con.commit()
            print("数据插入成功")
    except Exception as e:
        print("数据库连接失败")
        print(e)
    finally:
        if con:
            con.close()

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立连接
client.connect('cloud-5plus.dxh-wds.top', 1883, 60)
# 发布消息
client.publish('test', payload='Hello World', qos=0)

client.loop_forever()  # 保持连接
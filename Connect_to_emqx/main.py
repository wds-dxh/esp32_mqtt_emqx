import json
from pymysql import Connection
import paho.mqtt.client as mqtt     # pip install paho-mqtt

class MqttToMySQL:
    def __init__(self, mqtt_host, mqtt_port, mqtt_topic, mqtt_username, mqtt_password, db_host, db_user, db_password, db_name):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

        self.client = mqtt.Client()
        self.client.username_pw_set(username=mqtt_username, password=mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.con = None
        self.connect_db()

    def connect_db(self):
        try:
            self.con = Connection(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            print("数据库连接成功")
        except Exception as e:
            print("数据库连接失败")
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker {self.mqtt_host}:{self.mqtt_port} with result code {rc}")
            client.subscribe(self.mqtt_topic)
        else:
            print(f"Failed to connect to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
        try:
            data = json.loads(msg.payload)
            temperature = data.get("temperature", "")
            humidness = data.get("humidness", "")
            illumination = data.get("illumination", "")

            sql = """
            INSERT INTO Smart_factory_status(temperature, humidness, illumination, timestamp)
            VALUES(%s, %s, %s, CURRENT_TIMESTAMP)
            """
            with self.con.cursor() as cursor:
                cursor.execute(sql, (temperature, humidness, illumination))
                self.con.commit()
                print("数据插入成功")
        except Exception as e:
            print("插入数据失败")
            print(e)

    def start(self):
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("Disconnecting MQTT client")
            self.client.disconnect()

# 使用示例
if __name__ == "__main__":
    mqtt_host = 'vps.dxh-wds.top'
    mqtt_port = 1883
    mqtt_topic = 'smart_farm_status'
    mqtt_username = 'wds'
    mqtt_password = 'wdsshy0320'
    
    db_host = 'vps.dxh-wds.top'
    db_user = 'root'
    db_password = 'wdsshy0320'
    db_name = 'smart_farm'

    mqtt_to_mysql = MqttToMySQL(mqtt_host, mqtt_port, mqtt_topic, mqtt_username, mqtt_password, db_host, db_user, db_password, db_name)
    mqtt_to_mysql.start()

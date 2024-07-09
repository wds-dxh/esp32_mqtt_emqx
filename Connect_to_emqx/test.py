'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-07-08 08:44:17
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-07-08 08:45:34
FilePath: \Connect_to_emqx\test.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import paho.mqtt.client as mqtt

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('test_topic')

# 消息接收回调
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# 指定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 建立连接
client.connect('cloud-5plus.dxh-wds.top', 1883, 60)
# 发布消息
client.publish('test',payload='Hello World',qos=0)

client.loop_forever()   # 保持连接
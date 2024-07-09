#include <Arduino.h>
#include "MQTT_EMQX.h"

// WiFi和MQTT参数
const char *ssid = "wds";
const char *password = "wds666666";
const char *mqtt_broker = "vps.dxh-wds.top";
const char *topic = "esp32/test";
const char *mqtt_username = "wds";
const char *mqtt_password = "wdsshy0320";
const int mqtt_port = 1883;
const char *topic_pub = "esp32/test1";

// 创建Mqtt_emqx对象
Mqtt_emqx mqtt(ssid, password, mqtt_broker, topic, mqtt_username, mqtt_password, mqtt_port);

void setup() {
    // 初始化串口
    Serial.begin(115200);
    
    // 连接WiFi和MQTT
    mqtt.connect();

    mqtt.publish(topic_pub, "Hello, EMQ X!");
}

void loop() {
    // 保持MQTT连接
    mqtt.loop();
}

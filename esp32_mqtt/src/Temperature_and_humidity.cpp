#include <HardwareSerial.h>

class TempHumiditySensor {
private:
    HardwareSerial& serial;
    int rxPin, txPin;
    uint8_t deviceAddress;

    // CRC计算函数
    uint16_t calculateCRC(const uint8_t* data, uint8_t length) {
        uint16_t crc = 0xFFFF;
        for (uint8_t i = 0; i < length; i++) {
            crc ^= data[i];
            for (uint8_t j = 0; j < 8; j++) {
                if (crc & 0x0001) {
                    crc >>= 1;
                    crc ^= 0xA001;
                } else {
                    crc >>= 1;
                }
            }
        }
        return crc;
    }

    // 发送读取请求函数
    void sendRequest(uint8_t functionCode, uint16_t startAddress, uint16_t numRegisters) {
        uint8_t request[] = {
            deviceAddress,
            functionCode,
            (startAddress >> 8) & 0xFF,
            startAddress & 0xFF,
            (numRegisters >> 8) & 0xFF,
            numRegisters & 0xFF
        };
        uint16_t crc = calculateCRC(request, 6);
        serial.write(request, 6);
        serial.write(crc & 0xFF);
        serial.write((crc >> 8) & 0xFF);
    }

    // 读取响应数据函数
    bool readResponse(uint8_t* buffer, size_t length) {
        size_t bytesRead = 0;
        uint32_t startTime = millis();
        while (bytesRead < length && (millis() - startTime) < 1000) { // Timeout of 1 second
            if (serial.available()) {
                buffer[bytesRead++] = serial.read();
            }
        }
        return bytesRead == length;
    }

public:
    // 构造函数
    TempHumiditySensor(HardwareSerial& serialPort, int rx, int tx, uint8_t address)
        : serial(serialPort), rxPin(rx), txPin(tx), deviceAddress(address) {}

    // 初始化串口
    void begin(int baudRate) {
        serial.begin(baudRate, SERIAL_8N1, rxPin, txPin);
    }

    // 读取温湿度函数
    bool readTemperatureHumidity(float& temperature, float& humidity) {
        sendRequest(0x03, 0x0000, 0x0002); // Function 3, start at 0x0000, read 2 registers

        uint8_t response[9]; // Address, function, byte count, 2 humidity bytes, 2 temperature bytes, 2 CRC bytes
        if (readResponse(response, 9)) {
            uint16_t receivedCRC = response[7] | (response[8] << 8);
            if (calculateCRC(response, 7) == receivedCRC) {
                uint16_t rawHumidity = response[3] | (response[4] << 8);
                uint16_t rawTemperature = response[5] | (response[6] << 8);

                humidity = rawHumidity / 10.0;
                temperature = (int16_t)rawTemperature / 10.0; // Cast to int16_t to handle negative temperatures

                return true;
            }
        }
        return false;
    }
};

void setup() {
    Serial.begin(115200);
    TempHumiditySensor sensor(Serial1, 16, 17, 0x01); // RX, TX, device address
    sensor.begin(4800);

    float temperature, humidity;
    if (sensor.readTemperatureHumidity(temperature, humidity)) {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print(" °C, Humidity: ");
        Serial.print(humidity);
        Serial.println(" %RH");
    } else {
        Serial.println("Failed to read data from sensor");
    }
}

void loop() {
    // Add your code here
}

import paho.mqtt.client as mqtt
import json
import subprocess

# Настройки
BROKER = "broker.hivemq.com"  # Публичный MQTT-брокер для тестов
PORT = 1883
TOPIC = "nariman079i/grafana/topic"
CLIENT_ID = "python_client"

# Явно указываем версию API (исправляет ошибку)
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
    client_id=CLIENT_ID
)

# Функция, вызываемая при подключении к брокеру
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Подключено к MQTT-брокеру")
        client.subscribe(TOPIC)
    else:
        print(f"Ошибка подключения: {rc}")

# Функция, вызываемая при получении сообщения
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        for alert in payload.get("alerts", []):
            if alert.get("status") == "firing":
                summary = alert["annotations"]["summary"]
                description = alert["annotations"]["description"]

                # Отправляем уведомление
                subprocess.run([
                    "notify-send",
                    "-u", "critical",
                    "Grafana Alert",
                    f"{summary}\n\n{description}"
                ])
    except Exception as e:
        print("Ошибка обработки сообщения:", e)
    print(f"Получено сообщение: {msg.payload.decode()} по теме {msg.topic}")

# Функция, вызываемая при публикации сообщения
def on_publish(client, userdata, mid):
    print("Сообщение отправлено")

# Назначение обработчиков
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Подключение к брокеру
client.connect(BROKER, PORT, 60)

# Запуск цикла обработки сообщений
client.loop_start()

# Отправка сообщения
client.publish(TOPIC, "Привет, MQTT!")

# Ожидание ввода для завершения
input("Нажмите Enter для выхода...\n")
client.loop_stop()
client.disconnect()
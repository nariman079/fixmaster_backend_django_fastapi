import redis
import threading
import time
import json

client = redis.Redis(host='localhost', port=6379, db=0)

def publish_messages():
    """Функция для публикации сообщений в Redis канал"""
    channel = 'test_channel'
    counter = 0
    while True:
        message = {
            'id': counter,
            'text': f'Сообщение номер {counter}',
            'timestamp': time.time()
        }
        client.publish(channel, json.dumps(message))
        print(f"Опубликовано: {message}")
        counter += 1
        time.sleep(5)  # Публикуем сообщение каждые 5 секунд

def subscribe_messages():
    """Функция для подписки на сообщения из Redis канала и их вывода"""
    pubsub = client.pubsub()
    channel = 'test_channel'
    pubsub.subscribe(channel)
    
    print(f"Подписка на канал: {channel}")
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            print(f"Получено сообщение: {data}")

def start_main_loop():
    """Запуск pub и sub функционала в отдельных потоках"""
    # Создаем поток для публикации сообщений
    publish_thread = threading.Thread(target=publish_messages, daemon=True)
    publish_thread.start()
    
    # Создаем поток для подписки на сообщения
    subscribe_thread = threading.Thread(target=subscribe_messages, daemon=True)
    subscribe_thread.start()
    
    # Основной цикл
    while True:
        time.sleep(4)

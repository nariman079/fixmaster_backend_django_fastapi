#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функционала redis_connector
"""

import sys
import os
import time

# Добавляем путь к директории с redis_connector.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import redis_connector

if __name__ == "__main__":
    print("Запуск теста Redis pub/sub...")
    print("Для остановки нажмите Ctrl+C")
    
    try:
        # Запускаем основной цикл
        redis_connector.start_main_loop()
    except KeyboardInterrupt:
        print("\nТест остановлен пользователем")
        sys.exit(0)

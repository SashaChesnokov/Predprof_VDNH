# Оптимальные маршруты по ВДНХ

![ВДНХ](https://example.com/path/to/image.jpg) <!-- (опционально) -->

Веб-приложение для поиска кратчайших маршрутов между объектами на территории ВДНХ с использованием алгоритма Дейкстры.

## Основные возможности

- Поиск оптимального пешего маршрута между любыми двумя точками ВДНХ
- Учет времени и расстояния при построении маршрута
- Интерактивная карта с отображением маршрута
- Информация о ключевых объектах ВДНХ

## Технологии

- Python 3.x
- Django 4.x
- Алгоритм Дейкстры для поиска кратчайшего пути
- PostgreSQL/MySQL/SQLite (укажите вашу БД)
- Leaflet/OpenLayers (если используется, опционально)
- Docker (опционально)

## Установка и запуск

### Предварительные требования

- Установленный Python 3.x
- Установленный pip

### Инструкция по установке

1. Клонируйте репозиторий:
```bash
    git clone https://github.com/yourusername/vdnh-router.git
    cd vdnh-router
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate     # Windows
    pip install django
    python manage.py migrate
    python manage.py runserver
```

# Library Management System

Веб-приложение для управления библиотекой, разработанное в рамках курсовой работы.

## Возможности системы

- регистрация и авторизация пользователей;
- просмотр каталога книг;
- бронирование книг;
- просмотр списка бронирований;
- управление каталогом книг;
- REST API для взаимодействия клиентской и серверной частей.

## Используемые технологии

### Backend
- Python
- Django
- Django REST Framework
- PostgreSQL

### Frontend
- Vue.js
- Pinia
- Axios

### Дополнительно
- Docker
- Git
- GitHub

## Запуск backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

## REST API

```text
POST   /api/auth/register
POST   /api/auth/login

GET    /api/books/
GET    /api/books/{id}

POST   /api/reservations/
GET    /api/reservations/me
```

## GitHub

Репозиторий проекта:  
https://github.com/AnnaGS05/library-management-system

## Автор

Головина Анна Сергеевна  
ИКБО-12-23

# Тестовое задание.

## Описание задачи:
- Необходимо реализовать сервис, который будет принимать на вход excel файл, парсить его и записывать в БД.
- Необходимо реализовать эндпоинт, который будет возвращать данные из БД в виде файла 
- Необходимо реализовать эндпоинт, возвращающий json для построения столбчатой диаграммы суммарных значений всех проектов по датам конкретного года. Можно подавать версию файла, год и тип значений (план или факт).

## Ссылка на репозиторий с заданием:
https://github.com/R0v4n/junior_task_1/tree/master

## Запуск:
`docker compose up --build`

## Выполнение:
- [x] DDL для создания таблиц БД (SQLAlchemy, postgresql, alembic)
- [x] скрипт для парсинга из excel файла и запись в БД (pandas, sqlalchemy)
- [x] API для загрузки файла
- [x] API для получения файла
- [x] API для получения json 
- [x] упаковка в docker
- [x] swagger (FastAPI)
- [x] Наличие конфигурации, сборки и описания приложения
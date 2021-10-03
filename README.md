# todo-api

# Установка
```
git clone https://github.com/nurlybek-dev/todo-api.git
cd todo-api
docker-compose up -d --build
docker-compose exec web python manage.py migrate
```

Так же можно создать группы и тестовых пользователей
```
docker-compose exec web python manage.py loaddata data.json
```

Создадутся группы __admin__ и __employee__.
Пользователи:
```
Superuser
username: admin
password: admin
groups: admin
----------------
username: employee
password: employee
groups: employee
```

# Использование
Использовался ModelViewSet, так что все роуты доступны по префиксу __/tasks/__
```
/tasks/ - GET
/tasks/ - POST
/tasks/<id>/ - GET, DELETE
/tasks/<id>/ - PUT, PATCH

Для POST, PUT, PATCH тело:
{
  "title": "Task title",
  "description": "Task descrtipion",
  "priority": "",
  "deadline": ""
}
```

# Запуск тестов
```
docker-compose exec web pytest
```

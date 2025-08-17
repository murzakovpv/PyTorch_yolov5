brew install postgresql@15


export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/postgresql@15/lib"
export CPPFLAGS="-I/opt/homebrew/opt/postgresql@15/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/postgresql@15/lib/pkgconfig"
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/postgresql@15/lib"


создать такую базу, таблицу и юзера: 
"DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_count
DB_USER=admin
DB_PASSWORD=secret"


Полная инструкция по созданию базы данных, таблицы и пользователя в PostgreSQL согласно вашим требованиям:

1. Подключитесь к PostgreSQL (используя вашего текущего пользователя):
psql postgres

2. Создайте нового пользователя 'admin' с паролем 'secret':
CREATE ROLE admin WITH LOGIN PASSWORD 'secret' SUPERUSER;

3. Создайте базу данных 'people_count':
CREATE DATABASE people_count WITH OWNER admin;

4. Подключитесь к новой базе данных под пользователем admin:
psql -U admin -d people_count

5. Создайте таблицу (пример структуры):
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

6. Настройте привилегии (если нужно ограничить права):
GRANT ALL PRIVILEGES ON DATABASE people_count TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

7. Проверьте подключение с новыми параметрами:
psql -h localhost -p 5432 -U admin -d people_count -W
(Введите пароль 'secret' при запросе)

запрос - проверка данных в таблице
SELECT * FROM people_counts;
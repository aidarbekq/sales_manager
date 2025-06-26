# 📊 Sales Manager

**CRM-система** на Django для управления клиентами, товарами, заказами и генерации аналитических отчётов в формате PDF.

---

## 🚀 Функциональность

* 👤 Управление клиентами (CRUD)
* 📦 Управление продуктами (CRUD, складские остатки)
* 📑 Оформление заказов (с подсчётом итогов и статусами)
* 📄 Генерация PDF‑отчёта с аналитикой (Jinja2 + WeasyPrint)
* 🔐 JWT‑аутентификация (SimpleJWT)
* 🌍 Документация OpenAPI (Swagger / drf‑spectacular)

---

## 🧱 Стек технологий

| Слой    | Технологии                               |
| ------- | ---------------------------------------- |
| Backend | **Django 5**, **Django REST Framework**  |
| DB      | **PostgreSQL 15**                        |
| PDF     | **WeasyPrint 63**                        |
| Docs    | **drf‑spectacular** + Swagger‑UI         |
| Auth    | **djangorestframework‑simplejwt**        |
| Dev Ops | **Docker**, **Docker Compose**, Gunicorn |

---

## ⚙️ Быстрый старт (Docker)

1. Склонируйте репозиторий и скопируйте файл окружения:

   ```bash
   git clone https://github.com/your‑org/sales_manager.git
   cd sales_manager
   cp .env.example .env
   ```

2. Запустите контейнеры:

   ```bash
   docker compose up --build
   ```

3. Откройте в браузере:

   * **API** `http://localhost:8000/api/`
   * **Админка** `http://localhost:8000/admin/`

4. Создайте суперпользователя (в новой вкладке терминала):

   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

---

## 📂 Структура проекта

```
sales_manager/
├── crm/                # Приложение CRM (модели, сериализаторы, viewsets)
├── sales_manager/      # Конфигурация проекта Django
├── templates/          # Jinja2‑шаблоны (PDF‑отчёты)
├── staticfiles/        # Собранная статика
├── Dockerfile          # Docker‑образ backend’а
├── docker-compose.yml  # Compose‑конфигурация
├── entrypoint.sh       # Скрипт запуска внутри контейнера
└── requirements.txt    # Зависимости Python
```

---

## 🖥️ Работа локально (без Docker)

> Требуются Python 3.12+ и PostgreSQL 15.

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
---

## 🔑 Переменные окружения (.env)

| Имя                 | По умолчанию                                        | Назначение                                        |
|---------------------| --------------------------------------------------- |---------------------------------------------------|
| `DJANGO_SECRET_KEY` | `changeme`                                          | Секретный ключ Django                             |
| `DEBUG`             | `0`                                                 | Включение режима отладки                          |
| `POSTGRES_DB`       | `sales_manager`                                     | Имя базы данных                                   |
| `POSTGRES_USER`     | `sales`                                             | Пользователь БД                                   |
| `POSTGRES_PASSWORD` | `sales_pass`                                        | Пароль БД                                         |
| `DB_HOST`           | `db`                                                | Хост БД, используется в entrypoint.sh             |
| `DB_PORT`           | `5432`                                              | Порт БД , используется в entrypoint.sh            |
| `DATABASE_URL`      | `postgres://sales:sales_pass@db:5432/sales_manager` | URL для подключения к БД, используется в settings |

Пример `.env`:

```env
SECRET_KEY=django-insecure-5^eb-@-z6=bm0iyete9ltg!#(9*e@say5k4mx57p4#jkk)hs4z
DEBUG=1
POSTGRES_USER=sales
POSTGRES_PASSWORD=sup3rsecret
POSTGRES_DB=sales_manager
DATABASE_URL=postgres://sales:sup3rsecret@db:5432/sales_manager
DB_HOST=db
DB_PORT=5432
```

---

## 📘 Документация API

* **Swagger‑UI**:  [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
* **ReDoc**:        [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

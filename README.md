# 📊 Sales Manager

**CRM-система** на Django для управления клиентами, товарами, заказами и генерации аналитических отчётов в формате PDF.

---
## 📎 Пример отчета

В директории [`examples/`](./examples/) находятся демонстрационные материалы:

- [`sales_2025-06-01_2025-06-30.pdf`](./examples/sales_2025-06-01_2025-06-30.pdf) — пример сгенерированного отчёта о продажах в формате PDF.



## 🎥 Демонстрация работы как покупается товар, смена статуса и создание отчета 

📺 Видео-демо работы через Swagger:

▶️ [Смотреть на Streamable](https://streamable.com/vtywbb)

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
git clone https://github.com/aidarbekq/sales_manager.git
```
```bash
cd sales_manager
```
```bash
cp .env.example .env
```


2. Запустите контейнеры:

```bash
docker compose up --build
```
> 💡 Подсказки по Docker Compose:
>
> - Если вы используете docker-compose, то используйте `docker-compose up --build` команду.
> - Запуск с пересборкой: `docker-compose up --build`
> - Фоновый запуск: `docker-compose up -d`
> - Остановка: `docker compose down`
> - Остановка + удаление данных: `docker compose down -v`



3. Откройте в браузере:

   * **API** `http://localhost:8000/api/`
   * **Документация Swagger** `http://localhost:8000/api/docs/`
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
```
```bash
pip install -r requirements.txt
```
```bash
cp .env.example .env
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
---

## 🔑 Переменные окружения (.env)

| Имя                 | По умолчанию                                        | Назначение                                       |
|---------------------| --------------------------------------------------- |--------------------------------------------------|
| `DJANGO_SECRET_KEY` | `changeme`                                          | Секретный ключ Django                            |
| `DEBUG`             | `0`                                                 | Включение режима отладки                         |
| `POSTGRES_DB`       | `sales_manager`                                     | Имя базы данных                                  |
| `POSTGRES_USER`     | `sales`                                             | Пользователь БД                                  |
| `POSTGRES_PASSWORD` | `sales_pass`                                        | Пароль БД                                        |
| `DB_HOST`           | `db`                                                | Хост БД, используется в entrypoint.sh            |
| `DB_PORT`           | `5432`                                              | Порт БД , используется в entrypoint.sh           |
| `DATABASE_URL`      | `postgres://sales:sales_pass@db:5432/sales_manager` | URL для подключения к БД, используется в settings |

Рабочий пример `.env`:

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


## 🔍 Примеры API-запросов

### 📟 Получить список заказов

```bash
curl -H "Authorization: Bearer <ваш_токен>" http://localhost:8000/api/orders/
```

📃 Пример ответа:

```json
[
  {
    "id": 1,
    "customer": 2,
    "customer_detail": {
      "id": 2,
      "full_name": "Алия Асанова",
      "email": "aliya@example.com",
      "company_name": "ТОО Пример",
      "phone": "+996700123456",
      "created_at": "2025-06-01T12:34:56Z"
    },
    "status": "confirmed",
    "created_at": "2025-06-26T09:10:11Z",
    "discount_percent": "5.00",
    "tax_percent": "12.00",
    "shipping_cost": "0.00",
    "total": "18000.00",
    "items": [
      {
        "id": 1,
        "product": 3,
        "product_detail": {
          "id": 3,
          "name": "Принтер Canon",
          "description": "МФУ с Wi-Fi",
          "price": "15000.00",
          "stock_quantity": 10,
          "is_active": true
        },
        "quantity": 1,
        "subtotal": "15000.00"
      }
    ]
  }
]
```

---

### 📅 Создать заказ

```bash
curl -X POST http://localhost:8000/api/orders/ \
     -H "Authorization: Bearer <ваш_токен>" \
     -H "Content-Type: application/json" \
     -d '{
  "customer": 2,
  "discount_percent": "5.00",
  "tax_percent": "12.00",
  "items": [
    { "product": 3, "quantity": 2 },
    { "product": 4, "quantity": 1 }
  ]
}'
```

---

### 🔄 Изменить статус заказа

```bash
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
     -H "Authorization: Bearer <ваш_токен>" \
     -H "Content-Type: application/json" \
     -d '{ "status": "confirmed" }'
```

---

### 📄 Скачать PDF-отчёт о продажах

```bash
curl -X GET "http://localhost:8000/api/reports/sales/?start=2025-06-01&end=2025-06-30" \
     -H "Authorization: Bearer <ваш_токен>" \
     --output sales_report.pdf
```

Ответ: скачивается PDF-файл с отчётом.

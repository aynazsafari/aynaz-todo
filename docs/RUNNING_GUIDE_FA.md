# راهنمای اجرای پروژه (قدم‌به‌قدم و خیلی مبتدی)

این راهنما طوری نوشته شده که اگر «هیچ تجربه‌ای ندارید» هم بتوانید پروژه را اجرا کنید.

---

## A) ویندوز (Windows) — راه‌اندازی سریع

### 1) نصب Docker Desktop
1. Docker Desktop را نصب کنید.
2. Docker Desktop را اجرا کنید.
3. صبر کنید وضعیت **Running** شود.

> اگر پیام خطا درباره WSL2 گرفتید، معمولاً باید WSL2 را فعال کنید. (در اکثر سیستم‌ها Docker خودش راهنمایی می‌کند.)

### 2) Extract کردن فایل ZIP
1. روی فایل ZIP راست‌کلیک کنید.
2. گزینه **Extract All...** را بزنید.
3. یک فولدر مثل `todo-fullstack` ساخته می‌شود.

### 3) باز کردن ترمینال داخل پوشه پروژه
1. وارد فولدر پروژه شوید.
2. روی فضای خالی فولدر **Shift + Right Click** کنید.
3. گزینه **Open PowerShell window here** یا **Open in Terminal** را بزنید.

### 4) اجرای پروژه
داخل ترمینال:
```bash
docker compose up --build
```

### 5) باز کردن برنامه
- فرانت‌اند: http://localhost:3000  
- بک‌اند (Swagger): http://localhost:8000/docs

### 6) خاموش کردن
در ترمینال: **Ctrl + C**  
بعد:
```bash
docker compose down
```

---

## B) مک (macOS)

1) Docker Desktop را نصب و اجرا کنید  
2) فایل ZIP را Double Click کنید تا Extract شود  
3) Terminal را باز کنید و بروید داخل پوشه پروژه:
```bash
cd ~/Downloads/todo-fullstack
```
4) اجرا:
```bash
docker compose up --build
```
5) باز کردن:
- http://localhost:3000
- http://localhost:8000/docs

---

## C) خطاهای رایج

### 1) `docker: command not found`
Docker نصب نیست یا PATH درست نیست.
- Docker Desktop را نصب و اجرا کنید.

### 2) `Cannot connect to the Docker daemon`
Docker Desktop هنوز Running نشده.
- Docker Desktop را باز کنید و صبر کنید.

### 3) `port is already allocated`
یکی از پورت‌ها اشغال است (مثلاً 3000 یا 8000).
- برنامه‌های دیگر را ببندید یا پورت‌ها را تغییر دهید.

---

اگر اجرا کردید ولی صفحه بالا نیامد، از ترمینال یک اسکرین‌شات بگیرید یا متن خطا را کپی کنید؛ دقیق راهنمایی می‌کنم.

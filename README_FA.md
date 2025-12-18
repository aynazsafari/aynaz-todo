# نسخه MongoDB برای Backend پروژه To‑Do

این پروژه بک‌اند FastAPI را روی **MongoDB** اجرا می‌کند و API CRUD را حفظ می‌کند.

## اجرا (Docker)
داخل پوشه اصلی پروژه:

```powershell
docker compose up --build
```

سپس:
- Swagger: http://localhost:8000/docs
- API لیست: http://localhost:8000/api/v1/tasks

## نکات
- CRUD کامل (Create/Read/Update/Delete)
- Soft delete (deleted_at)
- Pagination (limit/offset/total)
- CORS برای فرانت روی 5173/3000 فعال است

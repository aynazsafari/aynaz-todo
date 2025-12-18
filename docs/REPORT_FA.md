# گزارش نهایی پروژه مهندسی نرم‌افزار
## سامانه مدیریت وظایف (To‑Do) — Full‑Stack (Frontend + Backend)

**نام پروژه:** PinkLav To‑Do  
**هدف:** پیاده‌سازی کامل چرخه حیات وظیفه (CRUD) در Backend + یک Frontend کاربرپسند برای استفاده عملی  
**الزامات اجباری:** Git (feature branch + PR) و Docker (Dockerfile + Compose)  

---

## 1) مقدمه
دامنه «To‑Do» با وجود سادگی، برای ارزیابی مفاهیم کلیدی مهندسی نرم‌افزار مناسب است: مهندسی نیازمندی‌ها، طراحی API، مدل‌سازی دامنه، معماری لایه‌ای، تست‌پذیری، کنترل نسخه و استقرار تکرارپذیر.

---

## 2) تعریف مسئله
### 2.1 بیان مسئله
نیاز است سامانه‌ای طراحی و پیاده‌سازی شود که موجودیت «وظیفه (Task)» را مدیریت کند:
- ایجاد وظیفه
- مشاهده لیست و جزئیات
- ویرایش و تغییر وضعیت
- حذف (حذف منطقی)

### 2.2 اهداف قابل سنجش
- ارائه API استاندارد و قابل اتکا برای CRUD (با Validation و Error Model ساخت‌یافته)
- معماری قابل توسعه (Frontend/Backend جدا، لایه‌بندی Backend)
- اجرای تکرارپذیر با Docker
- پیاده‌سازی فرایند Git با feature branches و Pull Request

---

## 3) دامنه و فرضیات
- سبک API: REST + JSON، نسخه‌بندی `/api/v1`
- DB: PostgreSQL (در Docker Compose)
- حذف: Soft Delete (فیلد `deleted_at`)
- وضعیت‌ها: `TODO`, `IN_PROGRESS`, `DONE`
- زمان‌ها: UTC
- Scope: تک‌کاربره (قابل توسعه به چندکاربره با افزودن user_id)

---

## 4) نیازمندی‌ها

### 4.1 Functional Requirements
- FR‑01 ایجاد وظیفه: `POST /api/v1/tasks`
- FR‑02 لیست وظایف: `GET /api/v1/tasks?limit&offset&status&q`
- FR‑03 مشاهده جزئیات: `GET /api/v1/tasks/{id}`
- FR‑04 ویرایش: `PATCH /api/v1/tasks/{id}`
- FR‑05 تغییر وضعیت: `PATCH /api/v1/tasks/{id}/status`
- FR‑06 حذف منطقی: `DELETE /api/v1/tasks/{id}`

### 4.2 Non‑Functional Requirements
- NFR‑01 Deployability: اجرای کامل با `docker compose up --build`
- NFR‑02 Maintainability: معماری لایه‌ای Controller/Service/Repository
- NFR‑03 Testability: وجود تست‌های API و سرویس
- NFR‑04 Security (حداقلی): Validation و عدم افشای خطاهای داخلی
- NFR‑05 Version Control: feature branch + PR برای ادغام به main

---

## 5) Use Cases (خلاصه)
- UC‑01 Create Task
- UC‑02 List Tasks (pagination + filtering)
- UC‑03 Update Task
- UC‑04 Change Task Status
- UC‑05 Delete Task (soft)

---

## 6) UML (متنی)
(کد PlantUML در گزارش اصلی نسخه DOCX درج شده است.)
- Use Case Diagram: ایجاد/لیست/جزئیات/ویرایش/تغییر وضعیت/حذف
- Class Diagram: Task, TaskStatus, TaskService, TaskRepository
- Sequence Diagram: Change Status
- State Machine: TODO → IN_PROGRESS → DONE

---

## 7) معماری سیستم
### 7.1 Backend
- Presentation/API: FastAPI routers + DTO
- Application: TaskService (Use Case logic)
- Infrastructure: TaskRepository (DB access)
- Domain: Task entity + TaskStatus

### 7.2 Frontend
- React SPA
- ارتباط با Backend از طریق fetch و متغیر محیطی `VITE_API_BASE_URL`
- UI RTL با فونت Vazirmatn و پالت صورتی/یاسی (Pastel)

---

## 8) طراحی

### 8.1 مدل داده
جدول `tasks` شامل: id, title, description, status, priority, due_at, created_at, updated_at, deleted_at

### 8.2 قرارداد API
- پاسخ موفق: `{ "data": ... }`
- پاسخ لیست: `{ "data": [...], "meta": { "pagination": ... } }`
- خطای اعتبارسنجی: `422` با ساختار ثابت و `trace_id`

---

## 9) پیاده‌سازی
### 9.1 Backend
- FastAPI + SQLAlchemy + PostgreSQL
- CORS برای فرانت (localhost:3000)
- ایجاد خودکار جدول‌ها در startup (برای سادگی پروژه آموزشی)

### 9.2 Frontend
- React + Vite
- UI کارت‌ها با تم صورتی/یاسی و افکت glassmorphism
- امکانات: ایجاد، ویرایش، تغییر وضعیت (چرخه‌ای)، حذف منطقی، فیلتر وضعیت، جستجو

---

## 10) تست و ارزیابی
- تست API (create/list/get/update/status/delete)
- تست سرویس (business logic)
- معیار پذیرش: pass شدن تست‌ها و سازگاری با نیازمندی‌ها

---

## 11) کنترل نسخه و استقرار
### 11.1 Git
- main + feature branches
- ادغام فقط از طریق PR
- پیام‌های commit استاندارد (Conventional Commits)

### 11.2 Docker
- Backend: Dockerfile مستقل
- Frontend: Dockerfile (build + nginx)
- Compose: بالا آوردن DB + API + Web

---

## 12) نتیجه‌گیری
این پروژه یک نمونه کامل و استاندارد از یک سامانه CRUD است که علاوه بر Backend صنعتی، یک Frontend کاربرپسند ارائه می‌دهد و الزامات فرایندی (Git/PR) و استقرار (Docker) را نیز رعایت می‌کند.

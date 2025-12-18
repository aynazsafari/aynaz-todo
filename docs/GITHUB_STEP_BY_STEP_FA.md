# راهنمای GitHub (گام‌به‌گام و خیلی ساده)

> هدف: شما پروژه را روی GitHub قرار بدهید و «شاخه‌های feature + Pull Request» را هم رعایت کنید (طبق الزام استاد).

---

## 1) ساخت حساب GitHub
1) مرورگر را باز کنید و وارد سایت **GitHub** شوید.  
2) روی **Sign up** کلیک کنید.  
3) ایمیل، پسورد و نام کاربری را وارد کنید.  
4) مراحل تأیید ایمیل را انجام دهید.

---

## 2) ساخت Repository جدید
1) بعد از ورود، از بالا سمت راست روی علامت **+** بزنید.  
2) گزینه **New repository** را انتخاب کنید.  
3) Repository name را بگذارید مثلاً: `todo-fullstack`  
4) Public/Private را انتخاب کنید (معمولاً Public برای پروژه دانشگاهی بهتر است مگر استاد گفته باشد).  
5) گزینه **Add a README** را **خاموش** بگذارید (چون پروژه ما README دارد).  
6) روی **Create repository** بزنید.

---

## 3) نصب Git (اگر بلد نیستید)
### گزینه A (پیشنهادی برای مبتدی‌ها): GitHub Desktop
- برنامه **GitHub Desktop** را نصب کنید.
- با اکانت GitHub لاگین کنید.
- آپلود پروژه با کلیک انجام می‌شود.

### گزینه B (حرفه‌ای/ترمینال): Git (CLI)
- ویندوز: «Git for Windows» را نصب کنید.  
- مک: معمولاً با Xcode Command Line Tools می‌آید.  
- لینوکس: با پکیج منیجر نصب می‌شود.

> اگر استاد روی «commit history» حساس است، CLI هم کاملاً مناسب است.

---

## 4) روش خیلی ساده با Command Line (پیشنهادی برای رعایت دقیق الزام استاد)

### 4.1 رفتن داخل پوشه پروژه
اول مطمئن شوید داخل فولدری هستید که فایل `docker-compose.yml` وجود دارد.

### 4.2 تنظیم نام و ایمیل Git (فقط یک بار)
```bash
git config --global user.name "نام شما"
git config --global user.email "ایمیل شما"
```

### 4.3 ساخت repo محلی و اولین commit
```bash
git init
git add .
git commit -m "chore: initial project scaffold"
```

### 4.4 وصل کردن به GitHub و push کردن
در صفحه Repo گیت‌هاب، بخش “Quick setup” آدرس repo را می‌بینید. مثال:

```bash
git remote add origin https://github.com/<USERNAME>/todo-fullstack.git
git branch -M main
git push -u origin main
```

---

## 5) رعایت الزام feature branch + Pull Request (حتی اگر تنها هستید!)

### 5.1 ساخت یک feature branch
مثلاً:
```bash
git checkout -b feature/ui-polish
```

یک تغییر کوچک انجام دهید (مثلاً یک خط در README)، سپس:
```bash
git add .
git commit -m "docs: add screenshots section"
git push -u origin feature/ui-polish
```

### 5.2 ساخت Pull Request
1) بروید به Repo در GitHub  
2) معمولاً یک پیام می‌بینید: “Compare & pull request” → روی آن بزنید  
3) عنوان PR را بنویسید (مثلاً: `docs: add screenshots section`)  
4) روی **Create pull request** بزنید

### 5.3 Merge کردن PR به main
داخل همان PR:
- روی **Merge pull request** بزنید  
- سپس **Confirm merge**

> این دقیقاً همان چیزی است که استاد می‌خواهد: ادغام فقط با PR.

---

## 6) خوشگل و حرفه‌ای کردن Repo در GitHub
در صفحه Repo:
1) بخش **About** (سمت راست) → یک Description کوتاه بنویسید  
2) Topics اضافه کنید: `software-engineering`, `fastapi`, `react`, `docker`, `crud`  
3) یک Screenshot از UI بگیرید و داخل `docs/screenshots/` بگذارید  
4) در README بخش Screenshots اضافه کنید

---

## 7) اگر ترمینال سخت است…
می‌توانید بگویید «من ویندوزم» یا «مکم»؛ قدم‌به‌قدم با کلیک‌ها راهنمایی می‌کنم.

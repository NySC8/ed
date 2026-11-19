# edmedical — فرانت‌اند (HTML / CSS / JavaScript)

همه‌ی فایل‌ها تخت‌اند (بدون پوشه). برای انتشار: همه را در ریشه‌ی ریپوی GitHub بگذارید → Settings → Pages → Branch: main / root.

- آدرس‌ها تمیزند: `/courses` ، `/blog-spinal-cord` ، `/podcasts` … (GitHub Pages خودش `.html` را حذف می‌کند؛ اگر کسی `.html` را باز کند، آدرس مرورگر اصلاح می‌شود).
- بدون Supabase سایت در **حالت نمایشی** با localStorage کار می‌کند (سبد، ورود، سفارش، دیدگاه، بازدید).
- اتصال به دیتابیس: زیپ `edmedical-supabase.zip` را طبق README داخلش اجرا کنید و مقدار `config.js` را پر کنید.
- 🔒 ربات‌ها قفل‌اند (robots.txt + meta robots). برای انتشار نهایی طبق کامنت‌های robots.txt و `build.py` بازشان کنید.
- ویرایش متن‌ها: `build_content.py` → سپس `python3 build.py` (اختیاری؛ HTML ساخته‌شده هم قابل ویرایش دستی است).
- پرداخت نمایشی: کارت `6037 9975 1234 5670` ، رمز دوم `12345` (کارتی که به `0000` ختم شود = پرداخت ناموفق).

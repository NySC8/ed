/* ───────────────────────────────────────────────
   تنظیمات edmedical
   بعد از ساخت پروژه در Supabase این دو مقدار را پر کنید
   (Project Settings → API). اگر خالی بمانند سایت در «حالت نمایشی» با
   localStorage کار می‌کند و به هیچ سروری وصل نمی‌شود.
   ─────────────────────────────────────────────── */
window.EDMED = {
  SUPABASE_URL: '',        // مثال: https://xxxxxxxx.supabase.co
  SUPABASE_ANON_KEY: '',   // کلید anon / public  (کلید service_role را هرگز اینجا نگذارید)
  PHONE_AUTH: false,       // true فقط وقتی در Supabase ارائه‌دهنده‌ی پیامک فعال کرده‌اید
  DEMO_OTP: '12345',       // کد تأیید نمایشی (فقط حالت نمایشی)
  SITE_URL: 'https://edmedical.ir'
};

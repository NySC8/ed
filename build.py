# -*- coding: utf-8 -*-
"""
تولید تمام صفحه‌های HTML سایت edmedical (فایل‌های تخت، بدون پوشه).
اجرا:  python3 build.py        ← خروجی در همین پوشه نوشته می‌شود
ویرایش متن‌ها: build_content.py
"""
import html, json, os, re, sys
from build_content import *

OUT = os.path.dirname(os.path.abspath(__file__))
URL = SITE['url']
def esc(s): return html.escape(str(s), quote=True)
def fa(n): return str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
def money(n): return f'{n:,}'
def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f: f.write(content)
P = {p['slug']: p for p in PRODUCTS}

# ───────────────────────── آیکون‌ها ─────────────────────────
ICONS = dict(
 book='M12 6.5C10.5 5 8 4.5 4 4.5v13c4 0 6.5.5 8 2 1.5-1.5 4-2 8-2v-13c-4 0-6.5.5-8 2zM12 6.5v13',
 course='M6 3h12a1 1 0 011 1v16a1 1 0 01-1 1H6a1 1 0 01-1-1V4a1 1 0 011-1zM12 8v6M9 11h6M9 17h6',
 headset='M4 14v-2a8 8 0 0116 0v2M3 14h4v6H3zM17 14h4v6h-4zM19 20c0 1-1.5 1.5-4 1.5',
 clip='M6 4.5h12v16H6zM9 4.5V3h6v1.5M12 10v6M9 13h6',
 target='M12 21a9 9 0 110-18 9 9 0 010 18zM12 16.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9zM12 12l8-8',
 inf='M12 12c-2-3-3.5-4-5.5-4a4 4 0 000 8c2 0 3.5-1 5.5-4zm0 0c2 3 3.5 4 5.5 4a4 4 0 000-8c-2 0-3.5 1-5.5 4z',
 cert='M3 4h18v13H3zM7 9h10M7 12.5h5M15 17l1 4 2-1.5 2 1.5-1-4',
 trophy='M7 4h10v5a5 5 0 01-10 0zM7 6H4v1.5A3.5 3.5 0 007.5 11M17 6h3v1.5a3.5 3.5 0 01-3.5 3.5M12 14v4M8.5 21h7',
 cart='M3 4h2.5l2 11h10l2-8H7M9 19.5h.01M17 19.5h.01',
 user='M12 12a4 4 0 100-8 4 4 0 000 8zM4.5 20c1-4 4-6 7.5-6s6.5 2 7.5 6',
 clock='M12 21a9 9 0 110-18 9 9 0 010 18zM12 7v5l3 2',
 pulse='M3 12h4l2.5-6 4 12L16 12h5',
 mega='M4 10v4h3l8 4V6L7 10zM18.5 9.5a4 4 0 010 5',
 check='M5 12.5l4.5 4.5L19 7.5', arrow='M19 12H5M11 6l-6 6 6 6',
 phone='M5 4h4l1.5 4.5-2.5 1.5a11 11 0 006 6l1.5-2.5L20 15v4a2 2 0 01-2 2A15 15 0 013 6a2 2 0 012-2z',
 mail='M3 5h18v14H3zM4 7l8 6 8-6', pin='M12 21s7-6 7-11.5A7 7 0 005 9.5C5 15 12 21 12 21zM12 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5z',
 chat='M4 5h16v11H10l-5 4v-4H4zM8.5 10.5h7', menu='M4 7h16M4 12h16M4 17h16',
 eye='M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 15a3 3 0 100-6 3 3 0 000 6z',
 cal='M4 6h16v14H4zM4 10h16M8 3v4M16 3v4', share='M8 12l8-5M8 12l8 5M6 15a3 3 0 100-6 3 3 0 000 6zM18 9a3 3 0 100-6 3 3 0 000 6zM18 21a3 3 0 100-6 3 3 0 000 6z',
 rocket='M12 3c3 2 5 5.5 5 9.5l-2 3h-6l-2-3C7 8.5 9 5 12 3zM9 15.5L6.5 18M15 15.5l2.5 2.5M12 18v3',
 mic='M12 3a3 3 0 013 3v6a3 3 0 01-6 0V6a3 3 0 013-3zM6 11a6 6 0 0012 0M12 17v4', lock='M6 11h12v9H6zM8.5 11V8a3.5 3.5 0 017 0v3',
 home='M4 11l8-7 8 7v9H4zM10 20v-5h4v5', list='M6 3h12v18H6zM9 8h6M9 12h6M9 16h4', out='M10 4H5v16h5M15 8l4 4-4 4M19 12H9', search='M11 18a7 7 0 100-14 7 7 0 000 14zM21 21l-5-5')
def ic(n, cls=''): return f'<svg class="ic {cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>' + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24"><path d="{v}"/></symbol>' for k, v in ICONS.items()) + '</defs></svg>'

# ───────────────────────── مسیرها ─────────────────────────
def url(path): return URL + '/' + path
def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': url(p)} for i, (n, p) in enumerate(items)]}
ORG = {'@context': 'https://schema.org', '@type': 'EducationalOrganization', 'name': 'edmedical', 'alternateName': 'ادمدیکال', 'url': URL,
       'logo': url('icon-512.png'), 'description': 'آموزش هوشمند پزشکی، ازپایه تا بالینی', 'telephone': '+98' + SITE['phone'][1:], 'email': SITE['email'],
       'address': {'@type': 'PostalAddress', 'addressLocality': 'کرج', 'streetAddress': 'خیابان مطهری – ساختمان کشتی', 'addressCountry': 'IR'}}

# ───────────────────────── <head> ─────────────────────────
CSP = ("default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data: blob: https:; media-src 'self' https: blob:; "
       "connect-src 'self' https://*.supabase.co wss://*.supabase.co; form-action 'self'; base-uri 'self'; object-src 'none'")
def head(title, desc, path, kw='', image='og-cover.jpg', typ='website', ld=None, extra='', full_title=None, pub=None):
    t = full_title or f'{title} | edmedical'
    ld = ld or []
    can = url(path) if path else URL + '/'
    kws = kw or 'آموزش پزشکی, دوره پزشکی, علوم پایه پزشکی, ادمدیکال, edmedical'
    art = f'<meta property="article:published_time" content="{pub}"><meta property="article:author" content="edmedical"><meta property="article:section" content="آموزش پزشکی">' if pub else ''
    return f'''<!doctype html>
<html lang="fa" dir="rtl" prefix="og: https://ogp.me/ns#">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(kws)}">
<meta name="author" content="edmedical">
<meta name="generator" content="edmedical build.py">
<meta name="application-name" content="edmedical">
<!-- 🔒 سایت هنوز آزمایشی است: ایندکس و کپی‌شدن در موتورهای جست‌وجو بسته است. هنگام راه‌اندازی نهایی، این سه خط و robots.txt را تغییر دهید. -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate">
<meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="bingbot" content="noindex, nofollow, noarchive">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#1d4b3c">
<meta name="format-detection" content="telephone=no, email=no, address=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="edmedical">
<meta name="msapplication-TileColor" content="#1d4b3c">
<meta name="geo.region" content="IR-30">
<meta name="geo.placename" content="کرج">
<meta name="language" content="fa">
<meta name="rating" content="general">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta property="og:locale" content="fa_IR">
<meta property="og:site_name" content="edmedical">
<meta property="og:type" content="{typ}">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{url(image)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
{art}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(t)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{url(image)}">
<link rel="canonical" href="{can}">
<link rel="alternate" hreflang="fa" href="{can}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="style.css">
{extra}{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)}
</head>'''

NAV = [('./', 'خانه', 'index'), ('courses', 'دوره آموزشی', 'courses'), ('blog', 'وبلاگ', 'blog'), ('podcasts', 'پادکست', 'podcasts'), ('about', 'درباره ما', 'about'), ('contact', 'تماس با ما', 'contact')]
def header(active=''):
    items = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    return f'''<a class="skip" href="#main">پرش به محتوای اصلی</a>
<header class="top"><div class="w">
<a class="logo" href="./" aria-label="edmedical – صفحه اصلی">{ic('pulse')}<span>ed<i>medical</i></span></a>
<nav class="nav" id="main-nav" aria-label="منوی اصلی"><ul class="navl">{items}</ul></nav>
<div class="act"><a class="btn" href="./#plans">{ic('chat')}مشاوره با ما</a>
<a class="ib" href="cart" aria-label="سبد خرید">{ic('cart')}<span class="bd" data-cart-count hidden>۰</span></a>
<a class="ib" href="login" data-user-link aria-label="ورود / ثبت‌نام">{ic('user')}</a>
<button class="ib menu" id="menu-btn" type="button" aria-label="باز و بسته کردن منو" aria-expanded="false" aria-controls="main-nav">{ic('menu')}</button></div></div></header>'''

FOOT_TXT = 'اد مدیکال، بستری جامع برای یادگیری هدفمند علوم پزشکی است؛ از آموزش مفهومی علوم پایه تا درک مباحث بالینی و ارتباط دانش تئوری با دنیای واقعی پزشکی .ما با ارائه دورههای آموزشی، بانک سؤاالت، آزمونهای تخصصی و محتوای علمی کاربردی، مسیر یادگیری دانشجویان علوم پزشکی را هموار میکنیم'
def footer():
    return f'''<footer class="ft2" id="footer"><div class="w">
<section aria-labelledby="f-about"><a class="logo" href="./">{ic('pulse')}<span>ed<i>medical</i></span></a><h2 class="sr" id="f-about">درباره edmedical</h2><p>{FOOT_TXT}</p></section>
<nav aria-labelledby="f-links"><h2 id="f-links">دسترسی سریع</h2><ul><li><a href="./">صفحه اصلی</a></li><li><a href="courses">محصولات</a></li><li><a href="courses">دوره ها</a></li><li><a href="podcasts">پادکست</a></li><li><a href="./#plans">پلن های مشاوره</a></li><li><a href="about">درباره ما</a></li><li><a href="blog">وبلاگ</a></li><li><a href="contact">تماس با ما</a></li></ul></nav>
<section aria-labelledby="f-contact"><h2 id="f-contact">تماس با ما</h2><address><dl><dt>تلفن</dt><dd><a href="tel:+98{SITE['phone'][1:]}" dir="ltr">{SITE['phone']}</a></dd><dt>ایمیل</dt><dd><a href="mailto:{SITE['email']}" dir="ltr">{SITE['email']}</a></dd><dt>آدرس</dt><dd>{SITE['address']}</dd></dl></address></section>
</div><p class="cp"><small>تمامی حقوق این وبسایت متعلق به <bdi>edmedical</bdi> میباشد.</small></p></footer>'''

def page(name, head_html, body_attr, inner, scripts=True, shell=True, active=''):
    sc = '<script src="config.js"></script><script src="data.js"></script><script src="app.js" defer></script><script src="pages.js" defer></script>' if scripts else ''
    top = (SPRITE + header(active)) if shell else SPRITE
    bot = footer() if shell else ''
    write(name, f'{head_html}\n<body {body_attr}>\n{top}\n{inner}\n{bot}\n<noscript><p class="ns">برای استفاده از سبد خرید، ورود و ثبت‌نام، جاوااسکریپت مرورگر را فعال کنید.</p></noscript>\n{sc}\n</body>\n</html>\n')

def bc(items):
    li = ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in items[:-1]) + f'<li aria-current="page">{items[-1][0]}</li>'
    return f'<nav class="bc" aria-label="مسیر صفحه"><ol class="bcl">{li}</ol></nav>'

# ───────────────────────── markdown ساده → HTML ─────────────────────────
def inline(s): return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(s).replace('&#x27;', "'"))
def md2html(md):
    out, toc, para, ul, tb = [], [], [], [], []
    def fp():
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    def fu():
        if ul: out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in ul) + '</ul>'); ul.clear()
    def ft():
        if tb:
            rows = [[c.strip() for c in r.strip('|').split('|')] for r in tb if not re.match(r'^\|[\s\-|:]+\|$', r)]
            h, b = rows[0], rows[1:]
            out.append('<table><caption class="sr">جدول</caption><thead><tr>' + ''.join(f'<th scope="col">{inline(c)}</th>' for c in h) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in b) + '</tbody></table>'); tb.clear()
    n = 0
    for ln in md.strip().split('\n'):
        s = ln.strip()
        if not s: fp(); fu(); ft(); continue
        m = re.match(r'^\[\[(flow|ecg|spine):(.+)\]\]$', s)
        if m:
            fp(); fu(); ft(); k, a = m.groups()
            if k == 'flow': parts = a.split('|'); cap = parts[-1]; svg = svg_flow(parts[:-1], cap)
            elif k == 'ecg': cap = a; svg = svg_ecg(a)
            else: cap = a; svg = svg_spine(a)
            out.append(f'<figure>{svg}<figcaption>{esc(cap)}</figcaption></figure>'); continue
        if s.startswith('## '): fp(); fu(); ft(); n += 1; t = s[3:]; toc.append((f's{n}', t)); out.append(f'<h2 id="s{n}">{inline(t)}</h2>')
        elif s.startswith('### '): fp(); fu(); ft(); out.append(f'<h3>{inline(s[4:])}</h3>')
        elif s.startswith('> '): fp(); fu(); ft(); out.append(f'<blockquote><p>{inline(s[2:])}</p></blockquote>')
        elif s.startswith('- '): fp(); ft(); ul.append(s[2:])
        elif s.startswith('|'): fp(); fu(); tb.append(s)
        else: fu(); ft(); para.append(s)
    fp(); fu(); ft()
    return '\n'.join(out), toc

# ───────────────────────── کارت‌ها ─────────────────────────
def course_card(p, order=0):
    cats = 'courses basic' 
    return (f'<article class="card cc course" data-price="{p["price"]}" data-title="{esc(p["title"])}" data-cats="{cats}" data-order="{order}">'
            f'<div class="im" aria-hidden="true">{ic("pulse")}</div><div class="b"><h3>{esc(p["title"])}</h3>'
            f'<div class="mt"><span title="مدت دوره"><data value="{p["hours"]}">{ic("clock")}{p["hours"]}</data></span><span><b>{money(p["price"])}</b> <small>تومان</small></span></div>'
            f'<button type="button" class="btn sm" data-add-to-cart="{p["slug"]}">{ic("cart")} افزودن به سبد خرید</button></div></article>')
COURSES = [p for p in PRODUCTS if p['kind'] == 'course']
def post_card(p):
    return (f'<article class="card po"><a href="{p["slug"]}" class="pl"><div class="imgw"><img src="{p["cover"]}" alt="{esc(p["title"])}" width="640" height="320" loading="lazy" decoding="async"></div></a><div class="b"><h3><a href="{p["slug"]}">{esc(p["title"])}</a></h3>'
            f'<div class="mt"><a href="{p["slug"]}">مطالعه کن</a><span><time datetime="{p["iso"]}">{p["date"]}</time> · {fa(p["minutes"])} دقیقه</span></div></div></article>')
def ep_card(e):
    return (f'<article class="card pd" data-title="{EP_TITLE} {e["no"]}"><a href="{e["slug"]}"><img src="{e["cover"]}" alt="{EP_TITLE} – اپیزود {e["no"]}" width="800" height="428" loading="lazy" decoding="async"></a>'
            f'<div class="b"><h3><a href="{e["slug"]}">{EP_TITLE}</a></h3><div class="mt"><span>اپیزود: {e["no"]}</span><span><time datetime="{e["iso"]}">{e["date"]}</time></span></div></div></article>')

# ───────────────────────── صفحه‌ی اصلی ─────────────────────────
T1 = 'شرکت در دوره‌های آموزشی ادمدیکال برای من تجربه‌ای بسیار ارزشمند و متفاوت بود. محتوای آموزشی با دقت و نظم ارائه شده و مطالب به شکلی قابل‌فهم و کاربردی توضیح داده می‌شوند. یکی از نقاط قوت ادمدیکال، توجه به کیفیت آموزش و تلاش برای انتقال مفاهیم تخصصی پزشکی به زبانی روشن و قابل‌درک است. این دوره‌ها به من کمک کردند تا دانش خودم را عمیق‌تر کنم، مطالب جدیدی یاد بگیرم و با اطمینان بیشتری در مسیر حرفه‌ای و تحصیلی خودم قدم بردارم. از تیم ادمدیکال بابت تلاش، تعهد و فراهم کردن چنین فضای آموزشی ارزشمندی صمیمانه تشکر می‌کنم. امیدوارم شاهد دوره‌های بیشتر و موفقیت روزافزون این مجموعه باشم.'
T2 = 'تجربه من از شرکت در دوره‌های ادمدیکال واقعاً رضایت‌بخش بود. کیفیت بالای آموزش، بیان ساده و قابل‌فهم مطالب تخصصی و کاربردی بودن محتوا باعث شد مطالب زیادی یاد بگیرم. از تیم حرفه‌ای ادمدیکال بابت این تجربه ارزشمند صمیمانه سپاسگزارم. ❤️'
T3 = 'یکی از بهترین تجربه‌های آموزشی من، شرکت در دوره‌های ادمدیکال بود. مطالب با کیفیت بالا و به شکلی کاملاً منظم و قابل‌فهم ارائه می‌شوند. محتوای دوره‌ها بسیار کاربردی است و به درک بهتر مباحث پزشکی کمک زیادی می‌کند. از اینکه چنین مجموعه‌ای با دقت و تعهد برای آموزش دانشجویان تلاش می‌کند، خوشحالم. بابت زحمات و کیفیت خوب آموزش‌ها از تیم ادمدیکال سپاسگزارم. 🌱'
def plan_card(p):
    chip = f'<span class="tm">{p["duration"]}</span>' if p['duration'] else ''
    return (f'<article class="card plan" aria-labelledby="h-{p["slug"]}"><div class="t">{ic(p["icon"])}<h3 id="h-{p["slug"]}">{p["label"]}</h3></div>'
            f'<ul>{"".join(f"<li>{ic(chr(99)+chr(104)+chr(101)+chr(99)+chr(107))}{x}</li>" for x in p["features"])}</ul>'
            f'<div class="f"><div>{chip}<div class="pr"><b>{money(p["price"])}</b> <small>تومان</small></div></div><button type="button" class="btn" data-add-to-cart="{p["slug"]}" data-buy-now>انتخاب پلن</button></div></article>')

def build_index():
    pk = P['pack-future-doctors']
    ld = [ORG, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'edmedical', 'url': URL, 'inLanguage': 'fa-IR'}]
    h = head('آموزش هوشمند پزشکی، ازپایه تا بالینی', 'دوره‌های آموزشی، آزمون‌ها و منابع کاربردی پزشکی؛ همراه شما در مسیر یادگیری و پیشرفت علمی.', '', ld=ld,
             full_title='خانه | edmedical – آموزش هوشمند پزشکی، ازپایه تا بالینی', extra='<link rel="preload" as="image" href="hero-mascot.gif">\n')
    cats = [('book', 'مشاوره تحصیلی', './#plans'), ('course', 'دوره‌های تخصصی پزشکی', 'courses'), ('headset', 'پشتیبانی و پاسخگویی', './#contact'), ('clip', 'منابع و آزمون‌های پزشکی', 'blog')]
    feats = [('inf', 'دسترسی نا محدود', 'تا همیشه'), ('book', 'آموزش پروژه محور', '3 عدد پروژه'), ('cert', 'مدرک پایان دوره', 'مدرک پایانی')]
    inner = f'''<main id="main">
<section class="hero" aria-labelledby="h-hero"><div class="w"><div>
<h1 id="h-hero">آموزش هوشمند پزشکی، ازپایه تا بالینی</h1><p class="bw" aria-label="edmedical">edmedical</p>
<p>«دوره‌های آموزشی، آزمون‌ها و منابع کاربردی پزشکی؛ همراه شما در مسیر یادگیری و پیشرفت علمی.»</p>
<a class="btn" href="courses">مشاهده دوره‌ها {ic('arrow')}</a></div>
<figure class="mf"><picture><source media="(prefers-reduced-motion: reduce)" srcset="hero-mascot-static.png"><img class="mascot" src="hero-mascot.gif" width="445" height="395" alt="+۲۰ دوره آموزشی و +۱۰۰۰ دانشجو در دوره‌های edmedical" fetchpriority="high"></picture></figure></div></section>

<section class="sec" aria-labelledby="h-cats"><div class="w"><header class="h"><div><h2 id="h-cats">دسته بندی های پر طرفدار</h2><p>دسترسی سریع به بخش های اصلی اموزشی پزشکی</p></div></header>
<ul class="g4 nolist">{"".join(f'<li><a class="card cat" href="{hh}">{ic(i)}<b>{t}</b></a></li>' for i, t, hh in cats)}</ul></div></section>

<section class="sec alt" id="courses" aria-labelledby="h-courses"><div class="w"><header class="h"><div><h2 id="h-courses">دوره‌های آموزشی ما</h2><p>آموزش‌هایی که مارا متمایز میکند</p></div><a class="btn o" href="courses">مشاهده همه</a></header>
<div class="g4">{"".join(course_card(c, i) for i, c in enumerate(COURSES))}</div></div></section>

<section class="sec" aria-labelledby="h-promo"><div class="w"><div class="promo2 card"><img src="doctor.jpg" alt="دانشجوی پزشکی | آموزش آنلاین پزشکی" width="900" height="600" loading="lazy"><div class="pt">{ic('mega')}
<h3 id="h-promo">50 درصد تخفیف پکیج دوره آموزشی ویژه پزشکان آینده</h3>
<p class="big"><b><data value="50"><i data-count="50">50</i></data></b> درصد تخفیف · <del>{money(pk['compare'])}</del> <b>{money(pk['price'])}</b> <small>تومان</small></p>
<p class="mu">شامل ۴ دوره: {"، ".join(P[s]["title"] for s in pk["includes"])}</p>
<div class="btns"><button type="button" class="btn" data-add-to-cart="{pk['slug']}" data-buy-now>{ic('cart')} خرید پکیج</button><a class="btn o" href="courses">مشاهده دوره‌ها</a></div></div></div></div></section>

<section class="sec alt" id="trust" aria-labelledby="h-trust"><div class="w"><header class="h"><h2 id="h-trust">اعتباری که داریم از اعتماد شماست</h2></header></div>
<div class="mq" dir="ltr"><div class="tr">
<figure class="card tc" dir="rtl"><header><img src="av3.jpg" alt="" width="48" height="48" loading="lazy"><figcaption><b>سمیرا پناهی</b></figcaption></header><h4>تجربه‌ای ارزشمند از یادگیری در ادمدیکال</h4><blockquote><p>{T1}</p></blockquote></figure>
<figure class="card tc" dir="rtl"><header><span class="ph">{ic('user')}</span></header><blockquote><p>{T2}</p></blockquote></figure>
<figure class="card tc" dir="rtl"><header><img src="av-atena.jpg" alt="" width="48" height="48" loading="lazy"><figcaption><b>اتنا قاسم پور</b></figcaption></header><blockquote><p>{T3}</p></blockquote></figure>
</div></div><div class="w"><div class="fc" aria-hidden="true"><img src="av1.jpg" alt="" width="38" height="38" loading="lazy"><img src="av2.jpg" alt="" width="38" height="38" loading="lazy"><img src="av3.jpg" alt="" width="38" height="38" loading="lazy"><img src="av4.jpg" alt="" width="38" height="38" loading="lazy"><img src="av5.jpg" alt="" width="38" height="38" loading="lazy"><img src="av6.jpg" alt="" width="38" height="38" loading="lazy"></div></div></section>

<section class="sec" id="plans" aria-labelledby="h-plans"><div class="w"><header class="h"><div><h2 id="h-plans">پلن های مشاوره edmedical</h2><p>رشد کسب و کار شما با مشاوره از آکادمیا — برای دیدن پلن‌های بیشتر، به چپ و راست بکشید</p></div></header>
<div class="plans-wrap"><div class="pls" tabindex="0" role="region" aria-label="پلن‌های مشاوره؛ با کشیدن یا کلیدهای جهت‌دار جابه‌جا شوید">{"".join(plan_card(P[s]) for s in ("plan-economic", "plan-advanced", "plan-standard"))}</div>
<div class="pl-nav"><button type="button" class="pl-prev" aria-label="پلن قبلی">{ic('arrow')}</button><div class="pl-dots" role="group" aria-label="انتخاب پلن"></div><button type="button" class="pl-next" aria-label="پلن بعدی">{ic('arrow')}</button></div></div></div></section>

<section class="sec alt" aria-labelledby="h-feat"><div class="w"><div class="ft"><div>
<header class="h"><div><h2 id="h-feat">ویژگـــــــــی هـــای دوره آموزشــــــی پزشکی edmedical</h2><p>ویژگی‌هایی که ما را متمایز میکند</p></div></header>
<dl class="feats">{"".join(f'<div class="card fi">{ic(i)}<div><dt>{t}</dt><dd>{s}</dd></div></div>' for i, t, s in feats)}</dl></div>
<div><img src="study.jpg" alt="دانشجویان پزشکی در حال مطالعه" width="1283" height="994" loading="lazy"><aside class="rs card" aria-label="نتایج">{ic('trophy')}<div><h3>نتایج edmedical</h3><p>+ ده‌ها شرکت معتبر دیگر</p></div><a class="btn" href="courses">شرکت در دوره‌ها {ic('arrow')}</a></aside></div></div></div></section>

<section class="sec" id="blog" aria-labelledby="h-blog"><div class="w"><header class="h"><div><h2 id="h-blog">وبلاگ من</h2><p>وبلاگ من رو مشاهده کن</p></div><a class="btn o" href="blog">مشاهده همه</a></header><div class="g4">{"".join(post_card(p) for p in POSTS)}</div></div></section>

<section class="ctc" id="contact" aria-labelledby="h-ctc"><div class="w"><div><h2 id="h-ctc">به ما دلگرم باشید.</h2><p>با خیال راحت دوره مورد نظرت رو خریداری کن ما اینجا پاسخگو هستیم.</p></div>
<div>{ic('phone')}<b dir="ltr"><a href="tel:+982125866 25".replace(" ","")>{SITE['hotline']}</a></b><p>24 ساعته پاسخگوی سوالات شما هستیم.</p></div>
<form data-form="newsletter" novalidate><label for="nl-email">عضویت در خبرنامه</label><div class="sr2"><input id="nl-email" name="email" type="email" inputmode="email" autocomplete="email" placeholder="ایمیل شما" data-v="required,email" dir="ltr" required><button class="btn" type="submit">ثبت</button></div><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><small class="err" hidden></small><p class="form-status" role="status"></p></form></div></section>
</main>'''
    inner = inner.replace('<a href="tel:+982125866 25".replace(" ","")>', '<a href="tel:+98212586625">')
    page('index.html', h, 'data-page="index"', inner, active='index')

# ───────────────────────── دوره‌ها ─────────────────────────
def build_courses():
    pk = P['pack-future-doctors']
    ld = [ORG, crumbs_ld([('خانه', ''), ('دوره آموزشی', 'courses')]),
          {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Course', 'name': c['title'], 'provider': {'@type': 'Organization', 'name': 'edmedical', 'sameAs': URL}, 'offers': {'@type': 'Offer', 'price': c['price'], 'priceCurrency': 'IRT'}}} for i, c in enumerate(COURSES)]}]
    h = head('دوره‌های آموزشی پزشکی', 'فهرست دوره‌های آموزشی edmedical: بیوشیمی، زبان انگلیسی، ایمونولوژی، انگل‌شناسی و پکیج ویژه پزشکان آینده با ۵۰ درصد تخفیف.', 'courses', kw='دوره آموزشی پزشکی, بیوشیمی, ایمونولوژی, انگل‌شناسی, زبان انگلیسی', ld=ld)
    inner = f'''<main id="main" class="w pg">{bc([('خانه', './'), ('دوره ها', 'courses')])}
<section class="card pk" aria-labelledby="h-pk"><div>{ic('mega')}<h2 id="h-pk">{pk['title']}</h2><p class="mu">همه ۴ دوره با ۵۰ درصد تخفیف · <del>{money(pk['compare'])}</del> <b>{money(pk['price'])}</b> تومان</p></div><button type="button" class="btn" data-add-to-cart="{pk['slug']}" data-buy-now>{ic('cart')} خرید پکیج</button></section>
<div class="lay"><aside class="card side" aria-label="فیلترها"><h2>فیلتر ها</h2>
<div class="op"><label class="sr" for="c-search">جست‌وجوی دوره</label><input id="c-search" type="search" placeholder="جست‌وجوی دوره…" autocomplete="off"></div>
<details open><summary>{ic('clip')}دسته بندی ها</summary><div class="op"><label><input type="checkbox" name="cat" value="courses">دوره های آموزشی<span>۴</span></label><label><input type="checkbox" name="cat" value="basic">دوره های علوم پایه پزشکی<span>۴</span></label></div></details>
<details open><summary>{ic('cart')}محدوده قیمت</summary><div class="op rg"><label for="lo">از (تومان)</label><input id="lo" type="text" inputmode="numeric" value="550000" dir="ltr"><label for="hi">تا (تومان)</label><input id="hi" type="text" inputmode="numeric" value="2900000" dir="ltr"><input id="rg" type="range" min="550000" max="2900000" step="50000" value="2900000" aria-label="حداکثر قیمت"></div></details>
<div class="op"><button type="button" class="link" id="c-reset">پاک کردن فیلترها</button></div></aside>
<section aria-labelledby="h-cl"><div class="tb"><h2 id="h-cl">دوره های آموزشی <output id="c-count" for="c-search lo hi rg" class="mu"></output></h2><label>مرتب‌سازی: <select id="c-sort"><option value="p">پرفروش‌ترین</option><option value="a">ارزان‌ترین</option><option value="d">گران‌ترین</option></select></label></div>
<div class="g3 cl" id="c-list">{"".join(course_card(c, i) for i, c in enumerate(COURSES))}</div><p class="empty" id="c-empty" hidden>دوره‌ای با این فیلتر پیدا نشد.</p></section></div></main>'''
    page('courses.html', h, 'data-page="courses"', inner, active='courses')

# ───────────────────────── وبلاگ و مقاله ─────────────────────────
def build_blog():
    ld = [ORG, crumbs_ld([('خانه', ''), ('وبلاگ', 'blog')]), {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'وبلاگ edmedical', 'url': url('blog'), 'inLanguage': 'fa-IR'}]
    h = head('وبلاگ آموزش پزشکی', 'مقاله‌های آموزشی edmedical درباره‌ی علوم پایه، مهارت‌های بالینی، علوم آزمایشگاهی و نورو‌آناتومی.', 'blog', ld=ld)
    page('blog.html', h, 'data-page="blog"', f'<main id="main" class="w pg">{bc([("خانه", "./"), ("وبلاگ", "blog")])}<header class="h" style="margin-top:14px"><h1 class="h1">وبلاگ من</h1></header><div class="g3">{"".join(post_card(p) for p in POSTS)}</div></main>', active='blog')

def build_posts():
    for p in POSTS:
        body, toc = md2html(POST_MD[p['slug']])
        rel = ''.join(f'<li><a href="{r["slug"]}">{esc(r["title"])}</a></li>' for r in POSTS if r['slug'] != p['slug'])
        ld = [ORG, crumbs_ld([('خانه', ''), ('وبلاگ', 'blog'), (p['title'], p['slug'])]),
              {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['h1'], 'description': p['desc'], 'image': url(p['cover']), 'datePublished': p['iso'], 'dateModified': p['iso'], 'inLanguage': 'fa-IR',
               'author': {'@type': 'Organization', 'name': 'edmedical'}, 'publisher': {'@type': 'Organization', 'name': 'edmedical', 'logo': {'@type': 'ImageObject', 'url': url('icon-512.png')}}, 'mainEntityOfPage': url(p['slug']), 'timeRequired': f'PT{p["minutes"]}M', 'keywords': p['kw']}]
        h = head(p['title'], p['desc'], p['slug'], kw=p['kw'], image=p['cover'], typ='article', ld=ld, pub=p['iso'], full_title=f'{p["h1"]} | edmedical')
        inner = f'''<progress id="read-progress" max="100" value="0" aria-hidden="true"></progress>
<main id="main" class="w">{bc([("خانه", "./"), ("وبلاگ", "blog"), (p["title"], p["slug"])])}
<header class="pgh"><h1>{esc(p["h1"])}</h1><p class="meta-row"><span>{ic("cal")}<time datetime="{p["iso"]}">{p["date"]}</time></span><span>{ic("clock")}{fa(p["minutes"])} دقیقه مطالعه</span><span data-views-wrap>{ic("eye")}<data data-views value="0">۰</data> بازدید</span></p></header>
<div class="art"><article class="card art-main"><img src="{p["cover"]}" alt="{esc(p["title"])}" width="640" height="320" fetchpriority="high"><div class="art-body" id="article-body">
{body}</div></article>
<aside class="side-col" aria-label="کنار مقاله"><nav class="card toc" aria-labelledby="toc-h"><h2 id="toc-h">فهرست مطالب</h2><ol>{"".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)}</ol></nav>
<div class="card share"><span>اشتراک‌گذاری:</span><button type="button" class="btn sm o" data-copy>{ic("share")} کپی پیوند</button></div>
<nav class="card related" aria-labelledby="rel-h"><h2 id="rel-h">مقاله‌های دیگر</h2><ul class="nolist">{rel}</ul></nav></aside></div></main>'''
        page(p['slug'] + '.html', h, f'data-page="post" data-slug="{p["slug"]}" data-base-views="{p["views"]}"', inner, active='blog')

# ───────────────────────── پادکست ─────────────────────────
def build_podcasts():
    ld = [ORG, crumbs_ld([('خانه', ''), ('پادکست', 'podcasts')]), {'@context': 'https://schema.org', '@type': 'PodcastSeries', 'name': EP_TITLE, 'url': url('podcasts'), 'inLanguage': 'fa-IR'}]
    h = head('پادکست‌ها', 'پادکست «کار زیاد یا تعادل»؛ گفت‌وگو درباره‌ی مرز باریک میان موفقیت حرفه‌ای و سلامت ذهنی.', 'podcasts', kw='پادکست, کار زیاد یا تعادل, سلامت ذهنی, ادمدیکال', ld=ld, image=EPISODES[0]['cover'])
    inner = f'''<main id="main" class="w pg">{bc([("خانه", "./"), ("پادکست ها", "podcasts")])}
<header class="tb" style="margin-top:14px"><h1 class="h1">پادکست ها</h1><div class="sr3"><label class="sr" for="p-search">جست‌وجو</label><input id="p-search" type="search" placeholder="جست و جو کن" autocomplete="off"></div></header>
<div class="g3" id="p-list">{"".join(ep_card(e) for e in EPISODES)}</div><p class="empty" id="p-empty" hidden>موردی پیدا نشد.</p></main>'''
    page('podcasts.html', h, 'data-page="podcasts"', inner, active='podcasts')

def cm_seed(c):
    return (f'<li class="cm" id="c-seed-{c["name"][:2]}"><article><header><b>{esc(c["name"])}</b> <span class="role">{c["role"]}</span></header><p>{esc(c["body"])}</p><footer><button type="button" class="link" data-reply="seed" data-name="{esc(c["name"])}">پاسخ</button></footer></article></li>')

def build_episodes():
    for e in EPISODES:
        txt = ''.join('<p>' + esc(t).replace('\n', '<br>') + '</p>' for t in EPISODE_TEXT)
        seeds = [c for c in SEED_COMMENTS if c['target'] == e['slug']]
        title = f'{EP_TITLE} – اپیزود {e["no"]}'
        ld = [ORG, crumbs_ld([('خانه', ''), ('پادکست', 'podcasts'), (title, e['slug'])]),
              {'@context': 'https://schema.org', '@type': 'PodcastEpisode', 'name': title, 'episodeNumber': int(e['no']), 'description': EPISODE_TEXT[0], 'datePublished': e['iso'], 'timeRequired': 'PT2H24M', 'image': url(e['cover']), 'inLanguage': 'fa-IR',
               'url': url(e['slug']), 'partOfSeries': {'@type': 'PodcastSeries', 'name': EP_TITLE, 'url': url('podcasts')}}]
        h = head(title, EPISODE_TEXT[0], e['slug'], kw='پادکست کار زیاد یا تعادل, سلامت ذهنی, فرسودگی شغلی, ادمدیکال', image=e['cover'], typ='article', ld=ld, pub=e['iso'])
        inner = f'''<main id="main" class="w">{bc([("خانه", "./"), ("پادکست ها", "podcasts"), (title, e["slug"])])}
<article class="ep" itemscope itemtype="https://schema.org/PodcastEpisode"><div><img class="cover" src="{e["cover"]}" alt="{title}" width="800" height="428" fetchpriority="high">
<figure id="media" data-media-src="" aria-label="فیلم اپیزود"><figcaption>{ic("mic")}<br>فیلم این اپیزود به‌زودی در همین بخش قرار می‌گیرد.</figcaption></figure></div>
<div class="ep-text"><header><h1 class="h1">{EP_TITLE} <small class="mu">اپیزود {e["no"]}</small></h1>
<p class="meta-row"><span>{ic("cal")}<time datetime="{e["iso"]}">{e["date"]}</time></span><span>{ic("clock")}<time datetime="PT2H24M"><data value="{e["duration_s"]}">{e["duration"]}</data></time></span><span data-views-wrap>{ic("eye")}<data data-views value="0">۰</data> بازدید</span><button type="button" class="link" data-copy>کپی پیوند</button></p></header>
<div class="desc">{txt}</div></div></article>
<section class="cms" aria-labelledby="cm-h"><h2 id="cm-h" class="h1">دیدگاه‌ها <small class="mu">(<span id="cm-count">{fa(len(seeds))}</span>)</small></h2>
<ol class="cm-list nolist" id="comments-list">{"".join(cm_seed(c) for c in seeds)}</ol>
<form class="card cm-form" id="comment-form" data-form="comment" novalidate><h3>ثبت دیدگاه‌ها</h3><p class="chip" id="reply-chip" hidden>در پاسخ به <b></b> <button type="button" aria-label="لغو پاسخ">×</button></p>
<input type="hidden" name="parent_id" value="">
<div class="r2"><div class="fd"><label for="cm-name">نام و نام خانوادگی <span class="req">*</span></label><input id="cm-name" name="name" type="text" autocomplete="name" data-v="required,name" required></div>
<div class="fd"><label for="cm-email">ایمیل <span class="req">*</span></label><input id="cm-email" name="email" type="email" inputmode="email" autocomplete="email" dir="ltr" data-v="required,email" required></div></div>
<div class="fd"><label for="cm-phone">شماره همراه <span class="req">*</span></label><input id="cm-phone" name="phone" type="tel" inputmode="numeric" autocomplete="tel" maxlength="14" dir="ltr" placeholder="09123456789" data-digits data-v="required,phone" required></div>
<div class="fd"><label for="cm-msg">پیام خود را وارد کنید <span class="req">*</span></label><textarea id="cm-msg" name="message" rows="5" maxlength="2000" placeholder="پیام خود را بگذارید" data-v="required,min:2,max:2000" required></textarea></div>
<input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">ثبت دیدگاه</button><p class="form-status" role="status"></p></form></section></main>'''
        page(e['slug'] + '.html', h, f'data-page="episode" data-slug="{e["slug"]}" data-base-views="{e["views"]}"', inner, active='podcasts')

# ───────────────────────── سبد، پرداخت، نتیجه ─────────────────────────
def build_shop():
    ld = [crumbs_ld([('خانه', ''), ('سبد خرید', 'cart')])]
    page('cart.html', head('سبد خرید', 'مرور اقلام سبد خرید و ادامه‌ی فرایند ثبت سفارش در edmedical.', 'cart', ld=ld), 'data-page="cart"',
         f'<main id="main" class="w pg">{bc([("خانه", "./"), ("سبد خرید", "cart")])}<h1 class="h1" style="margin:14px 0">سبد خرید</h1><div id="cart-body" aria-live="polite"></div></main>')
    form = f'''<form class="card co-form" id="checkout-form" data-form="checkout" novalidate><h2>اطلاعات خریدار</h2>
<div class="r2"><div class="fd"><label for="co-fn">نام <span class="req">*</span></label><input id="co-fn" name="first_name" autocomplete="given-name" data-v="required,name" required></div>
<div class="fd"><label for="co-ln">نام خانوادگی <span class="req">*</span></label><input id="co-ln" name="last_name" autocomplete="family-name" data-v="required,name" required></div>
<div class="fd"><label for="co-ph">شماره همراه <span class="req">*</span></label><input id="co-ph" name="phone" type="tel" inputmode="numeric" autocomplete="tel" maxlength="14" dir="ltr" placeholder="09123456789" data-digits data-v="required,phone" required></div>
<div class="fd"><label for="co-em">ایمیل <span class="req">*</span></label><input id="co-em" name="email" type="email" inputmode="email" autocomplete="email" dir="ltr" data-v="required,email" required></div></div>
<div class="fd"><label for="co-note">توضیحات سفارش (اختیاری)</label><textarea id="co-note" name="note" rows="3" maxlength="500" data-v="max:500"></textarea></div>
<fieldset><legend>روش پرداخت</legend><label class="rad"><input type="radio" name="gateway" value="demo" checked> درگاه پرداخت نمایشی (آزمایشی)</label></fieldset>
<div class="fd chk"><input id="co-agree" name="agree" type="checkbox" data-v="required" required><label for="co-agree">شرایط و قوانین خرید را می‌پذیرم.</label></div>
<button class="btn b" type="submit">{ic('lock')} پرداخت امن</button><p class="form-status" role="status"></p></form>'''
    page('checkout.html', head('تسویه حساب', 'تکمیل اطلاعات خریدار و رفتن به درگاه پرداخت.', 'checkout', ld=[crumbs_ld([('خانه', ''), ('سبد خرید', 'cart'), ('تسویه حساب', 'checkout')])]), 'data-page="checkout"',
         f'<main id="main" class="w pg">{bc([("خانه", "./"), ("سبد خرید", "cart"), ("تسویه حساب", "checkout")])}<h1 class="h1" style="margin:14px 0">تسویه حساب</h1><div class="co-grid">{form}<aside class="card co-sum" aria-labelledby="cs-h"><h2 id="cs-h">خلاصه سفارش</h2><div id="co-summary"></div></aside></div></main>')
    gw = f'''<main id="main" class="gw"><header class="gw-h"><b>{ic('lock')} درگاه پرداخت نمایشی</b><span>⚠ این صفحه آزمایشی است؛ هیچ مبلغی کسر نمی‌شود</span></header>
<dl class="gw-i"><dt>پذیرنده</dt><dd>edmedical (نمایشی)</dd><dt>شماره سفارش</dt><dd id="pay-order" dir="ltr">—</dd><dt>مبلغ</dt><dd><span id="pay-amount">0</span> تومان</dd></dl>
<form class="gw-f" id="pay-form" data-form="pay" novalidate><p class="gw-tm"><span>زمان باقی‌مانده</span><output id="pay-timer" dir="ltr">۱۰:۰۰</output></p>
<div class="fd"><label for="pf-card">شماره کارت</label><input id="pf-card" name="card" inputmode="numeric" autocomplete="cc-number" maxlength="19" placeholder="0000 0000 0000 0000" data-digits data-group data-v="required,card" required></div>
<div class="r2"><div class="fd"><label for="pf-cvv">CVV2</label><input id="pf-cvv" name="cvv" inputmode="numeric" autocomplete="cc-csc" maxlength="4" data-digits data-v="required,cvv" type="password" required></div>
<div class="fd"><label for="pf-m">تاریخ انقضا</label><div class="r2"><input id="pf-m" name="month" inputmode="numeric" autocomplete="cc-exp-month" maxlength="2" placeholder="ماه" data-digits data-v="required,month" required><input id="pf-y" name="year" inputmode="numeric" autocomplete="cc-exp-year" maxlength="2" placeholder="سال" aria-label="سال انقضا" data-digits data-v="required,year" required></div></div></div>
<div class="fd"><label for="pf-otp">رمز دوم (پویا)</label><div class="cap"><input id="pf-otp" name="otp" inputmode="numeric" autocomplete="one-time-code" maxlength="6" data-digits data-v="required,otp" type="password" required><button type="button" class="btn sm o" id="otp-send">دریافت رمز</button></div></div>
<div class="fd"><label for="pf-cap">کد امنیتی</label><div class="cap"><input id="pf-cap" name="captcha" inputmode="numeric" maxlength="5" data-digits data-v="required,equals" required><code id="cap-code" aria-label="کد امنیتی">— — — — —</code><button type="button" class="link" id="cap-refresh">تازه‌سازی</button></div></div>
<p class="form-status" role="alert"></p>
<div class="gw-btns"><button class="btn" type="submit">پرداخت</button><button class="btn o" type="button" id="pay-cancel">انصراف</button></div>
<details class="mu"><summary>راهنمای تست</summary><p>کارت نمونه: <bdi dir="ltr">6037 9975 1234 5670</bdi> · CVV2 و تاریخ: هر مقدار · رمز دوم: <bdi>۱۲۳۴۵</bdi><br>برای دیدن «پرداخت ناموفق»، شماره کارتی که به <bdi>0000</bdi> ختم می‌شود وارد کنید.</p></details></form>
<div id="pay-busy" hidden role="status">در حال پردازش پرداخت…</div>
<dialog id="cancel-dialog" aria-labelledby="dlg-t"><h2 id="dlg-t">لغو پرداخت</h2><p>آیا مطمئن هستید که می‌خواهید پرداخت را لغو کنید؟</p><menu><button type="button" class="btn" id="dlg-yes">بله، لغو شود</button><button type="button" class="btn o" id="dlg-no">ادامه‌ی پرداخت</button></menu></dialog></main>'''
    h = head('درگاه پرداخت نمایشی', 'صفحه‌ی آزمایشی درگاه پرداخت edmedical.', 'payment')
    page('payment.html', h, 'data-page="payment" class="gw-body"', gw, shell=False)
    page('payment-result.html', head('نتیجه‌ی پرداخت', 'رسید و وضعیت پرداخت سفارش شما در edmedical.', 'payment-result'), 'data-page="result"',
         '<main id="main" class="w"><div id="res-app" aria-live="polite"></div></main>')

# ───────────────────────── ورود، ثبت‌نام، حساب ─────────────────────────
def fd(i, label, name, typ='text', extra='', rules='required', req=True, ph='', ac=''):
    r = ' <span class="req">*</span>' if req else ''
    return f'<div class="fd"><label for="{i}">{label}{r}</label><input id="{i}" name="{name}" type="{typ}" {extra} placeholder="{ph}" autocomplete="{ac}" data-v="{rules}"{" required" if req else ""}></div>'
PHONE = 'inputmode="numeric" maxlength="14" dir="ltr" data-digits'
def pwfd(i, label='رمز عبور', ac='current-password', rules='required,password'):
    return f'<div class="fd"><label for="{i}">{label} <span class="req">*</span></label><div class="pw"><input id="{i}" name="password" type="password" autocomplete="{ac}" placeholder="یک رمز قوی انتخاب کنید" data-v="{rules}" required><button type="button" data-toggle-pass="#{i}" aria-pressed="false">نمایش</button></div></div>'
OTP = '<div class="fd otp-step" hidden><label for="OID">کد تأیید <span class="req">*</span></label><input id="OID" name="otp" inputmode="numeric" maxlength="6" autocomplete="one-time-code" dir="ltr" data-digits data-v="required,otp"></div>'
def build_auth():
    tabs = lambda a, b: f'<div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true">{a}</button><button type="button" role="tab" aria-selected="false" tabindex="-1">{b}</button></div>'
    nm = '<div class="r2">' + fd('rf', 'نام', 'first_name', ac='given-name', rules='required,name') + fd('rl', 'نام خانوادگی', 'last_name', ac='family-name', rules='required,name') + '</div>'
    nm2 = nm.replace('id="rf"', 'id="re-f"').replace('for="rf"', 'for="re-f"').replace('id="rl"', 'id="re-l"').replace('for="rl"', 'for="re-l"')
    st = '<p class="form-status" role="status"></p>'
    login = f'''<main id="main" class="w"><div class="card fm"><a class="logo" href="./">{ic('pulse')}<span>ed<i>medical</i></span></a><h1>ورود به حساب</h1><p>لطفاً روش ورود خود را انتخاب کنید:</p>{tabs('ورود با پیامک', 'ورود با ایمیل')}
<form id="login-sms" data-p="0" novalidate>{fd('ls-p', 'شماره همراه', 'phone', 'tel', PHONE, 'required,phone', ph='09123456789', ac='tel')}{OTP.replace('OID', 'ls-o')}<button class="btn b" type="submit">ارسال کد تایید</button>{st}</form>
<form id="login-email" data-p="1" hidden novalidate>{fd('le-e', 'ایمیل', 'email', 'email', 'inputmode="email" dir="ltr"', 'required,email', ac='email')}{pwfd('le-p')}<button class="btn b" type="submit">ورود</button>{st}</form>
<p class="alt-l">حساب کاربری ندارید؟ <a href="register">ثبت نام کنید</a></p></div></main>'''
    page('login.html', head('ورود به حساب', 'ورود به حساب کاربری edmedical با پیامک یا ایمیل.', 'login', ld=[crumbs_ld([('خانه', ''), ('ورود', 'login')])]), 'data-page="login"', login)
    reg = f'''<main id="main" class="w"><div class="card fm"><a class="logo" href="./">{ic('pulse')}<span>ed<i>medical</i></span></a><h1>ثبت نام</h1><p>لطفاً روش ثبت نام خود را انتخاب کنید:</p>{tabs('ثبت نام با پیامک', 'ثبت نام با ایمیل')}
<form id="reg-sms" data-p="0" novalidate>{nm}{fd('rs-p', 'شماره همراه', 'phone', 'tel', PHONE, 'required,phone', ph='09123456789', ac='tel')}{OTP.replace('OID', 'rs-o')}<button class="btn b" type="submit">ادامه و دریافت کد</button>{st}</form>
<form id="reg-email" data-p="1" hidden novalidate>{nm2}{fd('re-e', 'ایمیل', 'email', 'email', 'inputmode="email" dir="ltr"', 'required,email', ac='email')}{fd('re-p', 'شماره همراه (اختیاری)', 'phone', 'tel', PHONE, 'phone', req=False, ph='09123456789', ac='tel')}{pwfd('re-w', ac='new-password')}<button class="btn b" type="submit">تکمیل ثبت نام</button>{st}</form>
<p class="alt-l">حساب کاربری دارید؟ <a href="login">ورود</a></p></div></main>'''
    page('register.html', head('ثبت نام', 'ساخت حساب کاربری در edmedical با شماره همراه یا ایمیل.', 'register', ld=[crumbs_ld([('خانه', ''), ('ثبت نام', 'register')])]), 'data-page="register"', reg)
    menu = [('dashboard', 'home', 'پیشخوان'), ('orders', 'list', 'سفارشات'), ('courses', 'course', 'دوره های من'), ('profile', 'user', 'حساب کاربری')]
    acc = f'''<main id="main" class="w pg">{bc([("خانه", "./"), ("حساب کاربری", "account")])}<div class="ac"><aside class="card" aria-label="منوی حساب"><div class="who"><div class="avatar"><img id="avatar-img" alt="" hidden><span id="avatar-ph">{ic('user')}</span></div><b id="acc-name">—</b></div>
<nav class="mn" aria-label="بخش‌های حساب">{"".join(f'<a href="#{k}" data-tab="{k}">{ic(i)}{t}</a>' for k, i, t in menu)}<a href="login" class="out" data-logout>{ic("out")}خروج</a></nav></aside>
<div><section class="card pnl" data-panel="dashboard" aria-labelledby="p1"><h1 id="p1" class="h1">سلام <span id="acc-hello">کاربر</span> 👋</h1><div class="stats3"><div><b id="st-orders">۰</b>سفارش</div><div><b id="st-courses">۰</b>دوره‌ی فعال</div></div><p><a class="btn" href="courses">مشاهده دوره‌ها</a></p></section>
<section class="card pnl" data-panel="orders" aria-labelledby="p2" hidden><h2 id="p2">سفارشات</h2><div style="overflow-x:auto"><table class="tbl"><caption class="sr">فهرست سفارش‌ها</caption><thead><tr><th scope="col">شماره</th><th scope="col">تاریخ</th><th scope="col">وضعیت</th><th scope="col">مبلغ</th></tr></thead><tbody id="orders-body"></tbody></table></div></section>
<section class="card pnl" data-panel="courses" aria-labelledby="p3" hidden><h2 id="p3">دوره های من</h2><ul class="my-courses nolist" id="my-courses"></ul></section>
<section class="card pnl" data-panel="profile" aria-labelledby="p4" hidden><h2 id="p4">حساب کاربری</h2><p class="mu">جزئیات حساب کاربری شما در edmedical</p>
<div class="avrow"><label class="btn o sm" for="avatar-file">{ic('user')} افزودن پروفایل</label><input id="avatar-file" type="file" accept="image/png,image/jpeg,image/webp" class="sr"></div>
<form id="profile-form" data-form="profile" novalidate><div class="r2">{fd('pf-f', 'نام', 'first_name', ac='given-name', rules='required,name')}{fd('pf-l', 'نام خانوادگی', 'last_name', ac='family-name', rules='required,name')}{fd('pf-p', 'شماره همراه', 'phone', 'tel', PHONE, 'phone', req=False, ac='tel')}<div class="fd"><label for="pf-e">آدرس ایمیل</label><input id="pf-e" name="email" type="email" dir="ltr" readonly></div></div>{fd('pf-d', 'نام نمایشی', 'display_name', rules='max:60', req=False)}<button class="btn" type="submit">ذخیره تغییرات</button><p class="form-status" role="status"></p></form></section></div></div></main>'''
    page('account.html', head('حساب کاربری', 'پیشخوان، سفارش‌ها و دوره‌های شما در edmedical.', 'account'), 'data-page="account"', acc)

# ───────────────────────── درباره، تماس، ۴۰۴ ─────────────────────────
def build_misc():
    about = f'''<main id="main" class="w pg">{bc([("خانه", "./"), ("درباره ما", "about")])}<section class="about-g"><div><h1 class="h1" style="margin-bottom:12px">درباره edmedical</h1><p>{FOOT_TXT}</p><p class="mu">آموزش هوشمند پزشکی، ازپایه تا بالینی — دوره‌های آموزشی، آزمون‌ها و منابع کاربردی پزشکی؛ همراه شما در مسیر یادگیری و پیشرفت علمی.</p><p><a class="btn" href="courses">مشاهده دوره‌ها {ic('arrow')}</a></p></div><img src="study.jpg" alt="دانشجویان پزشکی در حال مطالعه" width="1283" height="994" loading="lazy"></section>
<ul class="vals nolist"><li class="card">{ic('inf')}<h2>دسترسی نا محدود</h2><p class="mu">تا همیشه</p></li><li class="card">{ic('book')}<h2>آموزش پروژه محور</h2><p class="mu">3 عدد پروژه</p></li><li class="card">{ic('cert')}<h2>مدرک پایان دوره</h2><p class="mu">مدرک پایانی</p></li></ul></main>'''
    page('about.html', head('درباره ما', 'edmedical بستری جامع برای یادگیری هدفمند علوم پزشکی است؛ از آموزش مفهومی علوم پایه تا درک مباحث بالینی.', 'about', ld=[ORG, crumbs_ld([('خانه', ''), ('درباره ما', 'about')]), {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'درباره edmedical', 'url': url('about')}]), 'data-page="about"', about, active='about')
    contact = f'''<main id="main" class="w pg">{bc([("خانه", "./"), ("تماس با ما", "contact")])}<h1 class="h1" style="margin:14px 0">تماس با ما</h1><div class="contact-g"><section class="card" aria-labelledby="ci-h"><h2 id="ci-h">راه‌های ارتباطی</h2><address><dl><dt>شماره تماس</dt><dd><a href="tel:+98{SITE['phone'][1:]}" dir="ltr">{SITE['phone']}</a></dd><dt>ایمیل</dt><dd><a href="mailto:{SITE['email']}" dir="ltr">{SITE['email']}</a></dd><dt>آدرس</dt><dd>{SITE['address']}</dd><dt>پشتیبانی</dt><dd>24 ساعته پاسخگوی سوالات شما هستیم.</dd></dl></address></section>
<form class="card" id="contact-form" data-form="contact" novalidate><h2>ارسال پیام</h2><div class="r2">{fd('ct-n', 'نام و نام خانوادگی', 'name', ac='name', rules='required,name')}{fd('ct-p', 'شماره همراه', 'phone', 'tel', PHONE, 'required,phone', ph='09123456789', ac='tel')}</div>{fd('ct-e', 'ایمیل', 'email', 'email', 'inputmode="email" dir="ltr"', 'required,email', ac='email')}
<div class="fd"><label for="ct-s">موضوع <span class="req">*</span></label><select id="ct-s" name="subject" data-v="required" required><option value="">انتخاب کنید…</option><option>سؤال درباره دوره‌ها</option><option>پشتیبانی و پاسخگویی</option><option>مشاوره تحصیلی</option><option>سایر</option></select></div>
<div class="fd"><label for="ct-m">پیام <span class="req">*</span></label><textarea id="ct-m" name="message" rows="5" maxlength="2000" data-v="required,min:5,max:2000" required></textarea></div><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn" type="submit">ارسال پیام</button><p class="form-status" role="status"></p></form></div></main>'''
    page('contact.html', head('تماس با ما', 'راه‌های ارتباط با edmedical: تلفن، ایمیل، آدرس و فرم ارسال پیام.', 'contact', ld=[ORG, crumbs_ld([('خانه', ''), ('تماس با ما', 'contact')]), {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'تماس با ما', 'url': url('contact')}]), 'data-page="contact"', contact, active='contact')
    write('404.html', '''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>صفحه پیدا نشد | edmedical</title>
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#1d4b3c"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>body{font-family:Vazirmatn,Tahoma,sans-serif;background:#f4f6f5;color:#1c2622;text-align:center;padding:90px 20px}h1{font-size:4rem;color:#1d4b3c;margin:0}p{color:#66736d}a{display:inline-block;background:#1d4b3c;color:#fff;padding:9px 22px;border-radius:4px;text-decoration:none;margin:6px}</style></head>
<body><main><h1>۴۰۴</h1><p>صفحه‌ای که دنبالش بودید پیدا نشد.</p><a id="h" href="/">صفحه اصلی</a><a id="c" href="/courses">دوره‌ها</a><a id="b" href="/blog">وبلاگ</a></main>
<script>if(/github\\.io$/.test(location.hostname)){var r='/'+location.pathname.split('/')[1]+'/';h.href=r;c.href=r+'courses';b.href=r+'blog';}</script></body></html>''')

# ───────────────────────── فایل‌های جانبی ─────────────────────────
def build_assets():
    prod = {}
    for p in PRODUCTS:
        d = dict(kind=p['kind'], title=p['title'], price=p['price'])
        for k in ('compare', 'includes', 'icon', 'duration'):
            if k in p: d[k] = p[k]
        prod[p['slug']] = d
    write('data.js', '/* تولیدشده توسط build.py — منبع: build_content.py (قیمت‌ها در سرور دوباره محاسبه می‌شوند) */\nwindow.EDMED_PRODUCTS = ' + json.dumps(prod, ensure_ascii=False, indent=1) + ';\n')
    bots = ['GPTBot', 'ChatGPT-User', 'CCBot', 'ClaudeBot', 'anthropic-ai', 'Google-Extended', 'PerplexityBot', 'Bytespider', 'Amazonbot', 'Applebot-Extended']
    write('robots.txt', '# 🔒 سایت آزمایشی است؛ تمام ربات‌ها مسدودند.\n# برای انتشار نهایی: «Disallow: /» را به «Allow: /» تغییر دهید،\n# سپس meta robots را در build.py عوض و دوباره build کنید و این خط را اضافه کنید:\n# Sitemap: ' + URL + '/sitemap.xml\n\nUser-agent: *\nDisallow: /\n\n' + '\n'.join(f'User-agent: {b}\nDisallow: /\n' for b in bots))
    pages = ['', 'courses', 'blog', 'podcasts', 'about', 'contact', 'login', 'register'] + [p['slug'] for p in POSTS] + [e['slug'] for e in EPISODES]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{URL}/{p}</loc><changefreq>weekly</changefreq></url>\n' for p in pages) + '</urlset>\n')
    write('manifest.webmanifest', json.dumps({'name': 'edmedical', 'short_name': 'edmedical', 'description': 'آموزش هوشمند پزشکی، ازپایه تا بالینی', 'lang': 'fa', 'dir': 'rtl', 'start_url': './', 'display': 'standalone', 'background_color': '#f4f6f5', 'theme_color': '#1d4b3c',
        'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}, {'src': 'favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, ensure_ascii=False, indent=1))
    write('humans.txt', '/* edmedical */\nفرانت‌اند: HTML / CSS / JavaScript بدون فریم‌ورک\nبک‌اند: Supabase (اختیاری)\nفونت: Vazirmatn\n')
    write('.nojekyll', '')

# ───────────────────────── دیتابیس Supabase (زیپ جدا) ─────────────────────────
def q(s): return "$q$" + s + "$q$"
def build_sql(d):
    os.makedirs(d, exist_ok=True)
    def w(n, c): open(os.path.join(d, n), 'w', encoding='utf-8').write(c)
    w('01_schema.sql', '''-- edmedical — ساختار دیتابیس (Supabase / PostgreSQL)
-- ترتیب اجرا: 01 → 02 → 03 → 04  (SQL Editor)
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  first_name text, last_name text, phone text unique, display_name text, avatar_url text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  constraint profiles_phone_fmt check (phone is null or phone ~ '^09[0-9]{9}$')
);

create table if not exists public.products (            -- دوره‌ها، پلن‌ها و پکیج‌ها
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('course','plan','package')),
  slug text not null unique, title text not null,
  price integer not null check (price >= 0), compare_price integer check (compare_price is null or compare_price >= price),
  hours integer, duration_label text, features jsonb not null default '[]'::jsonb, includes text[] not null default '{}',
  is_active boolean not null default true, sort integer not null default 0, created_at timestamptz not null default now()
);

create table if not exists public.posts (
  id uuid primary key default gen_random_uuid(), slug text not null unique, title text not null, excerpt text, cover text,
  read_minutes integer not null default 5, published_at timestamptz not null default now(), views integer not null default 0,
  content_html text, is_published boolean not null default true, created_at timestamptz not null default now()
);

create table if not exists public.episodes (
  id uuid primary key default gen_random_uuid(), slug text not null unique, title text not null, episode_no text not null,
  cover text, duration_seconds integer, media_url text,          -- media_url: لینک فیلم (mp4/webm/m3u8) که بعداً پر می‌شود
  description text, published_at timestamptz not null default now(), views integer not null default 0,
  is_published boolean not null default true, created_at timestamptz not null default now()
);

create table if not exists public.comments (
  id uuid primary key default gen_random_uuid(),
  target_type text not null check (target_type in ('post','episode')), target_slug text not null,
  parent_id uuid references public.comments(id) on delete cascade,
  author_name text not null check (char_length(author_name) between 2 and 80),
  email text not null check (email ~* '^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$'),
  phone text not null check (phone ~ '^09[0-9]{9}$'),
  body text not null check (char_length(body) between 2 and 2000),
  is_admin boolean not null default false, is_approved boolean not null default false,
  user_id uuid references auth.users(id) on delete set null, created_at timestamptz not null default now()
);
create index if not exists comments_target_idx on public.comments (target_type, target_slug, created_at);

create table if not exists public.view_events (          -- بازدید هوشمند: هر بازدیدکننده در روز یک‌بار
  id bigserial primary key, target_type text not null, target_slug text not null, visitor_id text not null,
  viewed_on date not null default current_date, created_at timestamptz not null default now(),
  unique (target_type, target_slug, visitor_id, viewed_on)
);

create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(), order_no text not null unique,
  public_token uuid not null default gen_random_uuid(), user_id uuid references auth.users(id) on delete set null,
  status text not null default 'pending' check (status in ('pending','paid','failed','canceled')),
  subtotal integer not null, discount integer not null default 0, total integer not null,
  customer_name text not null, customer_phone text not null, customer_email text not null,
  gateway_ref text, created_at timestamptz not null default now(), paid_at timestamptz
);
create table if not exists public.order_items (
  id uuid primary key default gen_random_uuid(), order_id uuid not null references public.orders(id) on delete cascade,
  product_slug text not null, product_kind text not null, title text not null, unit_price integer not null, qty integer not null default 1
);
create table if not exists public.payments (
  id uuid primary key default gen_random_uuid(), order_id uuid not null references public.orders(id) on delete cascade,
  status text not null, amount integer not null, card_last4 text, ref_id text, created_at timestamptz not null default now()
);
create table if not exists public.enrollments (
  user_id uuid not null references auth.users(id) on delete cascade, product_slug text not null,
  order_id uuid references public.orders(id) on delete set null, created_at timestamptz not null default now(),
  primary key (user_id, product_slug)
);
create table if not exists public.contact_messages (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 2 and 80), email text not null, phone text not null check (phone ~ '^09[0-9]{9}$'),
  subject text, message text not null check (char_length(message) between 5 and 2000), created_at timestamptz not null default now()
);
create table if not exists public.newsletter_subscribers (
  id uuid primary key default gen_random_uuid(), email text not null unique check (email ~* '^[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,}$'), created_at timestamptz not null default now()
);

-- نمای عمومی دیدگاه‌ها (بدون ایمیل و شماره)
create or replace view public.comments_public as
  select id, target_type, target_slug, parent_id, author_name, body, is_admin, created_at
  from public.comments where is_approved;
''')
    w('02_functions.sql', '''-- edmedical — توابع (RPC)  |  بعد از 01_schema.sql اجرا شود
create or replace function public.is_admin() returns boolean language sql stable as $$
  select coalesce((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin', false) $$;

-- پروفایل خودکار برای کاربر جدید
create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, first_name, last_name, phone, display_name)
  values (new.id, new.raw_user_meta_data ->> 'first_name', new.raw_user_meta_data ->> 'last_name',
          nullif(new.raw_user_meta_data ->> 'phone',''), new.raw_user_meta_data ->> 'display_name')
  on conflict (id) do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();

create or replace function public.touch_updated_at() returns trigger language plpgsql as $$ begin new.updated_at = now(); return new; end $$;
drop trigger if exists profiles_touch on public.profiles;
create trigger profiles_touch before update on public.profiles for each row execute function public.touch_updated_at();

-- بازدید هوشمند: فقط یک‌بار در روز برای هر بازدیدکننده شمرده می‌شود
create or replace function public.register_view(p_type text, p_slug text, p_visitor text) returns integer
language plpgsql security definer set search_path = public as $$
declare n integer; ins integer;
begin
  if p_type not in ('post','episode') or p_visitor is null or char_length(p_visitor) not between 8 and 64 then return 0; end if;
  insert into view_events (target_type, target_slug, visitor_id) values (p_type, p_slug, p_visitor) on conflict do nothing;
  get diagnostics ins = row_count;
  if ins = 1 then
    if p_type = 'post' then update posts set views = views + 1 where slug = p_slug returning views into n;
    else update episodes set views = views + 1 where slug = p_slug returning views into n; end if;
  end if;
  return coalesce(n, public.get_views(p_type, p_slug));
end $$;

create or replace function public.get_views(p_type text, p_slug text) returns integer
language sql stable security definer set search_path = public as $$
  select coalesce(case when p_type = 'post' then (select views from posts where slug = p_slug)
                       else (select views from episodes where slug = p_slug) end, 0) $$;

-- ثبت سفارش: قیمت‌ها همیشه از جدول products خوانده می‌شود (نه از مرورگر)
create or replace function public.create_order(p_items jsonb, p_name text, p_phone text, p_email text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare oid uuid; tok uuid; ono text; sub integer := 0; tot integer := 0; r record; it jsonb;
begin
  if jsonb_typeof(p_items) <> 'array' or jsonb_array_length(p_items) = 0 then raise exception 'سبد خرید خالی است'; end if;
  if p_phone !~ '^09[0-9]{9}$' then raise exception 'شماره همراه نامعتبر است'; end if;
  ono := 'ED-' || to_char(now(), 'YYMMDD') || '-' || lpad((floor(random() * 90000) + 10000)::int::text, 5, '0');
  insert into orders (order_no, user_id, subtotal, total, customer_name, customer_phone, customer_email)
  values (ono, auth.uid(), 0, 0, p_name, p_phone, p_email) returning id, public_token into oid, tok;
  for it in select * from jsonb_array_elements(p_items) loop
    select * into r from products where slug = it ->> 'slug' and is_active;
    if not found then raise exception 'محصول نامعتبر'; end if;
    insert into order_items (order_id, product_slug, product_kind, title, unit_price) values (oid, r.slug, r.kind, r.title, r.price);
    sub := sub + coalesce(r.compare_price, r.price); tot := tot + r.price;
  end loop;
  update orders set subtotal = sub, discount = sub - tot, total = tot where id = oid;
  return jsonb_build_object('order_id', oid, 'order_no', ono, 'token', tok, 'total', tot);
end $$;

-- ⚠ پرداخت نمایشی (DEMO). برای درگاه واقعی (زرین‌پال و ...) این تابع را حذف کنید و تأیید پرداخت را
--   در یک Edge Function انجام دهید (verify سمت سرور) — هرگز نتیجه‌ی پرداخت را از مرورگر قبول نکنید.
create or replace function public.mock_pay(p_order uuid, p_token uuid, p_success boolean, p_card_last4 text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare o orders; ref text;
begin
  select * into o from orders where id = p_order and public_token = p_token and status = 'pending';
  if not found then raise exception 'سفارش معتبر نیست'; end if;
  ref := 'MOCK-' || (floor(random() * 9000000000) + 1000000000)::bigint::text;
  insert into payments (order_id, status, amount, card_last4, ref_id) values (o.id, case when p_success then 'ok' else 'failed' end, o.total, right(coalesce(p_card_last4,''), 4), ref);
  update orders set status = case when p_success then 'paid' else 'failed' end, paid_at = case when p_success then now() end, gateway_ref = ref where id = o.id;
  if p_success and o.user_id is not null then
    insert into enrollments (user_id, product_slug, order_id)
    select o.user_id, x.slug, o.id from (
      select oi.product_slug as slug from order_items oi where oi.order_id = o.id and oi.product_kind = 'course'
      union select unnest(p.includes) from order_items oi join products p on p.slug = oi.product_slug where oi.order_id = o.id and oi.product_kind = 'package'
    ) x on conflict do nothing;
  end if;
  return jsonb_build_object('status', case when p_success then 'paid' else 'failed' end, 'ref_id', ref);
end $$;

grant execute on function public.register_view(text,text,text), public.get_views(text,text), public.create_order(jsonb,text,text,text), public.mock_pay(uuid,uuid,boolean,text) to anon, authenticated;
''')
    w('03_policies_rls.sql', '''-- edmedical — سیاست‌های امنیتی (Row Level Security)  |  بعد از 02 اجرا شود
alter table public.profiles enable row level security;
alter table public.products enable row level security;
alter table public.posts enable row level security;
alter table public.episodes enable row level security;
alter table public.comments enable row level security;
alter table public.view_events enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;
alter table public.payments enable row level security;
alter table public.enrollments enable row level security;
alter table public.contact_messages enable row level security;
alter table public.newsletter_subscribers enable row level security;

-- پروفایل: هر کاربر فقط پروفایل خودش
create policy "profiles_select_own" on public.profiles for select to authenticated using (id = auth.uid());
create policy "profiles_update_own" on public.profiles for update to authenticated using (id = auth.uid()) with check (id = auth.uid());
-- محتوای عمومی
create policy "products_public" on public.products for select to anon, authenticated using (is_active);
create policy "posts_public" on public.posts for select to anon, authenticated using (is_published);
create policy "episodes_public" on public.episodes for select to anon, authenticated using (is_published);
create policy "products_admin" on public.products for all to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "posts_admin" on public.posts for all to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "episodes_admin" on public.episodes for all to authenticated using (public.is_admin()) with check (public.is_admin());
-- دیدگاه: همه می‌توانند «ثبت» کنند (تأییدنشده)؛ نمایش فقط از نمای comments_public؛ مدیر همه‌چیز
create policy "comments_insert" on public.comments for insert to anon, authenticated with check (is_approved = false and is_admin = false);
create policy "comments_admin" on public.comments for all to authenticated using (public.is_admin()) with check (public.is_admin());
grant select on public.comments_public to anon, authenticated;
revoke select on public.comments from anon, authenticated;
-- سفارش‌ها: فقط صاحب سفارش یا مدیر (ایجاد فقط با RPC)
create policy "orders_select_own" on public.orders for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "order_items_select_own" on public.order_items for select to authenticated using (exists (select 1 from public.orders o where o.id = order_id and (o.user_id = auth.uid() or public.is_admin())));
create policy "payments_select_own" on public.payments for select to authenticated using (exists (select 1 from public.orders o where o.id = order_id and (o.user_id = auth.uid() or public.is_admin())));
create policy "enrollments_select_own" on public.enrollments for select to authenticated using (user_id = auth.uid());
-- فرم تماس و خبرنامه: فقط درج
create policy "contact_insert" on public.contact_messages for insert to anon, authenticated with check (true);
create policy "contact_admin" on public.contact_messages for select to authenticated using (public.is_admin());
create policy "news_insert" on public.newsletter_subscribers for insert to anon, authenticated with check (true);
create policy "news_admin" on public.newsletter_subscribers for select to authenticated using (public.is_admin());
-- view_events: هیچ دسترسی مستقیمی ندارد (فقط RPC)
revoke all on public.view_events, public.payments from anon;
revoke insert, update, delete on public.orders, public.order_items, public.enrollments from anon, authenticated;
''')
    s = ['-- edmedical — داده‌ی اولیه (از build_content.py تولید شده)\n-- محصولات']
    for i, p in enumerate(PRODUCTS):
        s.append("insert into public.products (kind, slug, title, price, compare_price, hours, duration_label, features, includes, sort) values (%s, %s, %s, %d, %s, %s, %s, %s::jsonb, %s, %d) on conflict (slug) do update set title = excluded.title, price = excluded.price;" % (
            q(p['kind']), q(p['slug']), q(p['title']), p['price'], p.get('compare', 'null'), p.get('hours', 'null'), q(p['duration']) if p.get('duration') else 'null',
            q(json.dumps(p.get('features', []), ensure_ascii=False)), "'{" + ','.join(p.get('includes', [])) + "}'", i))
    s.append('\n-- مقاله‌ها')
    for p in POSTS:
        body, _ = md2html(POST_MD[p['slug']])
        s.append("insert into public.posts (slug, title, excerpt, cover, read_minutes, published_at, views, content_html) values (%s, %s, %s, %s, %d, '%s', %d, %s) on conflict (slug) do update set content_html = excluded.content_html;" % (q(p['slug']), q(p['h1']), q(p['desc']), q(p['cover']), p['minutes'], p['iso'], p['views'], q(body)))
    s.append('\n-- پادکست‌ها (media_url را بعداً با لینک فیلم پر کنید)')
    for e in EPISODES:
        s.append("insert into public.episodes (slug, title, episode_no, cover, duration_seconds, media_url, description, published_at) values (%s, %s, %s, %s, %d, null, %s, '%s') on conflict (slug) do nothing;" % (q(e['slug']), q(EP_TITLE), q(e['no']), q(e['cover']), e['duration_s'], q('\n\n'.join(EPISODE_TEXT)), e['iso']))
    s.append('\n-- دیدگاه‌های نمونه')
    for c in SEED_COMMENTS:
        s.append("insert into public.comments (target_type, target_slug, author_name, email, phone, body, is_admin, is_approved) values ('episode', %s, %s, 'admin@edmedical.ir', '09125678500', %s, true, true);" % (q(c['target']), q(c['name']), q(c['body'])))
    w('04_seed.sql', '\n'.join(s) + '\n')
    w('README.md', '''# راه‌اندازی دیتابیس edmedical در Supabase

1. در [supabase.com](https://supabase.com) یک Project بسازید.
2. از منوی **SQL Editor** چهار فایل را **به ترتیب** اجرا کنید: `01_schema.sql` ← `02_functions.sql` ← `03_policies_rls.sql` ← `04_seed.sql`
3. از **Project Settings → API** مقدارهای `Project URL` و `anon public key` را بردارید و در فایل `config.js` سایت بگذارید:
   ```js
   SUPABASE_URL: 'https://xxxx.supabase.co',
   SUPABASE_ANON_KEY: 'eyJ...',
   ```
   (کلید `service_role` را هرگز در سایت نگذارید.)
4. **Authentication → Providers → Email** را فعال نگه دارید. اگر نمی‌خواهید تأیید ایمیل لازم باشد، «Confirm email» را خاموش کنید.
5. **مدیر سایت:** در Authentication → Users روی کاربر مدیر بروید و در `app_metadata` مقدار `{"role":"admin"}` را بگذارید. مدیر می‌تواند دیدگاه‌ها را تأیید کند (`comments.is_approved = true`) و پیام‌های تماس را ببیند.
6. **فیلم پادکست:** در جدول `episodes` ستون `media_url` را با لینک مستقیم `https://.../video.mp4` پر کنید؛ همان لحظه در صفحه‌ی اپیزود پخش می‌شود.

## جدول‌ها
`profiles` · `products` (دوره/پلن/پکیج) · `posts` · `episodes` · `comments` (+ نمای `comments_public`) · `view_events` · `orders` · `order_items` · `payments` · `enrollments` · `contact_messages` · `newsletter_subscribers`

## امنیت
- RLS روی همه‌ی جدول‌ها فعال است؛ ایمیل و شماره‌ی دیدگاه‌گذاران هرگز عمومی نمی‌شود.
- قیمت سفارش همیشه در سرور (`create_order`) از جدول `products` محاسبه می‌شود.
- `mock_pay` فقط **نمایشی** است. برای درگاه واقعی (زرین‌پال، IDPay و ...) یک Edge Function بنویسید که پرداخت را در سرور verify کند.
- ورود با پیامک نیاز به ارائه‌دهنده‌ی پیامک دارد (Authentication → Providers → Phone) و سپس `PHONE_AUTH: true` در `config.js`.
''')

if __name__ == '__main__':
    build_index(); build_courses(); build_blog(); build_posts(); build_podcasts(); build_episodes(); build_shop(); build_auth(); build_misc(); build_assets()
    if '--sql' in sys.argv: build_sql(os.path.join(OUT, 'supabase'))
    print('✓ build complete')

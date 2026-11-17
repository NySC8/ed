/* edmedical – فرانت‌اند | همه‌ی فایل‌ها کنار هم (بدون پوشه) */
const P={book:'M12 6.5C10.5 5 8 4.5 4 4.5v13c4 0 6.5.5 8 2 1.5-1.5 4-2 8-2v-13c-4 0-6.5.5-8 2zM12 6.5v13',
course:'M6 3h12a1 1 0 011 1v16a1 1 0 01-1 1H6a1 1 0 01-1-1V4a1 1 0 011-1zM12 8v6M9 11h6M9 17h6',
headset:'M4 14v-2a8 8 0 0116 0v2M3 14h4v6H3zM17 14h4v6h-4zM19 20c0 1-1.5 1.5-4 1.5',
clip:'M6 4.5h12v16H6zM9 4.5V3h6v1.5M12 10v6M9 13h6',
target:'M12 21a9 9 0 110-18 9 9 0 010 18zM12 16.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9zM12 12l8-8',
inf:'M12 12c-2-3-3.5-4-5.5-4a4 4 0 000 8c2 0 3.5-1 5.5-4zm0 0c2 3 3.5 4 5.5 4a4 4 0 000-8c-2 0-3.5 1-5.5 4z',
cert:'M3 4h18v13H3zM7 9h10M7 12.5h5M15 17l1 4 2-1.5 2 1.5-1-4',
trophy:'M7 4h10v5a5 5 0 01-10 0zM7 6H4v1.5A3.5 3.5 0 007.5 11M17 6h3v1.5a3.5 3.5 0 01-3.5 3.5M12 14v4M8.5 21h7',
cart:'M3 4h2.5l2 11h10l2-8H7M9 19.5h.01M17 19.5h.01',
user:'M12 12a4 4 0 100-8 4 4 0 000 8zM4.5 20c1-4 4-6 7.5-6s6.5 2 7.5 6',
clock:'M12 21a9 9 0 110-18 9 9 0 010 18zM12 7v5l3 2',
pulse:'M3 12h4l2.5-6 4 12L16 12h5',
mega:'M4 10v4h3l8 4V6L7 10zM18.5 9.5a4 4 0 010 5',
check:'M5 12.5l4.5 4.5L19 7.5',arrow:'M19 12H5M11 6l-6 6 6 6',
phone:'M5 4h4l1.5 4.5-2.5 1.5a11 11 0 006 6l1.5-2.5L20 15v4a2 2 0 01-2 2A15 15 0 013 6a2 2 0 012-2z',
mail:'M3 5h18v14H3zM4 7l8 6 8-6',pin:'M12 21s7-6 7-11.5A7 7 0 005 9.5C5 15 12 21 12 21zM12 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5z',
chat:'M4 5h16v11H10l-5 4v-4H4zM8.5 10.5h7',search:'M11 18a7 7 0 100-14 7 7 0 000 14zM21 21l-5-5',
menu:'M4 7h16M4 12h16M4 17h16',home:'M4 11l8-7 8 7v9H4zM10 20v-5h4v5',
list:'M6 3h12v18H6zM9 8h6M9 12h6M9 16h4',video:'M3 6h12v12H3zM15 10l6-3v10l-6-3',
ticket:'M4 14v-2a8 8 0 0116 0v2M3 14h4v6H3zM17 14h4v6h-4z',heart:'M12 20s-8-5-8-11a4.5 4.5 0 018-2.5A4.5 4.5 0 0120 9c0 6-8 11-8 11z',
dl:'M5 3h10l4 4v14H5zM12 9v7M9 13l3 3 3-3',out:'M10 4H5v16h5M15 8l4 4-4 4M19 12H9',
mic:'M12 3a3 3 0 013 3v6a3 3 0 01-6 3zM6 11a6 6 0 0012 0M12 17v4'};
const I=(n,c='')=>`<svg class="ic ${c}"><use href="#i-${n}"/></svg>`;
document.body.insertAdjacentHTML('afterbegin','<svg width="0" height="0" style="position:absolute"><defs>'+Object.entries(P).map(([k,d])=>`<symbol id="i-${k}" viewBox="0 0 24 24"><path d="${d.replace(/(\.\d)00/g,'$1')}"/></symbol>`).join('')+'</defs></svg>');

const L=[['index.html','صفحه اصلی'],['courses.html','دوره ها'],['blog.html','وبلاگ'],['podcasts.html','پادکست'],['index.html#plans','پلن های مشاوره']];
const cur=location.pathname.split('/').pop()||'index.html';
const hd=document.getElementById('site-header');
if(hd)hd.outerHTML=`<header class="top"><div class="w"><a class="logo" href="index.html">${I('pulse')}ed<i>medical</i></a>
<nav class="nav" id="nav">${L.map(([h,t])=>`<a href="${h}" class="${h===cur?'on':''}">${t}</a>`).join('')}</nav>
<div class="act"><a class="btn" href="index.html#plans">${I('chat')}مشاوره با ما</a><a class="ib" href="#" aria-label="سبد خرید">${I('cart')}</a><a class="ib" href="login.html" aria-label="حساب کاربری">${I('user')}</a><button class="ib menu" id="mb" aria-label="منو">${I('menu')}</button></div></div></header>`;
const ft=document.getElementById('site-footer');
if(ft)ft.outerHTML=`<footer class="ft2" id="footer"><div class="w"><div><a class="logo" href="index.html">${I('pulse')}ed<i>medical</i></a>
<p>اد مدیکال، بستری جامع برای یادگیری هدفمند علوم پزشکی است؛ از آموزش مفهومی علوم پایه تا درک مباحث بالینی و ارتباط دانش تئوری با دنیای واقعی پزشکی .ما با ارائه دوره‌های آموزشی، بانک سؤاالت، آزمونهای تخصصی و محتوای علمی کاربردی، مسیر یادگیری دانشجویان علوم پزشکی را هموار میکنیم</p></div>
<div><h4>دسترسی سریع</h4><ul><li><a href="index.html">صفحه اصلی</a></li><li><a href="courses.html">دوره ها</a></li><li><a href="index.html#plans">پلن های مشاوره</a></li><li><a href="blog.html">وبلاگ</a></li><li><a href="podcasts.html">پادکست</a></li></ul></div>
<div><h4>تماس با ما</h4><ul class="ct"><li>${I('phone')}<div><small>شماره تماس</small><b>09125678500</b></div></li><li>${I('mail')}<div><small>ایمیل</small><b>Amirreza10184@gmail.com</b></div></li><li>${I('pin')}<div><small>آدرس</small>کرج – خیابان مطهری – ساختمان کشتی</div></li></ul></div></div>
<div class="cp">تمامی حقوق این وبسایت متعلق به edmedical میباشد.</div></footer>`;
document.getElementById('mb')?.addEventListener('click',()=>document.getElementById('nav').classList.toggle('open'));

/* داده‌ها */
const fa=n=>n.toLocaleString('en-US');
const courses=[['بیوشیمی',2400000,58],['زبان انگلیسی',2400000,58],['ایمونولوژی (ایمنی‌شناسی)',2400000,58]];
const courseCard=([t,p,d])=>`<article class="card cc"><div class="im">${I('pulse')}</div><div class="b"><h3>${t}</h3><div class="mt"><span>${I('clock')}${d}</span><span><b>${fa(p)}</b> تومان</span></div></div></article>`;
const posts=[['Spinal cord | نخاع','blog-spinal'],['آموزش پزشکی از پایه','blog-basic'],['آزمایشگاه و علوم تشخیصی','blog-lab'],['مهارت‌های بالینی و تشخیصی','blog-clinical']];
const postCard=([t,i])=>`<article class="card po"><img src="${i}.jpg" alt="" loading="lazy"><div class="b"><h3>${t}</h3><div class="mt"><a href="#">مطالعه کن</a><span>۵ دقیقه</span></div></div></article>`;
const pods=[['04','pod1',1],['08','pod2',1],['02','pod3',2],['01','pod4',2]];
const podCard=([e,i,c])=>`<article class="card pd" data-c="${c}"><img src="${i}.jpg" alt=""><div class="b"><h3>کار زیاد یا تعادل</h3><small>اپیزود: ${e}</small></div></article>`;
const fill=(id,arr,fn)=>{const el=document.getElementById(id);if(el)el.innerHTML=arr.map(fn).join('')};
fill('home-courses',courses,courseCard);fill('home-posts',posts.slice(1),postCard);fill('blog-list',posts,postCard);fill('pod-list',pods,podCard);

/* دوره‌ها: فیلتر قیمت و مرتب‌سازی */
const cl=document.getElementById('course-list');
if(cl){const lo=document.getElementById('lo'),hi=document.getElementById('hi'),so=document.getElementById('so'),r=document.getElementById('rg');
const draw=()=>{let a=courses.filter(c=>c[1]>=+lo.value&&c[1]<=+hi.value);if(so.value==='a')a.sort((x,y)=>x[1]-y[1]);if(so.value==='d')a.sort((x,y)=>y[1]-x[1]);
cl.innerHTML=a.length?a.map(courseCard).join(''):'<div class="empty">دوره‌ای با این فیلتر پیدا نشد.</div>'};
[lo,hi,so].forEach(e=>e.addEventListener('input',draw));r.addEventListener('input',()=>{hi.value=r.value;draw()});draw()}

/* پادکست: جست‌وجو و دسته‌بندی */
const ps=document.getElementById('ps');
if(ps){let cat='0';const f=()=>{const q=ps.value.trim();document.querySelectorAll('#pod-list .pd').forEach(c=>{c.style.display=(cat==='0'||c.dataset.c===cat)&&c.textContent.includes(q)?'':'none'})};
ps.addEventListener('input',f);document.querySelectorAll('[data-cat]').forEach(l=>l.addEventListener('click',()=>{cat=l.dataset.cat;document.querySelectorAll('[data-cat]').forEach(x=>x.classList.toggle('on',x===l));f()}))}

/* تب‌های ورود/ثبت‌نام */
document.querySelectorAll('.tab').forEach(t=>{const bs=[...t.querySelectorAll('button')],ps2=[...document.querySelectorAll('[data-p]')];
bs.forEach((b,i)=>b.addEventListener('click',()=>{bs.forEach(x=>x.classList.toggle('on',x===b));ps2.forEach(p=>p.hidden=+p.dataset.p!==i)}))});
document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const m=f.querySelector('.ms');if(m)m.style.display='block'}));

/* اسکرول خودکار نظرات (راست به چپ، شروع با تأخیر ۰.۷ ثانیه — در style.css: .tr) */
const tr=document.querySelector('.tr');
if(tr){const b=[...tr.children];let n=0;while(tr.scrollWidth<innerWidth*1.3&&n++<8)b.forEach(c=>{const k=c.cloneNode(true);k.setAttribute('aria-hidden','true');tr.appendChild(k)});[...tr.children].forEach(c=>tr.appendChild(c.cloneNode(true)))}

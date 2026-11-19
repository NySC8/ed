/* edmedical — منطق هر صفحه (بعد از app.js بارگذاری می‌شود) */
(() => {
'use strict';
const run = () => {
const { $, $$, toEn, toFa, money, esc, store, toast, href, go, DB, Auth, Cart, Orders, bindForm, setStatus, smartView, jalali, P } = window.ED;
const page = document.body.dataset.page;
const qs = new URLSearchParams(location.search);
const SAFE_NEXT = ['account', 'checkout', 'cart'];
const nextPage = () => { const n = qs.get('next'); return SAFE_NEXT.includes(n) ? n : 'account'; };
const STATUS = { paid: ['پرداخت‌شده', 'ok'], pending: ['در انتظار پرداخت', 'wait'], failed: ['ناموفق', 'bad'], canceled: ['لغوشده', 'bad'] };
const badge = s => `<span class="st ${(STATUS[s] || [s, ''])[1]}">${(STATUS[s] || [s])[0]}</span>`;
const lineHtml = l => `<li><span>${esc(l.title)}</span><b>${money(l.price)} <small>تومان</small></b></li>`;

/* ───────── صفحه‌ی اصلی ───────── */
if (page === 'index') {
  const sc = $('.pls'), wrap = $('.plans-wrap');
  if (sc && wrap) {
    const cards = $$('.plan', sc), dots = $('.pl-dots', wrap), rtl = getComputedStyle(sc).direction === 'rtl';
    dots.innerHTML = cards.map((_, i) => `<button type="button" aria-label="پلن ${toFa(i + 1)}" data-i="${i}"></button>`).join('');
    const step = () => cards[0].getBoundingClientRect().width + parseFloat(getComputedStyle(sc).columnGap || 16);
    const max = () => Math.max(1, sc.scrollWidth - sc.clientWidth);
    const cur = () => Math.min(cards.length - 1, Math.max(0, Math.round(Math.abs(sc.scrollLeft) / max() * (cards.length - 1))));
    const sync = () => { const i = cur(); $$('button', dots).forEach((b, k) => b.setAttribute('aria-current', k === i)); cards.forEach((c, k) => c.classList.toggle('on', k === i)); };
    const to = i => sc.scrollTo({ left: (rtl ? -1 : 1) * max() * i / (cards.length - 1), behavior: 'smooth' });
    $('.pl-prev', wrap).addEventListener('click', () => to(Math.max(0, cur() - 1)));
    $('.pl-next', wrap).addEventListener('click', () => to(Math.min(cards.length - 1, cur() + 1)));
    dots.addEventListener('click', e => { const b = e.target.closest('button'); if (b) to(+b.dataset.i); });
    sc.addEventListener('scroll', () => requestAnimationFrame(sync), { passive: true });
    sc.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') { e.preventDefault(); to(Math.min(cards.length - 1, cur() + (rtl ? 1 : -1))); } if (e.key === 'ArrowRight') { e.preventDefault(); to(Math.max(0, cur() + (rtl ? -1 : 1))); } });
    /* کشیدن با ماوس (موبایل خودش اسکرول لمسی دارد) */
    let d = null;
    sc.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse' || e.target.closest('a,button')) return; d = { x: e.clientX, s: sc.scrollLeft, m: false }; sc.setPointerCapture(e.pointerId); sc.classList.add('drag'); });
    sc.addEventListener('pointermove', e => { if (!d) return; const dx = e.clientX - d.x; if (Math.abs(dx) > 4) d.m = true; sc.scrollLeft = d.s - dx; });
    const end = () => { if (!d) return; d = null; sc.classList.remove('drag'); to(cur()); };
    sc.addEventListener('pointerup', end); sc.addEventListener('pointercancel', end);
    sync(); addEventListener('resize', sync);
  }
  const tr = $('.tr');
  if (tr) { const base = [...tr.children]; let n = 0; while (tr.scrollWidth < innerWidth * 1.3 && n++ < 8) base.forEach(c => { const k = c.cloneNode(true); k.setAttribute('aria-hidden', 'true'); tr.appendChild(k); }); [...tr.children].forEach(c => { const k = c.cloneNode(true); k.setAttribute('aria-hidden', 'true'); tr.appendChild(k); }); }
  const io = new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; io.unobserve(e.target); const el = e.target, to = +el.dataset.count, t0 = performance.now(); const f = t => { const p = Math.min((t - t0) / 1600, 1); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString('en-US'); if (p < 1) requestAnimationFrame(f); }; requestAnimationFrame(f); }), { threshold: .6 });
  $$('[data-count]').forEach(e => io.observe(e));
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) $$('[data-count]').forEach(e => { e.textContent = (+e.dataset.count).toLocaleString('en-US'); });
}

/* ───────── دوره‌ها: جست‌وجو، فیلتر، مرتب‌سازی ───────── */
if (page === 'courses') {
  const list = $('#c-list'), items = $$('.course', list), q = $('#c-search'), so = $('#c-sort'), lo = $('#lo'), hi = $('#hi'), rg = $('#rg'), out = $('#c-count');
  const draw = () => {
    const cats = $$('input[name=cat]:checked').map(x => x.value), s = toEn(q.value).trim();
    const a = +toEn(lo.value) || 0, b = +toEn(hi.value) || Infinity; let n = 0;
    const vis = items.filter(el => (!cats.length || cats.some(c => el.dataset.cats.split(' ').includes(c))) && (!s || el.dataset.title.includes(s)) && +el.dataset.price >= a && +el.dataset.price <= b);
    items.forEach(el => { el.hidden = !vis.includes(el); });
    const ord = [...vis].sort((x, y) => so.value === 'a' ? x.dataset.price - y.dataset.price : so.value === 'd' ? y.dataset.price - x.dataset.price : x.dataset.order - y.dataset.order);
    ord.forEach(el => list.appendChild(el)); n = vis.length; out.textContent = n ? `${toFa(n)} دوره` : '';
    $('#c-empty').hidden = n > 0;
  };
  [q, so, lo, hi].forEach(e => e.addEventListener('input', draw)); $$('input[name=cat]').forEach(e => e.addEventListener('change', draw));
  rg.addEventListener('input', () => { hi.value = rg.value; draw(); }); draw();
  $('#c-reset')?.addEventListener('click', () => { q.value = ''; lo.value = rg.min; hi.value = rg.max; rg.value = rg.max; $$('input[name=cat]').forEach(x => { x.checked = false; }); draw(); });
}

/* ───────── پادکست‌ها: جست‌وجو ───────── */
if (page === 'podcasts') {
  const q = $('#p-search'), items = $$('#p-list .pd');
  q.addEventListener('input', () => { const s = toEn(q.value).trim(); let n = 0; items.forEach(el => { const ok = !s || toEn(el.dataset.title).includes(s); el.hidden = !ok; if (ok) n++; }); $('#p-empty').hidden = n > 0; });
}

/* ───────── مقاله ───────── */
if (page === 'post' || page === 'episode') {
  smartView(page === 'post' ? 'post' : 'episode', document.body.dataset.slug, +document.body.dataset.baseViews || 0);
  $$('[data-copy]').forEach(b => b.addEventListener('click', async () => { try { await navigator.clipboard.writeText(location.href); toast('پیوند صفحه کپی شد'); } catch { toast('کپی انجام نشد'); } }));
}
if (page === 'post') {
  const bar = $('#read-progress'), art = $('#article-body');
  const f = () => { const r = art.getBoundingClientRect(), t = r.height - innerHeight * .5; bar.value = Math.max(0, Math.min(100, Math.round((-r.top + innerHeight * .2) / t * 100))); };
  addEventListener('scroll', f, { passive: true }); f();
  const links = $$('.toc a'), heads = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
  if (heads.length) { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-20% 0px -70% 0px' }); heads.forEach(h => io.observe(h)); }
}

/* ───────── پادکست: فیلد فیلم + دیدگاه‌ها ───────── */
if (page === 'episode') {
  const slug = document.body.dataset.slug, media = $('#media'), listEl = $('#comments-list'), form = $('#comment-form');
  const setMedia = url => { if (!url) return; if (!/^https:\/\/[^\s"']+\.(mp4|webm|m3u8)(\?.*)?$/i.test(url)) return; media.innerHTML = `<video controls preload="metadata" playsinline src="${esc(url)}"></video>`; media.classList.add('has'); };
  setMedia(media.dataset.mediaSrc);
  if (DB.on()) DB.select('episodes', t => t.select('media_url').eq('slug', slug).maybeSingle()).then(r => setMedia(r.data?.media_url));
  const cmHtml = c => `<li class="cm${c.parent ? ' reply' : ''}" id="c-${esc(c.id)}"><article><header><b>${esc(c.name)}</b>${c.admin ? ' <span class="role">مدیر سایت</span>' : ''}${c.pending ? ' <span class="st wait">در انتظار تایید</span>' : ''}${c.at ? ` <time datetime="${esc(c.at)}">${esc(jalali(c.at))}</time>` : ''}</header><p>${esc(c.body)}</p>${c.pending ? '' : `<footer><button type="button" class="link" data-reply="${esc(c.id)}" data-name="${esc(c.name)}">پاسخ</button></footer>`}</article></li>`;
  const local = () => store.get('ed_comments', []).filter(c => c.target === slug);
  if (DB.on()) DB.select('comments_public', t => t.select('id,parent_id,author_name,body,is_admin,created_at').eq('target_type', 'episode').eq('target_slug', slug).order('created_at')).then(r => {
    if (!r.data) return; listEl.innerHTML = r.data.map(c => cmHtml({ id: c.id, parent: c.parent_id, name: c.author_name, body: c.body, admin: c.is_admin, at: c.created_at })).join('') + local().map(c => cmHtml({ ...c, pending: true })).join(''); $('#cm-count').textContent = toFa(r.data.length);
  }); else listEl.insertAdjacentHTML('beforeend', local().map(c => cmHtml({ ...c, pending: true })).join(''));
  const parent = $('input[name=parent_id]', form), chip = $('#reply-chip');
  document.addEventListener('click', e => { const b = e.target.closest('[data-reply]'); if (!b) return; parent.value = b.dataset.reply; chip.hidden = false; $('b', chip).textContent = b.dataset.name; form.scrollIntoView({ behavior: 'smooth', block: 'center' }); $('[name=name]', form).focus(); });
  $('button', chip).addEventListener('click', () => { parent.value = ''; chip.hidden = true; });
  bindForm(form, async v => {
    const row = { target_type: 'episode', target_slug: slug, parent_id: v.parent_id || null, author_name: v.name, email: v.email, phone: v.phone, body: v.message };
    if (DB.on()) { const { error } = await DB.insert('comments', row); if (error) throw new Error('ثبت دیدگاه انجام نشد: ' + error.message); }
    const item = { id: 'l' + Date.now(), target: slug, name: v.name, body: v.message, at: new Date().toISOString(), parent: v.parent_id };
    const l = store.get('ed_comments', []); l.push(item); store.set('ed_comments', l);
    listEl.insertAdjacentHTML('beforeend', cmHtml({ ...item, pending: true })); form.reset(); parent.value = ''; chip.hidden = true;
    setStatus(form, 'دیدگاه شما ثبت شد و پس از تأیید مدیر سایت نمایش داده می‌شود.');
  });
}

/* ───────── تماس با ما ───────── */
if (page === 'contact') {
  bindForm($('#contact-form'), async (v, f) => {
    const { error } = DB.on() ? await DB.insert('contact_messages', { name: v.name, email: v.email, phone: v.phone, subject: v.subject, message: v.message }) : { error: null };
    if (error) throw new Error('ارسال پیام انجام نشد، دوباره تلاش کنید');
    if (!DB.on()) { const l = store.get('ed_contact', []); l.push({ ...v, at: new Date().toISOString() }); store.set('ed_contact', l); }
    f.reset(); setStatus(f, 'پیام شما ارسال شد. در اولین فرصت پاسخ می‌دهیم.');
  });
}

/* ───────── ورود و ثبت‌نام ───────── */
const tabs = $('.tabs');
if (tabs) { const bs = $$('[role=tab]', tabs), ps = $$('[data-p]'); bs.forEach((b, i) => b.addEventListener('click', () => { bs.forEach(x => { x.setAttribute('aria-selected', x === b); x.tabIndex = x === b ? 0 : -1; }); ps.forEach(p => { p.hidden = +p.dataset.p !== i; }); })); }
const otpFlow = (form, onVerified) => bindForm(form, async v => {
  if (form.dataset.step !== '2') { Auth.sendOtp(v.phone); form.dataset.step = '2'; $('.otp-step', form).hidden = false; $('[name=otp]', form).focus(); $('[type=submit]', form).textContent = 'تأیید و ادامه'; return setStatus(form, `کد تأیید به ${toFa(v.phone)} ارسال شد (۲ دقیقه اعتبار دارد).`); }
  if (!Auth.checkOtp(v.phone, v.otp)) throw new Error('کد تأیید نادرست یا منقضی شده است');
  await onVerified(v); go(nextPage());
});
if (page === 'login') {
  otpFlow($('#login-sms'), async v => Auth.signInPhone(v.phone));
  bindForm($('#login-email'), async v => { await Auth.signIn(v.email, v.password); go(nextPage()); });
}
if (page === 'register') {
  otpFlow($('#reg-sms'), async v => { await Auth.signUp({ first_name: v.first_name, last_name: v.last_name, phone: v.phone }); });
  bindForm($('#reg-email'), async (v, f) => { const r = await Auth.signUp({ first_name: v.first_name, last_name: v.last_name, phone: v.phone, email: v.email, password: v.password }); if (r.needsConfirm) return setStatus(f, 'ثبت‌نام انجام شد. برای فعال‌سازی، پیوند ارسال‌شده به ایمیل خود را باز کنید.'); go(nextPage()); });
}

/* ───────── سبد خرید ───────── */
if (page === 'cart') {
  const body = $('#cart-body');
  const draw = () => {
    const lines = Cart.lines(), t = Cart.totals();
    if (!lines.length) { body.innerHTML = `<div class="empty-state"><p>سبد خرید شما خالی است.</p><a class="btn" href="courses">مشاهده دوره‌ها</a></div>`; return; }
    body.innerHTML = `<div class="cart-grid"><table class="tbl"><caption class="sr">اقلام سبد خرید</caption><thead><tr><th scope="col">محصول</th><th scope="col">نوع</th><th scope="col">قیمت</th><th scope="col"><span class="sr">حذف</span></th></tr></thead><tbody>${lines.map(l => `<tr><th scope="row">${esc(l.title)}${l.includes ? `<small class="mu">شامل ${toFa(l.includes.length)} دوره</small>` : ''}</th><td>${{ course: 'دوره', plan: 'پلن مشاوره', package: 'پکیج' }[l.kind]}</td><td><b>${money(l.price)}</b> ${l.compare ? `<del>${money(l.compare)}</del>` : ''}<small> تومان</small></td><td><button type="button" class="link" data-rm="${l.slug}" aria-label="حذف ${esc(l.title)}">حذف</button></td></tr>`).join('')}</tbody></table>
    <aside class="card sum"><h2>خلاصه سفارش</h2><dl><dt>جمع کل</dt><dd>${money(t.subtotal)} <small>تومان</small></dd>${t.saved ? `<dt>تخفیف</dt><dd class="ok">− ${money(t.saved)} <small>تومان</small></dd>` : ''}<dt class="tot">مبلغ قابل پرداخت</dt><dd class="tot">${money(t.total)} <small>تومان</small></dd></dl><a class="btn b" href="checkout">ادامه و ثبت سفارش</a><a class="link" href="courses">ادامه خرید</a></aside></div>`;
  };
  body.addEventListener('click', e => { const b = e.target.closest('[data-rm]'); if (b) { Cart.remove(b.dataset.rm); draw(); } });
  draw();
}

/* ───────── تسویه حساب ───────── */
if (page === 'checkout') {
  const form = $('#checkout-form'), sum = $('#co-summary');
  if (!Cart.lines().length) { go('cart'); return; }
  const t = Cart.totals();
  sum.innerHTML = `<ul class="lines">${Cart.lines().map(lineHtml).join('')}</ul><dl><dt>جمع کل</dt><dd>${money(t.subtotal)} <small>تومان</small></dd>${t.saved ? `<dt>تخفیف</dt><dd class="ok">− ${money(t.saved)} <small>تومان</small></dd>` : ''}<dt class="tot">قابل پرداخت</dt><dd class="tot">${money(t.total)} <small>تومان</small></dd></dl>`;
  Auth.user().then(u => { if (!u) return; const set = (n, v) => { if (form.elements[n] && !form.elements[n].value) form.elements[n].value = v || ''; }; set('first_name', u.first_name); set('last_name', u.last_name); set('phone', u.phone); set('email', u.email); });
  bindForm(form, async v => { await Orders.create({ name: `${v.first_name} ${v.last_name}`, phone: v.phone, email: v.email, note: v.note || '' }); go('payment'); });
}

/* ───────── درگاه پرداخت نمایشی ───────── */
if (page === 'payment') {
  const id = store.get('ed_pending', null), o = id && Orders.get(id);
  if (!o || o.status !== 'pending') { go('cart'); return; }
  $('#pay-amount').textContent = money(o.total); $('#pay-order').textContent = o.number;
  const cap = () => { window.__captcha = String(Math.floor(10000 + Math.random() * 90000)); $('#cap-code').textContent = window.__captcha.split('').join(' '); };
  cap(); $('#cap-refresh').addEventListener('click', cap);
  $('#otp-send').addEventListener('click', () => toast('رمز پویای نمایشی: ' + toFa(window.ED.cfg.DEMO_OTP), { ms: 7000 }));
  let left = 600; const tm = $('#pay-timer');
  const timer = setInterval(() => { left--; tm.textContent = `${toFa(String(Math.floor(left / 60)).padStart(2, '0'))}:${toFa(String(left % 60).padStart(2, '0'))}`; if (left <= 0) { clearInterval(timer); Orders.cancel(o.id); go('payment-result', `?order=${o.id}`); } }, 1000);
  const done = r => { clearInterval(timer); go('payment-result', `?order=${r.id}`); };
  bindForm($('#pay-form'), async v => {
    const last4 = v.card.slice(-4); $('#pay-busy').hidden = false; await new Promise(r => setTimeout(r, 1600));
    if (last4 === '0000') { const r = await Orders.pay(o.id, false, last4); return done(r); }
    if (v.otp !== window.ED.cfg.DEMO_OTP) { $('#pay-busy').hidden = true; throw new Error('رمز پویا نادرست است (در حالت نمایشی: ' + toFa(window.ED.cfg.DEMO_OTP) + ')'); }
    done(await Orders.pay(o.id, true, last4));
  });
  const dlg = $('#cancel-dialog');
  $('#pay-cancel').addEventListener('click', () => dlg.showModal ? dlg.showModal() : (confirm('پرداخت لغو شود؟') && done(Orders.cancel(o.id))));
  $('#dlg-no', dlg).addEventListener('click', () => dlg.close()); $('#dlg-yes', dlg).addEventListener('click', () => { dlg.close(); done(Orders.cancel(o.id)); });
}

/* ───────── نتیجه‌ی پرداخت ───────── */
if (page === 'result') {
  const o = Orders.get(qs.get('order')), app = $('#res-app');
  if (!o) { app.innerHTML = '<div class="empty-state"><p>سفارشی پیدا نشد.</p><a class="btn" href="./">صفحه اصلی</a></div>'; return; }
  const ok = o.status === 'paid';
  document.title = (ok ? 'پرداخت موفق' : 'پرداخت ناموفق') + ' | edmedical';
  app.innerHTML = `<div class="res ${ok ? 'ok' : 'bad'}"><h1>${ok ? 'پرداخت با موفقیت انجام شد' : (o.status === 'canceled' ? 'پرداخت لغو شد' : 'پرداخت ناموفق بود')}</h1>
  <p>${ok ? 'سپاسگزاریم! سفارش شما ثبت شد و دوره‌ها در حساب کاربری شما فعال می‌شود.' : 'مبلغی از حساب شما کسر نشده است. می‌توانید دوباره تلاش کنید.'}</p>
  <table class="tbl"><caption class="sr">رسید سفارش</caption><tbody><tr><th scope="row">شماره سفارش</th><td>${esc(o.number)}</td></tr><tr><th scope="row">وضعیت</th><td>${badge(o.status)}</td></tr><tr><th scope="row">تاریخ</th><td><time datetime="${esc(o.paidAt || o.createdAt)}">${esc(jalali(o.paidAt || o.createdAt))}</time></td></tr>${ok ? `<tr><th scope="row">کد پیگیری</th><td>${esc(o.ref)}</td></tr>` : ''}<tr><th scope="row">مبلغ</th><td><b>${money(o.total)}</b> تومان</td></tr></tbody></table>
  <ul class="lines">${o.items.map(lineHtml).join('')}</ul>
  <p class="actions">${ok ? '<a class="btn" href="account#courses">دوره‌های من</a><button type="button" class="btn o" onclick="print()">چاپ رسید</button>' : '<a class="btn" href="cart">بازگشت به سبد خرید</a>'}<a class="link" href="./">صفحه اصلی</a></p></div>`;
}

/* ───────── حساب کاربری ───────── */
if (page === 'account') {
  Auth.user().then(async u => {
    if (!u) return go('login', '?next=account');
    $('#acc-name').textContent = u.display_name || 'کاربر edmedical'; $('#acc-hello').textContent = u.first_name || u.display_name || 'کاربر';
    const panels = $$('[data-panel]'), links = $$('[data-tab]');
    const show = () => { const h = (location.hash || '#dashboard').slice(1); const t = panels.some(p => p.dataset.panel === h) ? h : 'dashboard'; panels.forEach(p => { p.hidden = p.dataset.panel !== t; }); links.forEach(a => a.classList.toggle('on', a.dataset.tab === t)); };
    addEventListener('hashchange', show); show();
    const list = await Orders.mine(), bought = Orders.purchased(list);
    $('#st-orders').textContent = toFa(list.length); $('#st-courses').textContent = toFa(bought.length);
    $('#orders-body').innerHTML = list.length ? list.map(o => `<tr><th scope="row">${esc(o.number)}</th><td><time datetime="${esc(o.createdAt)}">${esc(jalali(o.createdAt))}</time></td><td>${badge(o.status)}</td><td><b>${money(o.total)}</b> <small>تومان</small></td></tr>`).join('') : '<tr><td colspan="4" class="empty">هنوز سفارشی ثبت نکرده‌اید.</td></tr>';
    $('#my-courses').innerHTML = bought.length ? bought.map(b => `<li class="card"><b>${esc(b.title)}</b><small class="mu">سفارش ${esc(b.orderNo)}</small></li>`).join('') : '<li class="empty">هنوز دوره‌ای خریداری نکرده‌اید. <a href="courses">مشاهده دوره‌ها</a></li>';
    const f = $('#profile-form'); ['first_name', 'last_name', 'phone', 'display_name'].forEach(n => { f.elements[n].value = u[n] || ''; }); f.elements.email.value = u.email || '';
    bindForm(f, async v => { const patch = { first_name: v.first_name, last_name: v.last_name, phone: v.phone, display_name: v.display_name || `${v.first_name} ${v.last_name}` }; await Auth.updateProfile(patch); $('#acc-name').textContent = patch.display_name; setStatus(f, 'تغییرات ذخیره شد.'); });
    const av = store.get('ed_avatar', null), img = $('#avatar-img'); if (av) { img.src = av; img.hidden = false; $('#avatar-ph').hidden = true; }
    $('#avatar-file').addEventListener('change', e => { const file = e.target.files[0]; if (!file) return; if (!/^image\/(png|jpe?g|webp)$/.test(file.type) || file.size > 3e6) return toast('تصویر png/jpg/webp و کمتر از ۳ مگابایت انتخاب کنید'); const r = new FileReader(); r.onload = () => { const im = new Image(); im.onload = () => { const c = document.createElement('canvas'); c.width = c.height = 160; const s = Math.min(im.width, im.height); c.getContext('2d').drawImage(im, (im.width - s) / 2, (im.height - s) / 2, s, s, 0, 0, 160, 160); const d = c.toDataURL('image/jpeg', .85); store.set('ed_avatar', d); img.src = d; img.hidden = false; $('#avatar-ph').hidden = true; toast('تصویر پروفایل به‌روز شد'); }; im.src = r.result; }; r.readAsDataURL(file); });
    $$('[data-logout]').forEach(b => b.addEventListener('click', async e => { e.preventDefault(); await Auth.signOut(); go('login'); }));
  });
}
};
if (window.ED) run(); else document.addEventListener('ed:ready', run, { once: true });
})();

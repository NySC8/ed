/* edmedical — هسته‌ی جاوااسکریپت (مسیریابی، سبد خرید، احراز هویت، دیتابیس، فرم‌ها) */
(() => {
'use strict';
const cfg = Object.assign({ SUPABASE_URL: '', SUPABASE_ANON_KEY: '', PHONE_AUTH: false, DEMO_OTP: '12345' }, window.EDMED || {});
const P = window.EDMED_PRODUCTS || {};
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const FA = '۰۱۲۳۴۵۶۷۸۹', AR = '٠١٢٣٤٥٦٧٨٩';
const toEn = s => String(s ?? '').replace(/[۰-۹]/g, d => FA.indexOf(d)).replace(/[٠-٩]/g, d => AR.indexOf(d));
const toFa = n => String(n).replace(/\d/g, d => FA[d]);
const money = n => Number(n).toLocaleString('en-US');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => { const r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16); }));
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* حافظه پر یا بسته */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* noop */ } }
};
const sha = async s => [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))].map(b => b.toString(16).padStart(2, '0')).join('');
const jalali = iso => { try { return new Intl.DateTimeFormat('fa-IR-u-ca-persian', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(iso)); } catch { return iso; } };

/* ───────── مسیریابی: آدرس‌های تمیز بدون .html ───────── */
const isLocal = location.protocol === 'file:' || /^(localhost|127\.0\.0\.1|\[::1\]|0\.0\.0\.0)$/.test(location.hostname);
const href = (page, q = '') => (isLocal ? (page || 'index') + '.html' : (page || './')) + q;
const go = (page, q) => { location.href = href(page, q); };
if (isLocal) {
  $$('a[href]').forEach(a => {
    const h = a.getAttribute('href'); if (!h || /^([a-z]+:|#)/i.test(h)) return;
    const [p, hash] = h.split('#'); const path = (p === './' || p === '') ? 'index' : p;
    if (/\.[a-z0-9]+$/i.test(path)) return;
    a.setAttribute('href', path + '.html' + (hash ? '#' + hash : ''));
  });
} else if (/\.html$/.test(location.pathname)) {
  history.replaceState(null, '', location.pathname.replace(/index\.html$/, '').replace(/\.html$/, '') + location.search + location.hash);
}

/* ───────── اعلان (toast) ───────── */
function toast(msg, opt = {}) {
  let t = $('#toast');
  if (!t) { t = document.createElement('div'); t.id = 'toast'; t.setAttribute('role', 'status'); t.setAttribute('aria-live', 'polite'); document.body.appendChild(t); }
  t.innerHTML = '<span></span>'; t.firstChild.textContent = msg;
  if (opt.link) { const a = document.createElement('a'); a.href = href(opt.link[0]); a.textContent = opt.link[1]; t.appendChild(a); }
  t.classList.add('on'); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove('on'), opt.ms || 4200);
}

/* ───────── دیتابیس (Supabase) با حالت نمایشی ───────── */
const DB = {
  on: () => !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY),
  _p: null,
  client() {
    if (!this.on()) return Promise.resolve(null);
    if (!this._p) this._p = new Promise(res => {
      const make = () => res(window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY));
      if (window.supabase) return make();
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js';
      s.async = true; s.onload = make; s.onerror = () => res(null); document.head.appendChild(s);
    });
    return this._p;
  },
  async rpc(fn, args) { const c = await this.client(); return c ? c.rpc(fn, args) : { data: null, error: { message: 'offline' } }; },
  async insert(table, row) { const c = await this.client(); return c ? c.from(table).insert(row) : { error: { message: 'offline' } }; },
  async select(table, build) { const c = await this.client(); if (!c) return { data: null, error: { message: 'offline' } }; return build(c.from(table)); }
};

/* ───────── احراز هویت ───────── */
const Auth = {
  map(u) { const m = u.user_metadata || {}; return { id: u.id, email: u.email || '', phone: m.phone || u.phone || '', first_name: m.first_name || '', last_name: m.last_name || '', display_name: m.display_name || [m.first_name, m.last_name].filter(Boolean).join(' ') }; },
  async user() {
    if (DB.on()) { const c = await DB.client(); if (c) { const { data } = await c.auth.getSession(); if (data?.session?.user) return this.map(data.session.user); } }
    return store.get('ed_user', null);
  },
  accounts: () => store.get('ed_accounts', []),
  async signUp({ first_name, last_name, phone, email, password }) {
    if (DB.on()) {
      const c = await DB.client(); if (!c) throw new Error('اتصال به سرور برقرار نشد');
      const { data, error } = await c.auth.signUp({ email, password, options: { data: { first_name, last_name, phone, display_name: `${first_name} ${last_name}` } } });
      if (error) throw new Error(error.message.includes('registered') ? 'این ایمیل قبلاً ثبت شده است' : error.message);
      return { needsConfirm: !data.session };
    }
    const list = this.accounts();
    if (list.some(a => (email && a.email === email) || (phone && a.phone === phone))) throw new Error('این ایمیل یا شماره قبلاً ثبت شده است');
    const acc = { id: uid(), first_name, last_name, phone: phone || '', email: email || '', display_name: `${first_name} ${last_name}`, pw: password ? await sha(password) : '' };
    list.push(acc); store.set('ed_accounts', list); store.set('ed_user', { ...acc, pw: undefined });
    return { needsConfirm: false };
  },
  async signIn(email, password) {
    if (DB.on()) {
      const c = await DB.client(); if (!c) throw new Error('اتصال به سرور برقرار نشد');
      const { error } = await c.auth.signInWithPassword({ email, password });
      if (error) throw new Error('ایمیل یا رمز عبور نادرست است'); return;
    }
    const h = await sha(password);
    const acc = this.accounts().find(a => a.email === email && a.pw === h);
    if (!acc) throw new Error('ایمیل یا رمز عبور نادرست است');
    store.set('ed_user', { ...acc, pw: undefined });
  },
  sendOtp(phone) {
    if (DB.on() && !cfg.PHONE_AUTH) throw new Error('ورود با پیامک هنوز فعال نشده است؛ فعلاً با ایمیل وارد شوید');
    store.set('ed_otp', { phone, code: cfg.DEMO_OTP, exp: Date.now() + 120000 });
    toast(`کد تأیید نمایشی: ${toFa(cfg.DEMO_OTP)}`, { ms: 8000 });
  },
  checkOtp(phone, code) { const o = store.get('ed_otp', null); return !!o && o.phone === phone && o.code === code && o.exp > Date.now(); },
  signInPhone(phone) {
    const acc = this.accounts().find(a => a.phone === phone); if (!acc) throw new Error('حسابی با این شماره پیدا نشد؛ ابتدا ثبت‌نام کنید');
    store.set('ed_user', { ...acc, pw: undefined }); store.del('ed_otp');
  },
  async updateProfile(patch) {
    if (DB.on()) {
      const c = await DB.client(); const { data } = await c.auth.getSession(); const u = data?.session?.user; if (!u) throw new Error('وارد حساب خود نشده‌اید');
      const meta = { ...u.user_metadata, ...patch };
      const { error } = await c.auth.updateUser({ data: meta }); if (error) throw new Error(error.message);
      await c.from('profiles').update({ first_name: patch.first_name, last_name: patch.last_name, phone: patch.phone || null, display_name: patch.display_name }).eq('id', u.id);
      return;
    }
    const cur = store.get('ed_user', null); if (!cur) throw new Error('وارد حساب خود نشده‌اید');
    const next = { ...cur, ...patch }; store.set('ed_user', next);
    store.set('ed_accounts', this.accounts().map(a => a.id === cur.id ? { ...a, ...patch } : a));
  },
  async signOut() { if (DB.on()) { const c = await DB.client(); if (c) await c.auth.signOut(); } store.del('ed_user'); }
};

/* ───────── سبد خرید ───────── */
const Cart = {
  key: 'ed_cart',
  slugs() { return store.get(this.key, []).filter(s => P[s]); },
  has(s) { return this.slugs().includes(s); },
  add(s) {
    const p = P[s]; if (!p) return false; let a = this.slugs();
    if (a.includes(s)) { toast('این مورد از قبل در سبد خرید شما هست', { link: ['cart', 'مشاهده سبد'] }); return false; }
    if (p.kind === 'package') a = a.filter(x => !(p.includes || []).includes(x));
    else if (p.kind === 'course' && a.some(x => P[x].kind === 'package' && P[x].includes.includes(s))) { toast('این دوره در پکیج انتخابی شما وجود دارد'); return false; }
    a.push(s); store.set(this.key, a); this.badge(); toast(`«${p.title}» به سبد خرید اضافه شد`, { link: ['cart', 'مشاهده سبد'] }); return true;
  },
  remove(s) { store.set(this.key, this.slugs().filter(x => x !== s)); this.badge(); },
  clear() { store.set(this.key, []); this.badge(); },
  lines() { return this.slugs().map(s => ({ slug: s, ...P[s] })); },
  totals() { const l = this.lines(); const total = l.reduce((a, x) => a + x.price, 0); const subtotal = l.reduce((a, x) => a + (x.compare || x.price), 0); return { count: l.length, total, subtotal, saved: subtotal - total }; },
  badge() { const n = this.slugs().length; $$('[data-cart-count]').forEach(e => { e.textContent = toFa(n); e.hidden = !n; }); $$('[data-add-to-cart]').forEach(b => { const done = this.has(b.dataset.addToCart); b.classList.toggle('done', done); if (b.dataset.label === undefined) b.dataset.label = b.textContent.trim(); b.lastChild && (b.lastChild.textContent = done ? ' در سبد خرید ✓' : ' ' + b.dataset.label); }); }
};
document.addEventListener('click', e => {
  const b = e.target.closest('[data-add-to-cart]'); if (!b) return; e.preventDefault();
  Cart.add(b.dataset.addToCart);
  if (b.hasAttribute('data-buy-now')) go('cart');
});

/* ───────── سفارش‌ها (دمو + RPC سرور) ───────── */
const Orders = {
  list() { return store.get('ed_orders', []); },
  save(l) { store.set('ed_orders', l); },
  get(id) { return this.list().find(o => o.id === id); },
  async create(customer) {
    const lines = Cart.lines(); if (!lines.length) throw new Error('سبد خرید خالی است');
    const t = Cart.totals();
    const order = { id: uid(), number: 'ED-' + Date.now().toString(36).toUpperCase().slice(-6) + (10 + Math.floor(Math.random() * 90)), token: uid(), status: 'pending', createdAt: new Date().toISOString(), customer,
      items: lines.map(l => ({ slug: l.slug, kind: l.kind, title: l.title, price: l.price })), subtotal: t.subtotal, discount: t.saved, total: t.total, ref: '' };
    if (DB.on()) {
      const { data, error } = await DB.rpc('create_order', { p_items: lines.map(l => ({ slug: l.slug, qty: 1 })), p_name: customer.name, p_phone: customer.phone, p_email: customer.email });
      if (error) throw new Error('ثبت سفارش در سرور انجام نشد: ' + error.message);
      Object.assign(order, { id: data.order_id, number: data.order_no, token: data.token, total: data.total, remote: true });
    }
    const l = this.list(); l.unshift(order); this.save(l); store.set('ed_pending', order.id); return order;
  },
  async pay(id, ok, last4) {
    const l = this.list(); const o = l.find(x => x.id === id); if (!o) return null;
    if (o.remote && DB.on()) { const { data } = await DB.rpc('mock_pay', { p_order: o.id, p_token: o.token, p_success: ok, p_card_last4: last4 || null }); if (data?.ref_id) o.ref = data.ref_id; }
    o.status = ok ? 'paid' : 'failed';
    if (ok) { o.paidAt = new Date().toISOString(); o.ref = o.ref || 'MOCK-' + Math.floor(1e9 + Math.random() * 9e9); Cart.clear(); }
    this.save(l); store.del('ed_pending'); return o;
  },
  cancel(id) { const l = this.list(); const o = l.find(x => x.id === id); if (o && o.status === 'pending') { o.status = 'canceled'; this.save(l); } store.del('ed_pending'); return o; },
  async mine() {
    if (DB.on()) {
      const u = await Auth.user();
      if (u) {
        const { data } = await DB.select('orders', t => t.select('id,order_no,status,total,created_at,paid_at,gateway_ref,order_items(product_slug,product_kind,title,unit_price)').order('created_at', { ascending: false }));
        if (data) return data.map(o => ({ id: o.id, number: o.order_no, status: o.status, total: o.total, createdAt: o.created_at, paidAt: o.paid_at, ref: o.gateway_ref, items: (o.order_items || []).map(i => ({ slug: i.product_slug, kind: i.product_kind, title: i.title, price: i.unit_price })) }));
      }
    }
    return this.list();
  },
  purchased(list) { const seen = new Map(); list.filter(o => o.status === 'paid').forEach(o => o.items.forEach(i => { if (!seen.has(i.slug)) seen.set(i.slug, { ...i, orderNo: o.number, at: o.paidAt || o.createdAt }); })); return [...seen.values()]; }
};

/* ───────── اعتبارسنجی فرم‌ها ───────── */
const luhn = n => { let s = 0; [...n].reverse().forEach((d, i) => { let x = +d; if (i % 2 === 1) { x *= 2; if (x > 9) x -= 9; } s += x; }); return s % 10 === 0; };
const RULES = {
  required: (v, el) => (el.type === 'checkbox' ? el.checked : v.trim() !== '') ? '' : (el.type === 'checkbox' ? 'پذیرش این مورد الزامی است' : 'این فیلد الزامی است'),
  name: v => !v || /^[\u0600-\u06FFa-zA-Z\u200c\s.'-]{2,40}$/.test(v) ? '' : 'نام را با حروف و بین ۲ تا ۴۰ نویسه وارد کنید',
  email: v => !v || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'ایمیل معتبر نیست (مثال: name@example.com)',
  phone: v => !v || /^09\d{9}$/.test(v) ? '' : 'شماره همراه باید ۱۱ رقم و با ۰۹ شروع شود',
  password: v => !v || (v.length >= 8 && /[A-Za-z]/.test(v) && /\d/.test(v)) ? '' : 'رمز عبور حداقل ۸ نویسه و شامل حرف و عدد باشد',
  card: v => !v || (/^\d{16}$/.test(v) && luhn(v)) ? '' : 'شماره کارت ۱۶ رقمی معتبر وارد کنید',
  cvv: v => !v || /^\d{3,4}$/.test(v) ? '' : 'CVV2 باید ۳ یا ۴ رقم باشد',
  month: v => !v || (/^\d{1,2}$/.test(v) && +v >= 1 && +v <= 12) ? '' : 'ماه بین ۱ تا ۱۲',
  year: v => !v || /^\d{2}$/.test(v) ? '' : 'سال دو رقمی',
  otp: v => !v || /^\d{5,6}$/.test(v) ? '' : 'رمز پویا ۵ یا ۶ رقم است'
};
function validate(el) {
  const raw = el.type === 'checkbox' ? '' : el.value;
  const v = el.dataset.digits !== undefined ? toEn(raw).replace(/[\s-]/g, '') : raw;
  let msg = '';
  for (const r of (el.dataset.v || '').split(',').filter(Boolean)) {
    const [k, arg] = r.split(':');
    if (k === 'min') msg = v.trim().length >= +arg || !v ? '' : `حداقل ${toFa(arg)} نویسه وارد کنید`;
    else if (k === 'max') msg = v.length <= +arg ? '' : `حداکثر ${toFa(arg)} نویسه مجاز است`;
    else if (k === 'match') msg = v === ($(arg)?.value ?? '') ? '' : 'مقدار با فیلد قبلی یکسان نیست';
    else if (k === 'equals') msg = v === (window.__captcha || '') ? '' : 'کد امنیتی نادرست است';
    else if (RULES[k]) msg = RULES[k](v, el);
    if (msg) break;
  }
  let out = el.closest('.fd')?.querySelector('.err');
  if (!out) { out = document.createElement('small'); out.className = 'err'; out.id = (el.id || el.name || uid().slice(0, 6)) + '-err'; (el.closest('.fd') || el.parentNode).appendChild(out); }
  el.setAttribute('aria-describedby', out.id); el.setAttribute('aria-invalid', msg ? 'true' : 'false');
  out.textContent = msg; out.hidden = !msg; return !msg;
}
function bindForm(form, handler) {
  if (!form) return;
  form.setAttribute('novalidate', '');
  $$('[data-digits]', form).forEach(el => el.addEventListener('input', () => { const p = el.selectionStart; el.value = toEn(el.value); if (el.dataset.group) el.value = el.value.replace(/\D/g, '').slice(0, 16).replace(/(\d{4})(?=\d)/g, '$1 '); try { el.setSelectionRange(p, p); } catch { /* نوع ورودی انتخاب را پشتیبانی نمی‌کند */ } }));
  $$('[data-v]', form).forEach(el => { el.addEventListener('blur', () => { if (el.value || el.dataset.touched) validate(el); el.dataset.touched = '1'; }); el.addEventListener('input', () => { if (el.getAttribute('aria-invalid') === 'true') validate(el); }); });
  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (form.dataset.busy) return;
    const bad = $$('[data-v]', form).filter(el => !el.closest('[hidden]')).filter(el => !validate(el));
    const status = $('.form-status', form);
    if (bad.length) { bad[0].focus(); if (status) { status.textContent = 'لطفاً فیلدهای مشخص‌شده را اصلاح کنید.'; status.className = 'form-status bad'; } return; }
    const hp = form.elements.website; if (hp && hp.value) return;   // honeypot
    const vals = {}; $$('input,select,textarea', form).forEach(el => { if (!el.name || el.closest('[hidden]')) return; if (el.type === 'checkbox') vals[el.name] = el.checked; else if (el.type === 'radio') { if (el.checked) vals[el.name] = el.value; } else vals[el.name] = el.dataset.digits !== undefined ? toEn(el.value).replace(/[\s-]/g, '') : el.value.trim(); });
    const btn = $('[type=submit]', form); form.dataset.busy = '1'; btn && (btn.disabled = true); btn?.classList.add('loading');
    try { await handler(vals, form); } catch (err) { if (status) { status.textContent = err.message || 'خطایی رخ داد'; status.className = 'form-status bad'; } else toast(err.message || 'خطایی رخ داد'); }
    finally { delete form.dataset.busy; btn && (btn.disabled = false); btn?.classList.remove('loading'); }
  });
}
function setStatus(form, msg, ok = true) { const s = $('.form-status', form); if (!s) return toast(msg); s.textContent = msg; s.className = 'form-status ' + (ok ? 'ok' : 'bad'); }
$$('[data-toggle-pass]').forEach(b => b.addEventListener('click', () => { const i = $(b.dataset.togglePass); const show = i.type === 'password'; i.type = show ? 'text' : 'password'; b.setAttribute('aria-pressed', show); b.textContent = show ? 'مخفی' : 'نمایش'; }));

/* ───────── بازدید هوشمند ───────── */
const visitorId = () => { let v = store.get('ed_vid', null); if (!v) { v = uid(); store.set('ed_vid', v); } return v; };
function smartView(type, slug, base = 0) {
  const out = $$('[data-views]'); const set = n => out.forEach(e => { e.textContent = toFa(n); e.closest('[data-views-wrap]')?.removeAttribute('hidden'); });
  const dk = type + ':' + slug;
  (async () => {
    let n = base + (store.get('ed_views', {})[dk] || 0);
    if (DB.on()) { const { data } = await DB.rpc('get_views', { p_type: type, p_slug: slug }); if (typeof data === 'number') n = data; }
    set(n);
  })();
  if (/bot|crawl|spider|headless|lighthouse|preview/i.test(navigator.userAgent) || navigator.webdriver || document.prerendering) return;
  let ms = 0, active = false, done = false;
  ['scroll', 'pointerdown', 'keydown', 'touchstart', 'mousemove'].forEach(ev => addEventListener(ev, () => { active = true; }, { passive: true }));
  const tick = setInterval(() => { if (document.visibilityState === 'visible' && active) ms += 500; if (ms >= 6000 && !done) { done = true; clearInterval(tick); commit(); } }, 500);
  async function commit() {
    const day = new Date().toISOString().slice(0, 10), k = 'ed_seen_' + dk;
    try { if (localStorage.getItem(k) === day) return; localStorage.setItem(k, day); } catch { /* noop */ }
    if (DB.on()) { const { data } = await DB.rpc('register_view', { p_type: type, p_slug: slug, p_visitor: visitorId() }); if (typeof data === 'number') set(data); }
    else { const v = store.get('ed_views', {}); v[dk] = (v[dk] || 0) + 1; store.set('ed_views', v); set(base + v[dk]); }
  }
}

/* ───────── هدر: وضعیت کاربر، سبد، منوی موبایل، خبرنامه ───────── */
Cart.badge();
(async () => { const u = await Auth.user(); $$('[data-user-link]').forEach(a => { a.setAttribute('href', href(u ? 'account' : 'login')); a.setAttribute('title', u ? (u.display_name || 'حساب کاربری') : 'ورود / ثبت‌نام'); a.classList.toggle('on', !!u); }); })();
const mb = $('#menu-btn'), nav = $('#main-nav');
if (mb && nav) { mb.addEventListener('click', () => { const o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); }); document.addEventListener('keydown', e => { if (e.key === 'Escape') { nav.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); } }); }
const hdr = $('.top'); if (hdr) { const f = () => hdr.classList.toggle('scrolled', scrollY > 8); addEventListener('scroll', f, { passive: true }); f(); }
$$('form[data-form=newsletter]').forEach(f => bindForm(f, async v => {
  const { error } = DB.on() ? await DB.insert('newsletter_subscribers', { email: v.email }) : { error: null };
  if (error && !/duplicate|23505/.test(error.message + (error.code || ''))) throw new Error('ثبت انجام نشد، دوباره تلاش کنید');
  if (!DB.on()) { const l = store.get('ed_news', []); if (!l.includes(v.email)) l.push(v.email); store.set('ed_news', l); }
  f.reset(); setStatus(f, 'عضویت شما در خبرنامه ثبت شد. سپاسگزاریم!');
}));

window.ED = { cfg, P, $, $$, toEn, toFa, money, esc, uid, store, toast, href, go, DB, Auth, Cart, Orders, bindForm, setStatus, validate, smartView, jalali, isLocal };
document.dispatchEvent(new Event('ed:ready'));
})();

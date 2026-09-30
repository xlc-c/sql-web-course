/* ================= 状态 ================= */
let db = null;
let SQL = null;
const store = {
  key: 'sql-course-v1',
  data: { done: {}, code: {}, current: null },
  load() {
    try { const s = localStorage.getItem(this.key); if (s) this.data = Object.assign(this.data, JSON.parse(s)); } catch (e) {}
  },
  save() { try { localStorage.setItem(this.key, JSON.stringify(this.data)); } catch (e) {} }
};
store.load();

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(t._tm); t._tm = setTimeout(() => t.classList.remove('show'), 2400);
}
function sqlHighlight(sql) {
  return esc(sql).replace(/\b(SELECT|FROM|WHERE|AND|OR|NOT|IN|LIKE|BETWEEN|ORDER BY|ORDER|BY|ASC|DESC|LIMIT|AS|GROUP|HAVING|COUNT|SUM|AVG|MIN|MAX|JOIN|INNER|LEFT|RIGHT|ON|WITH|CASE|WHEN|THEN|ELSE|END|DISTINCT|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|UNION|ALL|IS|NULL)\b/gi, '<span class="kw">$1</span>')
    .replace(/(--[^\n]*)/g, '<span class="cm">$1</span>');
}

/* ================= 数据库 ================= */
function b64ToBytes(b64) {
  const s = atob(b64); const n = s.length; const u = new Uint8Array(n);
  for (let i = 0; i < n; i++) u[i] = s.charCodeAt(i);
  return u;
}
async function initDB() {
  $('#boot-msg').textContent = '正在载入数据库引擎…';
  SQL = await initSqlJs({
    instantiateWasm: (imports, ok) => {
      WebAssembly.instantiate(b64ToBytes(WASM_B64), imports)
        .then(r => ok(r.instance))
        .catch(e => { $('#boot-msg').textContent = '引擎载入失败：' + e.message; });
      return {};
    }
  });
  $('#boot-msg').textContent = '正在准备练习数据…';
  db = new SQL.Database();
  db.run(INIT_SQL);
}

function execAll(d, sql) { return d.exec(sql); }
function lastResult(results) { return results.length ? results[results.length - 1] : null; }
function runSQL(sql, d) {
  d = d || db;
  const r = lastResult(execAll(d, sql));
  return r || { columns: [], values: [] };
}

/* ================= 结果渲染 ================= */
function renderResult(box, res, ms) {
  box.classList.add('show');
  if (!res.columns || res.columns.length === 0) {
    box.innerHTML = '<div class="empty">执行成功，没有返回数据（这可能是写入语句，或结果为空）。</div>';
    return;
  }
  let h = '<div class="meta">共 ' + res.values.length + ' 行 · 用时 ' + ms + ' ms' + (res.values.length > 100 ? ' · 仅显示前 100 行' : '') + '</div><table><thead><tr>';
  res.columns.forEach(c => h += '<th>' + esc(c) + '</th>');
  h += '</tr></thead><tbody>';
  res.values.slice(0, 100).forEach(row => {
    h += '<tr>';
    row.forEach(v => h += '<td>' + (v === null ? '<span style="color:#5a5a5a">（空）</span>' : esc(v)) + '</td>');
    h += '</tr>';
  });
  box.innerHTML = h + '</tbody></table>';
}
function renderError(box, e, sql) {
  box.classList.add('show');
  let tip = '';
  const m = String(e.message || e);
  if (/no such table/i.test(m)) tip = '提示：表名写错了。可用的表：animals（动物个体）、batches（批次）、projects（项目）、assignments（入组）。';
  else if (/no such column/i.test(m)) tip = '提示：列名写错了。点下方「参考答案」对照一下列名，或回忆本课讲的表结构。';
  else if (/syntax error/i.test(m)) tip = '提示：语法错误。常见原因：中文引号（应为英文单引号）、少了空格、逗号多余、关键词拼错。';
  else if (/incomplete input/i.test(m)) tip = '提示：语句不完整，检查括号、引号是否成对。';
  box.innerHTML = '<div class="err"><b>出错了：</b>' + esc(m) + (tip ? '<br>' + esc(tip) : '') + '</div>';
}

/* ================= 判题 ================= */
function normRows(res) {
  return res.values.map(r => r.map(v => v === null ? '∅' : String(v)).join('␟'));
}
function judge(userSql, ex) {
  const base = db.export();
  let ud = null, ad = null, uLast, aLast;
  try {
    ud = new SQL.Database(base);
    uLast = lastResult(execAll(ud, userSql)) || { columns: [], values: [] };
  } catch (e) { if (ud) ud.close(); return { pass: false, why: 'sql_error', err: e }; }
  try {
    ad = new SQL.Database(base);
    aLast = lastResult(execAll(ad, ex.answer)) || { columns: [], values: [] };
  } catch (e) { ud.close(); if (ad) ad.close(); return { pass: false, why: 'answer_error', err: e }; }
  let uRes = uLast, aRes = aLast;
  if (ex.verify) {
    try { uRes = runSQL(ex.verify, ud); } catch (e) { ud.close(); ad.close(); return { pass: false, why: 'sql_error', err: e }; }
    try { aRes = runSQL(ex.verify, ad); } catch (e) { ud.close(); ad.close(); return { pass: false, why: 'answer_error', err: e }; }
  }
  ud.close(); ad.close();
  const ordered = /order\s+by/i.test(ex.answer);
  if (uRes.values.length !== aRes.values.length)
    return { pass: false, why: 'row_count', un: uRes.values.length, an: aRes.values.length };
  let ur = normRows(uRes), ar = normRows(aRes);
  if (!ordered) { ur = ur.slice().sort(); ar = ar.slice().sort(); }
  if (ur.join('␞') === ar.join('␞')) return { pass: true, rows: aRes.values.length };
  return { pass: false, why: 'diff', un: uRes.values.length, an: aRes.values.length };
}

/* ================= 课程渲染 ================= */
function lessonById(id) {
  for (const g of COURSE.groups) for (const l of g.lessons) if (l.id === id) return l;
  return null;
}
function flatLessons() {
  const arr = [];
  COURSE.groups.forEach(g => g.lessons.forEach(l => arr.push(l)));
  return arr;
}
function exBlock(ex, liId) {
  const saved = store.data.code[ex.id] || ex.prefill || '';
  return `
  <section class="blk ex" id="ex-${ex.id}">
    <div class="ex-title"><span class="tag">练习</span>${esc(ex.title)}</div>
    <div class="ex-desc">${ex.desc}</div>
    <div class="bench">
      <div class="bench-head">
        <div class="dots"><i></i><i></i><i></i></div>
        <span class="b-label">练习区 · ${esc(ex.id)}</span><span class="spacer"></span>
      </div>
      <textarea class="code-input" spellcheck="false" data-ex="${ex.id}" placeholder="在这里写 SQL，然后点「运行」看结果，「提交判题」检查对错…">${esc(saved)}</textarea>
      <div class="bench-foot">
        <button class="btn btn-run" data-act="run" data-ex="${ex.id}">▶ 运行</button>
        ${ex.noJudge ? '' : `<button class="btn btn-ghost" data-act="judge" data-ex="${ex.id}">✓ 提交判题</button>`}
        <span class="hint">Ctrl + Enter 快捷运行</span>
      </div>
      <div class="result" id="res-${ex.id}"></div>
      <div class="judge" id="judge-${ex.id}"></div>
      <details class="ans"><summary>卡住了？查看参考答案</summary><pre class="code">${sqlHighlight(ex.answer)}</pre></details>
    </div>
  </section>`;
}
function exampleBlock(html) { return html; }

function renderLesson(id) {
  const l = lessonById(id);
  if (!l) return;
  store.data.current = id; store.save();
  const flat = flatLessons();
  const idx = flat.findIndex(x => x.id === id);
  const done = !!store.data.done[id];

  let body = `<div class="crumb">${esc(l.crumb)}</div>
    <h2 class="lesson-title">${esc(l.title)}</h2>
    <div class="lesson-sub">${l.sub}</div>`;
  body += l.html;
  (l.exercises || []).forEach(ex => body += exBlock(ex, id));
  if (l.after) body += l.after;

  $('#content').innerHTML = body;
  $('#content').closest('main').scrollTop = 0;
  window.scrollTo(0, 0);

  // 导航态
  document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.id === id));
  $('#nav-done').textContent = done ? '✓ 已完成（点击取消）' : '标记完成';
  $('#nav-done').classList.toggle('is-done', done);
  $('#nav-prev').style.visibility = idx === 0 ? 'hidden' : 'visible';
  $('#nav-next').style.visibility = idx === flat.length - 1 ? 'hidden' : 'visible';

  // 动画
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .05 });
  document.querySelectorAll('section.blk').forEach(s => io.observe(s));

  // 事件绑定
  document.querySelectorAll('[data-act]').forEach(b => b.addEventListener('click', onExAction));
  document.querySelectorAll('textarea.code-input').forEach(t => {
    t.addEventListener('input', () => { store.data.code[t.dataset.ex] = t.value; store.save(); });
    t.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); execExercise(t.dataset.ex, false); }
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = t.selectionStart;
        t.value = t.value.slice(0, s) + '  ' + t.value.slice(t.selectionEnd);
        t.selectionStart = t.selectionEnd = s + 2;
      }
    });
  });
  // 可运行示例
  document.querySelectorAll('[data-demo]').forEach(b => b.addEventListener('click', () => {
    const el = document.getElementById(b.dataset.demo);
    const box = document.getElementById(b.dataset.demo + '-res');
    if (!el || !box) return;
    const sql = el.textContent;
    b.disabled = true;
    setTimeout(() => {
      try { const t0 = performance.now(); const r = runSQL(sql); renderResult(box, r, (performance.now() - t0).toFixed(1)); }
      catch (e) { renderError(box, e, sql); }
      b.disabled = false;
    }, 30);
  }));
  $('aside').classList && $('aside').classList.remove('open');
  updateProgress();
}

function onExAction(e) {
  const id = e.target.dataset.ex;
  execExercise(id, e.target.dataset.act === 'judge');
}
function findEx(id) {
  for (const g of COURSE.groups) for (const l of g.lessons)
    for (const ex of (l.exercises || [])) if (ex.id === id) return ex;
  return null;
}
function execExercise(id, doJudge) {
  const t = document.querySelector(`textarea[data-ex="${id}"]`);
  const box = $('#res-' + id), jbox = $('#judge-' + id);
  const ex = findEx(id);
  const sql = t.value.trim();
  if (!sql) { toast('先写点 SQL 再运行'); return; }
  if (ex.verify) {
    // 写入类练习：在独立副本中执行，不动公共数据
    const d2 = new SQL.Database(db.export());
    try {
      const t0 = performance.now();
      const results = execAll(d2, sql);
      const ms = (performance.now() - t0).toFixed(1);
      let last = lastResult(results);
      if (!last) last = runSQL(ex.verify, d2);
      renderResult(box, last, ms);
      const meta = box.querySelector('.meta');
      if (meta) meta.innerHTML = '已在独立副本中执行（公共数据不受影响）' +
        (lastResult(results) ? '' : ' · 下方为验证查询结果') + '<br>' + meta.innerHTML;
    } catch (e2) { renderError(box, e2, sql); }
    d2.close();
  } else {
    try {
      const t0 = performance.now(); const r = runSQL(sql);
      renderResult(box, r, (performance.now() - t0).toFixed(1));
    } catch (e2) { renderError(box, e2, sql); }
  }
  if (doJudge) {
    const v = judge(sql, ex);
    jbox.classList.add('show');
    if (v.pass) {
      jbox.className = 'judge show pass';
      jbox.innerHTML = '✓ 正确！结果集与参考答案完全一致（' + v.rows + ' 行）。' + (ex.explain ? '<br>' + esc(ex.explain) : '');
      markExDone(id);
    } else if (v.why === 'sql_error') {
      jbox.className = 'judge show fail';
      jbox.innerHTML = '✗ SQL 本身出错了，先看上面的报错提示改一改。';
    } else if (v.why === 'row_count') {
      jbox.className = 'judge show fail';
      jbox.innerHTML = '✗ 行数不对：你查出了 ' + v.un + ' 行，正确结果应为 ' + v.an + ' 行。检查筛选条件是不是太宽或太严了。';
    } else {
      jbox.className = 'judge show fail';
      jbox.innerHTML = '✗ 行数相同但内容不一致。逐列对照你的结果和「参考答案」的结果，看看是哪一列取错了。';
    }
  } else {
    jbox.classList.remove('show');
  }
}
function markExDone(exId) {
  // 一节课的所有练习都判对过 → 提示可标记完成
  store.data.code['_pass_' + exId] = '1'; store.save();
}

/* ================= 侧栏 & 进度 ================= */
function buildNav() {
  let h = '';
  COURSE.groups.forEach(g => {
    h += `<div class="nav-group"><div class="nav-gtitle">${esc(g.title)}</div>`;
    g.lessons.forEach(l => {
      const done = store.data.done[l.id];
      h += `<button class="nav-item ${done ? 'completed' : ''}" data-id="${l.id}"><span class="num">${l.num}</span><span>${esc(l.title)}</span><i class="done-dot"></i></button>`;
    });
    h += '</div>';
  });
  $('#nav').innerHTML = h;
  document.querySelectorAll('.nav-item').forEach(b => b.addEventListener('click', () => {
    renderLesson(b.dataset.id);
    document.querySelector('aside').classList.remove('open');
  }));
}
function updateProgress() {
  const flat = flatLessons();
  const n = flat.filter(l => store.data.done[l.id]).length;
  $('#p-text').textContent = n + ' / ' + flat.length;
  $('#p-fill').style.width = (n / flat.length * 100) + '%';
  document.querySelectorAll('.nav-item').forEach(el =>
    el.classList.toggle('completed', !!store.data.done[el.dataset.id]));
}

/* ================= 底部导航 ================= */
function navStep(d) {
  const flat = flatLessons();
  const idx = flat.findIndex(x => x.id === store.data.current);
  const ni = idx + d;
  if (ni >= 0 && ni < flat.length) renderLesson(flat[ni].id);
}
// 支持 #课号 直达（如 index.html#l6），自检模式除外
window.addEventListener('hashchange', () => {
  const id = location.hash.slice(1);
  if (id && lessonById(id) && id !== store.data.current) renderLesson(id);
});
$('#nav-prev').addEventListener('click', () => navStep(-1));
$('#nav-next').addEventListener('click', () => navStep(1));
$('#nav-done').addEventListener('click', () => {
  const id = store.data.current;
  if (!id) return;
  if (store.data.done[id]) { delete store.data.done[id]; toast('已取消完成标记'); }
  else {
    store.data.done[id] = Date.now();
    toast('已标记完成');
    setTimeout(() => navStep(1), 500);
  }
  store.save();
  const done = !!store.data.done[id];
  $('#nav-done').textContent = done ? '✓ 已完成（点击取消）' : '标记完成';
  $('#nav-done').classList.toggle('is-done', done);
  updateProgress();
});

/* ================= 进度导入导出 ================= */
$('#btn-export').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(store.data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'sql课程进度.json';
  a.click();
  URL.revokeObjectURL(a.href);
  toast('进度已导出为文件');
});
$('#btn-import').addEventListener('click', () => $('#import-file').click());
$('#import-file').addEventListener('change', e => {
  const f = e.target.files[0]; if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const d = JSON.parse(rd.result);
      if (typeof d !== 'object' || !d) throw new Error('格式不对');
      store.data = Object.assign({ done: {}, code: {}, current: null }, d);
      store.save(); buildNav(); updateProgress();
      if (store.data.current) renderLesson(store.data.current);
      toast('进度已恢复');
    } catch (err) { toast('导入失败：文件格式不对'); }
  };
  rd.readAsText(f);
  e.target.value = '';
});
$('#btn-reset').addEventListener('click', () => {
  if (!confirm('确定清空本机上的全部学习记录？（练习代码和完成标记都会删除）')) return;
  localStorage.removeItem(store.key);
  store.data = { done: {}, code: {}, current: null };
  buildNav(); updateProgress(); renderLesson(COURSE.groups[0].lessons[0].id);
  toast('已清空');
});
// 沙盒「重置练习数据」按钮（事件委托，按钮在课程内容里动态出现）
document.addEventListener('click', e => {
  if (e.target && e.target.id === 'reset-data') {
    ['animals','batches','projects','assignments','customers','products','orders','order_items']
      .forEach(t => db.run('DROP TABLE IF EXISTS ' + t + ';'));
    db.run(INIT_SQL);
    toast('练习数据已重置为初始状态');
    const rb = document.querySelector('#res-sandbox-ex');
    if (rb) rb.classList.remove('show');
  }
});
$('#menu-btn').addEventListener('click', () => document.querySelector('aside').classList.toggle('open'));
document.addEventListener('click', e => {
  const aside = document.querySelector('aside');
  if (aside.classList.contains('open') && !aside.contains(e.target) && e.target.id !== 'menu-btn')
    aside.classList.remove('open');
});

/* ================= 自检（#selftest 触发） ================= */
function selfTest() {
  const report = [];
  let pass = 0, fail = 0;
  // 1. 所有练习：答案 SQL 可执行、自判通过、结果非空
  flatLessons().forEach(l => (l.exercises || []).forEach(ex => {
    if (ex.noJudge) return;
    const v = judge(ex.answer, ex);
    if (!v.pass) {
      report.push('FAIL ' + ex.id + ' why=' + v.why + (v.err ? ' ' + (v.err.message || v.err) : ''));
      fail++;
    } else if (!ex.verify && v.rows === 0) {
      report.push('EMPTY ' + ex.id); fail++;
    } else pass++;
  }));
  // 2. 数据量校验
  try {
    ['animals','orders','order_items'].forEach(t =>
      report.push(t + '=' + runSQL('SELECT COUNT(*) AS n FROM ' + t).values[0][0]));
  } catch (e) { report.push('count ERR'); fail++; }
  document.body.dataset.selftest = 'pass=' + pass + ' fail=' + fail + ' | ' + report.join(' ; ');
}

/* ================= 启动 ================= */
(async function boot() {
  try {
    await initDB();
    buildNav(); updateProgress();
    const hashId = location.hash.slice(1);
    const start = (hashId && lessonById(hashId)) ? hashId
      : (store.data.current && lessonById(store.data.current)
        ? store.data.current : COURSE.groups[0].lessons[0].id);
    renderLesson(start);
    const counts = {};
    ['animals','batches','projects','assignments','customers','products','orders','order_items'].forEach(t => {
      counts[t] = runSQL('SELECT COUNT(*) AS n FROM ' + t).values[0][0];
    });
    document.body.dataset.boot = 'ok lessons=' + flatLessons().length + ' ' +
      Object.entries(counts).map(([k, v]) => k + '=' + v).join(',');
    if (location.hash === '#selftest') selfTest();
    $('#boot').style.opacity = '0';
    setTimeout(() => $('#boot').remove(), 500);
  } catch (e) {
    document.body.dataset.boot = 'error: ' + (e.message || e);
    $('#boot-msg').textContent = '初始化失败：' + (e.message || e) + ' —— 请换用较新的 Chrome / Edge 浏览器打开。';
  }
})();

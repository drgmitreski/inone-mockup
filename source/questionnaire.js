(function(){
  var root = document.querySelector('[data-q]'); if (!root) return;
  var form = root.querySelector('form');
  var card = root.querySelector('[data-form-card]'), done = root.querySelector('[data-done]');
  var steps = [].slice.call(form.querySelectorAll('[data-step]'));
  var items = [].slice.call(root.querySelectorAll('[data-progress] li'));
  var bar = root.querySelector('[data-bar]'), err = root.querySelector('[data-error]');
  var back = root.querySelector('[data-back]'), next = root.querySelector('[data-next]'), note = root.querySelector('[data-stepnote]');
  var cur = 0;

  function q(sel, ctx){ return [].slice.call((ctx || form).querySelectorAll(sel)); }
  function shown(el){ for (var p = el; p && !p.hasAttribute('data-step'); p = p.parentElement) if (p.hidden) return false; return true; }
  function vals(name){ return q('[name="' + name + '"]:checked').filter(shown).map(function(i){ return i.value; }); }
  function when(el){
    return el.getAttribute('data-when').split('|').some(function(sp){
      var p = sp.split(':'), v = vals(p[0]);
      return p[1].split(',').some(function(x){ return v.indexOf(x) >= 0; });
    });
  }
  function blocked(){ return vals('urgent').indexOf('yes') >= 0; }
  function refresh(){
    // outer-first so nested conditions see their parent's visibility
    q('[data-when]').forEach(function(el){ el.hidden = !when(el); });
    q('[data-when]').forEach(function(el){ el.hidden = !when(el); });
    next.disabled = steps[cur] && blocked() && cur === 2;
  }
  function render(){
    steps.forEach(function(s, i){ s.hidden = i !== cur; });
    items.forEach(function(li, i){
      if (i === cur) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
      if (i < cur) li.setAttribute('data-done', ''); else li.removeAttribute('data-done');
    });
    bar.style.width = ((cur + 1) / steps.length * 100) + '%';
    back.hidden = cur === 0;
    next.textContent = cur === steps.length - 1 ? 'Send enquiry' : 'Continue';
    note.textContent = 'Step ' + (cur + 1) + ' of ' + steps.length;
    err.hidden = true;
    refresh();
  }
  function focusTop(sel){
    var h = (sel || card).querySelector('.q-h');
    var r = (sel || card).getBoundingClientRect();
    if (r.top < 0 || r.top > 200) window.scrollTo({ top: window.scrollY + r.top - 100, behavior: 'smooth' });
    if (h) h.focus({ preventScroll: true });
  }

  /* validation */
  function validDob(v){
    var m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(v); if (!m) return false;
    var d = new Date(+m[3], +m[2] - 1, +m[1]);
    return d.getFullYear() === +m[3] && d.getMonth() === +m[2] - 1 && d.getDate() === +m[1] && d < new Date() && +m[3] > 1900;
  }
  var checks = {
    dob: [validDob, 'Please enter a date like 04/09/1975.'],
    phone: [function(v){ return v.replace(/\D/g, '').length >= 8; }, 'Please enter a phone number we can call.'],
    email: [function(v){ return !v || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); }, 'That email doesn’t look right.']
  };
  function setErr(field, msg){
    field.classList.toggle('err', !!msg);
    var m = field.querySelector('.q-msg');
    if (msg) { if (!m) { m = document.createElement('span'); m.className = 'q-msg'; field.appendChild(m); } m.textContent = msg; }
    else if (m) m.remove();
  }
  function validate(step){
    var ok = true, first = null;
    function bad(el){ ok = false; first = first || el; }
    q('.q-field', step).forEach(function(f){
      if (!shown(f)) return;
      var inp = f.querySelector('input,select,textarea'); if (!inp) return;
      var v = inp.value.trim(), msg = '';
      if (inp.required && !v) msg = 'Required';
      else if (inp.dataset.v && v !== '' || (inp.dataset.v === 'email')) { var c = checks[inp.dataset.v]; if (c && !c[0](v)) msg = c[1]; }
      setErr(f, msg); if (msg) bad(f);
    });
    q('[data-req]', step).forEach(function(g){
      if (!shown(g)) return;
      var good = !!form.querySelector('[name="' + g.getAttribute('data-req') + '"]:checked');
      g.classList.toggle('q-invalid', !good); if (!good) bad(g);
    });
    err.hidden = ok;
    if (!ok && first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return ok;
  }

  /* summary */
  function label(i){ return i.getAttribute('data-label') || (i.nextElementSibling && i.nextElementSibling.textContent) || i.value; }
  function checkedLabels(name){ return q('[name="' + name + '"]:checked').filter(function(i){ return shown(i) && !i.hasAttribute('data-none'); }).map(label); }
  function val(n){ var e = form.elements[n]; return e ? e.value.trim() : ''; }
  function finish(){
    var first = val('fn'), sum = root.querySelector('[data-summary]');
    root.querySelector('[data-done-h]').textContent = 'Thanks' + (first ? ', ' + first : '') + '. We’ve got your enquiry.';
    root.querySelector('[data-done-p]').textContent = 'A member of our team will call you on ' + val('mob') + (val('time') !== 'Any time' ? ' (' + val('time').toLowerCase() + ')' : '') + ' within [CONFIRM: 1 business day]. They’ll go through your answers, tell you the full fee and find a time. Nothing is booked or charged until you say yes.';
    var rows = [
      ['Enquiring about', checkedLabels('svc').join(', ')],
      ['Name', first + ' ' + val('ln')],
      ['Date of birth', val('dob')],
      ['Contact', val('mob') + (val('em') ? ' · ' + val('em') : '')],
      ['Preferred clinic', val('clinic')],
      ['Referral', checkedLabels('ref').join('')]
    ];
    var extra = checkedLabels('womReason'); if (extra.length) rows.splice(1, 0, ['Women’s health', extra.join(', ')]);
    sum.textContent = '';
    var dl = document.createElement('dl'); dl.className = 'q-summary';
    rows.forEach(function(r){ if (!r[1]) return; var dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = r[0]; dd.textContent = r[1]; dl.appendChild(dt); dl.appendChild(dd); });
    sum.appendChild(dl);
    // things the team should talk through
    var flags = [];
    checkedLabels('implants').forEach(function(l){ if (l !== 'Not sure') flags.push('Implant or device: ' + l); else flags.push('Unsure about implants or devices'); });
    q('[data-flag]').forEach(function(g){
      if (!shown(g)) return;
      var r = g.querySelector('input:checked');
      if (r && g.getAttribute('data-flag').split(',').indexOf(r.value) >= 0) flags.push(g.querySelector('.q-q').textContent.replace(/\s*\?.*$/, '') + ': ' + label(r));
    });
    var p = vals('preg'); if (p.length && p[0] !== 'no') flags.push('Pregnancy: ' + (p[0] === 'yes' ? 'yes' : 'not sure'));
    var f = vals('famAneu'); if (f.length && f[0] !== 'no') flags.push('Family history of brain aneurysm or bleed: ' + (f[0] === 'yes' ? 'yes' : 'not sure'));
    var box = root.querySelector('[data-flags]'), ul = root.querySelector('[data-flag-list]');
    ul.textContent = ''; flags.forEach(function(t){ var li = document.createElement('li'); li.textContent = t; ul.appendChild(li); });
    box.hidden = !flags.length;
    card.hidden = true; done.hidden = false;
    focusTop(done);
  }

  function go(d){
    if (d > 0) {
      if (blocked()) { return; }
      if (!validate(steps[cur])) return;
      if (cur === steps.length - 1) { finish(); return; }
    }
    cur = Math.max(0, Math.min(steps.length - 1, cur + d));
    render(); focusTop();
  }
  next.addEventListener('click', function(){ go(1); });
  back.addEventListener('click', function(){ go(-1); });
  form.addEventListener('submit', function(e){ e.preventDefault(); go(1); });
  form.addEventListener('change', function(e){
    var t = e.target;
    if (t.type === 'checkbox' && t.name) {
      var grp = q('[name="' + t.name + '"]');
      if (t.hasAttribute('data-none') && t.checked) grp.forEach(function(i){ if (i !== t) i.checked = false; });
      else if (t.checked) grp.forEach(function(i){ if (i.hasAttribute('data-none')) i.checked = false; });
    }
    var g = t.closest('[data-req],.q-opts'); if (g) g.classList.remove('q-invalid');
    if (!err.hidden && !q('.q-invalid,.q-field.err').length) err.hidden = true;
    refresh();
  });
  form.addEventListener('input', function(e){
    var t = e.target;
    if (t.getAttribute('data-v') === 'dob') {
      var d = t.value.replace(/\D/g, '').slice(0, 8), o = d.slice(0, 2);
      if (d.length > 2) o += '/' + d.slice(2, 4); if (d.length > 4) o += '/' + d.slice(4);
      t.value = o;
    }
    var f = t.closest('.q-field'); if (f && f.classList.contains('err')) setErr(f, '');
  });
  root.querySelector('[data-restart]').addEventListener('click', function(){
    form.reset(); cur = 0; done.hidden = true; card.hidden = false; applyHash(); render(); focusTop();
  });

  /* #screening-enquiry--brain etc. pre-selects a scan */
  function applyHash(){
    var m = /^#screening-enquiry--(\w+)/.exec(location.hash); if (!m) return;
    var i = form.querySelector('[name="svc"][value="' + m[1] + '"]');
    if (i && !i.checked) { i.checked = true; refresh(); }
  }
  window.addEventListener('hashchange', applyHash);
  applyHash(); render();
})();

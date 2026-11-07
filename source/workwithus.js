(function(){
  var root = document.querySelector('[data-wwu]'); if (!root) return;
  var form = root.querySelector('form'), card = root.querySelector('[data-form-card]'), done = root.querySelector('[data-done]'), err = root.querySelector('[data-error]');
  function q(s){ return [].slice.call(form.querySelectorAll(s)); }
  function shown(el){ for (var p = el; p && p !== form; p = p.parentElement) if (p.hidden) return false; return true; }
  function vals(n){ return q('[name="' + n + '"]:checked').filter(shown).map(function(i){ return i.value; }); }
  function label(i){ return i.getAttribute('data-label') || i.value; }
  function refresh(){
    for (var k = 0; k < 2; k++) q('[data-when]').forEach(function(el){
      var ok = el.getAttribute('data-when').split('|').some(function(sp){ var p = sp.split(':'), v = vals(p[0]); return p[1].split(',').some(function(x){ return v.indexOf(x) >= 0; }); });
      el.hidden = !ok;
    });
  }
  var checks = {
    phone: [function(v){ return v.replace(/\D/g, '').length >= 8; }, 'Please enter a phone number we can call.'],
    email: [function(v){ return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); }, 'That email doesn’t look right.']
  };
  function setErr(f, msg){
    f.classList.toggle('err', !!msg);
    var m = f.querySelector('.q-msg');
    if (msg) { if (!m) { m = document.createElement('span'); m.className = 'q-msg'; f.appendChild(m); } m.textContent = msg; } else if (m) m.remove();
  }
  function validate(){
    var ok = true, first = null;
    function bad(el){ ok = false; first = first || el; }
    q('.q-field').forEach(function(f){
      if (!shown(f)) return;
      var i = f.querySelector('input,select,textarea'); if (!i || !i.required) return;
      var v = i.value.trim(), msg = '';
      if (!v) msg = 'Required'; else if (i.dataset.v && !checks[i.dataset.v][0](v)) msg = checks[i.dataset.v][1];
      setErr(f, msg); if (msg) bad(f);
    });
    q('[data-req]').forEach(function(g){
      if (!shown(g)) return;
      var good = !!form.querySelector('[name="' + g.getAttribute('data-req') + '"]:checked');
      g.classList.toggle('q-invalid', !good); if (!good) bad(g);
    });
    err.hidden = ok;
    if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return ok;
  }
  function labs(n){ return q('[name="' + n + '"]:checked').filter(shown).map(label).join(', '); }
  function finish(){
    var fn = form.elements.fn.value.trim();
    root.querySelector('[data-done-h]').textContent = 'Thanks' + (fn ? ', ' + fn : '') + '. We’ve got it.';
    var rows = [['Role', labs('role')], ['Name', fn + ' ' + form.elements.ln.value.trim()], ['Contact', form.elements.em.value.trim() + ' · ' + form.elements.mob.value.trim()], ['Where', labs('loc')], ['Type of work', labs('type')], ['Interests', [labs('sub'), labs('mods'), labs('areas')].filter(Boolean).join(', ')]];
    var host = root.querySelector('[data-summary]'); host.textContent = '';
    var dl = document.createElement('dl'); dl.className = 'q-summary';
    rows.forEach(function(r){ if (!r[1]) return; var dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = r[0]; dd.textContent = r[1]; dl.appendChild(dt); dl.appendChild(dd); });
    host.appendChild(dl);
    card.hidden = true; done.hidden = false;
    var r = done.getBoundingClientRect(); window.scrollTo({ top: window.scrollY + r.top - 100, behavior: 'smooth' });
    done.querySelector('.q-h').focus({ preventScroll: true });
  }
  form.addEventListener('submit', function(e){ e.preventDefault(); if (validate()) finish(); });
  form.addEventListener('change', function(e){
    var g = e.target.closest('[data-req]'); if (g) g.classList.remove('q-invalid');
    if (!err.hidden && !q('.q-invalid,.q-field.err').length) err.hidden = true;
    refresh();
  });
  form.addEventListener('input', function(e){ var f = e.target.closest('.q-field'); if (f && f.classList.contains('err')) setErr(f, ''); });
  root.querySelector('[data-restart]').addEventListener('click', function(){ form.reset(); done.hidden = true; card.hidden = false; refresh(); window.scrollTo({ top: 0 }); });
  refresh();
})();

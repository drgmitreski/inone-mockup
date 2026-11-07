(function(){
  var root = document.querySelector('.page[data-page="people"]'); if (!root) return;
  var tabs = [].slice.call(root.querySelectorAll('[data-people-tab]')), groups = [].slice.call(root.querySelectorAll('[data-people-group]'));
  function pick(k){
    if (!groups.some(function(g){ return g.getAttribute('data-people-group') === k; })) return;
    groups.forEach(function(g){ g.hidden = g.getAttribute('data-people-group') !== k; });
    tabs.forEach(function(t){ var on = t.getAttribute('data-people-tab') === k; t.setAttribute('aria-current', on ? 'page' : 'false'); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
  }
  tabs.forEach(function(t){ t.addEventListener('click', function(){ pick(t.getAttribute('data-people-tab')); }); });
  function fromHash(){ var m = /^#(?:people|radiologists)--(\w+)/.exec(location.hash); if (m) pick(m[1]); }
  window.addEventListener('hashchange', fromHash); fromHash();
})();

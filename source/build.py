import re, base64, io, sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image

P = os.path.join(HERE, 'pages') + '/'
C = os.path.join(HERE, 'images') + '/'
blobs = {
 'c2818184f6c46fa083fb199ff07c7bd0': C+'int_hero.jpg', '4f7582fc3b25026b63866ed6ac8caa42': C+'scr_hero.jpg',
 '1682394af6db5c537291e27217487aac': C+'edu_hero.jpg', '8f401ec21bd0d90a2526a6dc2aefd045': C+'int_uae.jpg',
 'b2aa635de34454597abc4cf9baf65540': C+'int_pae.jpg', 'ab7c4d5801ba22af43902a9521a7fb54': C+'int_y90.jpg',
 'a80d37ad97baf6234f1606dc67bc9639': C+'int_evlt.jpg', 'fb77486bcbdecbba5ccf28b09d2603eb': C+'int_thy.jpg',
 '4c7f1e74760b31362d05da69159e4006': C+'int_more.jpg', '87321787c845e212022fafae5d524a0c': C+'scr_vasc.jpg',
 'dd0afc9bee66b11276785156a43e7783': C+'scr_onc.jpg', 'a08e16d0250f826bdd41dd9640a59874': C+'scr_lung.jpg',
 '89db4104753359964200692de6d5b6a4': C+'scr_wom.jpg', '8ef3b369c862572a96ad80fd1c1148d3': C+'scr_abd.jpg',
 'cbbb73d220aab2050d6b2d747fe014db': C+'scr_heart.jpg', '0b186ac0d05108c0b0db4b77b02d1cdc': C+'edu_live.jpg',
 '7c1734259eb5311c81dd28047b998a0a': C+'edu_ondemand.jpg', '739e59a315095af2c78fbaca6bc02392': C+'edu_web.jpg',
 'aeecd815a9228dd18fbce30e28bfea0c': C+'edu_research.jpg', 'e267aef412d967484e86514f4f67a2c6': C+'edu_clin.jpg',
 'f171579f6c2260af58097206ac832897': C+'d87acb78-image.jpg',
 '7a1c9e52b3d4486fa0e1c2d3b4a59687': C+'radiographer.jpg',
 '3c5e7a9b1d2f4086a7b8c9d0e1f2a3b4': C+'deerpark_banner.jpg',
 '47ce6e5a4a0db0fcf7463dd3811c37fa': C+'medicare_bb.png',
 '04306ef66cb25900fa0a5802578dd5f8': C+'mont/m_angio.jpg',
 'c911005aab4d15705309e8487d50864f': C+'mont/m_ct.jpg',
 '43c02d11a0a34bc283b5717c9c0113da': C+'mont/m_teach.jpg',
 'b52772f1f0231a8401db80fc13554ec9': C+'mont/m_room.jpg',
 'c71ab575ef018919ece8b27b46865d46': C+'mont/m_lectern.jpg',
 '055a5d4a76c5208a0a82ef5aa5150189': C+'mont/m_qa.jpg',
 '97eee86d411cb8405565f1370dd9aaf1': C+'int_hero_real.jpg',
 'f748bbfaa0051b374f7c7117d8afeeb7': C+'scr_hero_real.jpg',
 '76ebeba8a8709811e46acb2360a8a2a0': C+'edu_hero_real.jpg',
 '2a0f90512375763fea0f6c8378a0d6e1': C+'edu_live_real.jpg',
}
def datauri(path):
    im = Image.open(path).convert('RGB')
    if im.width > 1400:
        im = im.resize((1400, int(im.height * 1400 / im.width)))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
uris = {k: datauri(v) for k, v in blobs.items()}

pages = [('Main', 'home'), ('Home-Warm', 'home-warm'), ('Patient-Portal', 'patients'), ('Clinician-Portal', 'referrers'), ('Portals', 'portals'),
         ('Diagnosis', 'diagnosis'), ('Intervention', 'intervention'), ('Screening', 'screening'), ('Screening-Enquiry', 'screening-enquiry'), ('Costs', 'costs'), ('Work-With-Us', 'work-with-us'), ('Radiographers', 'radiographers'), ('Sonographers', 'sonographers'), ('Education', 'education'), ('Radiologists', 'radiologists'), ('Research', 'research'), ('Clinics', 'clinics'), ('About', 'about')]
pid = dict(pages)
VARIANTS = [('Portals', 'portals-patient', 'patient'), ('Portals', 'portals-clinician', 'clinician')]

def body(fname):
    s = open(P + fname + '.dc.html').read()
    s = s[s.index('<x-dc>') + 6:s.index('</x-dc>')]
    s = re.sub(r'<helmet>.*?</helmet>', '', s, flags=re.S)
    return s

# Header
hdr = body('Header')
SETS = {
 'none': [('radiologists','Our radiologists','Radiologists.dc.html'),('radiographers','Our radiographers','Radiographers.dc.html'),('sonographers','Our sonographers','Sonographers.dc.html'),('clinics','Our clinics','Clinics.dc.html'),('about','About us','About.dc.html'),('work','Work with us','Work-With-Us.dc.html')],
 'patient': [('home','Patient home','Patient-Portal.dc.html'),('imaging','Imaging &amp; scans','Diagnosis.dc.html'),('procedures','Procedures','Intervention.dc.html'),('screening','Screening','Screening.dc.html'),('costs','Costs &amp; billing','Costs.dc.html'),('radiologists','Our radiologists','Radiologists.dc.html')],
 'clinician': [('home','Clinician home','Clinician-Portal.dc.html'),('refer','Refer a patient','Portals.dc.html#referral'),('pathways','Procedures &amp; pathways','Clinician-Portal.dc.html#tab-intervention'),('programs','Screening programs','Clinician-Portal.dc.html#tab-screening'),('education','Education &amp; CPD','Education.dc.html'),('support','Referrer support','Clinician-Portal.dc.html')],
}
def header(mode, active):
    clin = mode == 'clinician'
    accent = '#1D4A7E' if clin else '#5A4593'
    ctx = {
      'isPatient': mode == 'patient', 'isClin': clin, 'isNone': mode == 'none',
      'topBg': '#141838' if clin else '#FFFFFF', 'topFg': '#FFFFFF' if clin else '#1A1F4A',
      'topLine': '#141838' if clin else '#E3E1EC', 'logoInk': '#FFFFFF' if clin else '#214068',
      'logoSub': '#B3A6D4', 'subFg': '#B7B6CE' if clin else '#5E6080',
      'segBg': '#2A2F5C' if clin else '#EEEAF7', 'segCls': 'seg-dark' if clin else '',
      'patBg': '#5A4593' if mode == 'patient' else 'transparent',
      'patFg': '#FFFFFF' if mode == 'patient' else ('#D9D8E8' if clin else '#1A1F4A'),
      'clinBg': '#FFFFFF' if clin else 'transparent', 'clinFg': '#141838' if clin else '#1A1F4A',
      'patCur': 'page' if mode == 'patient' else 'false', 'clinCur': 'page' if clin else 'false',
      'navLabel': 'Clinician menu' if clin else ('Patient menu' if mode == 'patient' else 'Main menu'),
    }
    t = hdr
    def forrep(m):
        body_ = m.group(1); out = ''
        for i, lab, href in SETS[mode]:
            on = i == active
            d = {'l.href': href, 'l.label': lab, 'l.cur': 'page' if on else 'false'}
            out += re.sub(r'\{\{\s*(l\.[a-z]+)\s*\}\}', lambda mm: d[mm.group(1)], body_)
        return out
    t = re.sub(r'<sc-for[^>]*>(.*?)</sc-for>', forrep, t, flags=re.S)
    t = re.sub(r'<sc-if value="\{\{ (\w+) \}\}"[^>]*>(.*?)</sc-if>', lambda m: m.group(2) if ctx[m.group(1)] else '', t, flags=re.S)
    t = re.sub(r'\{\{\s*(\w+)\s*\}\}', lambda m: str(ctx[m.group(1)]), t)
    return t

def tabs(defs, first):
    out = ''
    for i, lab, c in defs:
        on = i == first
        out += '<button type="button" role="tab" data-tab="%s" data-color="%s" aria-selected="%s" style="min-height: 52px; padding: 0 22px; background: transparent; border: 0; border-bottom: 3px solid %s; margin-bottom: -1px; font-family: \'Montserrat\', sans-serif; font-weight: 600; font-size: 16px; color: %s; cursor: pointer">%s</button>\n' % (
            i, c, 'true' if on else 'false', c if on else 'transparent', c if on else '#5E6080', lab)
    return out
tabdefs = {
 'Patient-Portal': [('imaging', 'Imaging &amp; diagnosis', '#4A3A84'), ('screening', 'Screening', '#355E46'), ('intervention', 'Intervention', '#9A3623')],
 'Clinician-Portal': [('imaging', 'Imaging &amp; diagnosis', '#4A3A84'), ('screening', 'Screening', '#355E46'), ('intervention', 'Intervention', '#9A3623'), ('education', 'Education &amp; CPD', '#1D4A7E')],
}


heads = {
 'goran': ('d1349e826_PHOTO-18-43-33_inOne_white.jpg', 'Dr Goran Mitreski', '96.5px 105.2px', '-20.2px 0px'),
 'julian': ('85aed73d6_PHOTO-18-43-32_inOne_B_white.jpg', 'A/Prof Julian Maingard', '87.7px 86.8px', '-15.8px 0px'),
 'terry': ('2b2d0c497_New_doctor_matched_v2_inOneterry.jpg', 'A/Prof Terry Kok', '74.7px 112px', '-7.9px 0px'),
 'daniel': ('bbb1319b2_PHOTO-11-49-20_inOne_white.jpg', 'Dr Daniel Liu', '66.1px 88px', '-5px 0px'),
 'kevin': ('d243631f8_PHOTO-12-11-16_shade_matched_inOne.jpg', 'Dr Kevin Chen', '93.7px 138.9px', '-18.9px -0.8px'),
}
def headrep(m):
    f, name, size, pos = heads[m.group(1)]
    initials = re.search(r'>([A-Z]+)</span>$', m.group(0)).group(1)
    url = 'https://media.base44.com/images/public/69a9f3dc05d4f7f2914e64a9/' + f
    ring = 'border: 3px solid #FFFFFF; box-sizing: content-box; ' if 'border: 3px' in m.group(0) else ''
    return ('<span role="img" aria-label="%s" style="' + ring + 'position: relative; overflow: hidden; width: 56px; height: 56px; border-radius: 50%%; flex: none; background: #E9E4F5; color: #4A3A84; display: flex; align-items: center; justify-content: center; font-family: Montserrat, sans-serif; font-weight: 700; font-size: 17px">%s'
            '<span style="position: absolute; inset: 0; background: url(%s) no-repeat; background-size: %s; background-position: %s"></span></span>') % (name, initials, url, size, pos)

HEADP = {  # aspect w/h, head top, head bottom, face x (measured from the photos)
 'goran': (939/1024, .05, .38, .5), 'julian': (1024/1014, .10, .50, .5), 'terry': (683/1024, .05, .32, .48),
 'daniel': (769/1024, .10, .45, .5), 'kevin': (691/1024, .07, .32, .5)}
def portrep(m):
    key = m.group(1); f, name = heads[key][0], heads[key][1]
    a, t, bt, fx = HEADP[key]; BW, BH = 240, 300
    hf = bt - t; fy = (t + bt) / 2
    H = 0.36 * BH / hf; W = a * H
    k = max(BW / W, BH / H, 1); W *= k; H *= k
    x = min(0, max(BW - W, BW / 2 - fx * W)); y = min(0, max(BH - H, 0.30 * BH - fy * H))
    url = 'https://media.base44.com/images/public/69a9f3dc05d4f7f2914e64a9/' + f
    initials = re.search(r'>([A-Z]+)</span>$', m.group(0)).group(1)
    return ('<span role="img" aria-label="%s" style="position: relative; overflow: hidden; flex: none; width: 240px; height: 300px; border-radius: 14px; background: #E9E4F5; color: #4A3A84; display: flex; align-items: center; justify-content: center; font-family: Montserrat, sans-serif; font-weight: 700; font-size: 56px">%s'
            '<span style="position: absolute; inset: 0; background: url(%s) no-repeat; background-size: %.1fpx %.1fpx; background-position: %.1fpx %.1fpx"></span></span>') % (name, initials, url, W, H, x, y)
PUBS = json.load(open(os.path.join(HERE, 'pubs.json')))
NAMES = {'G': 'Dr Goran Mitreski', 'J': 'A/Prof Julian Maingard', 'T': 'A/Prof Terry Kok'}
def research_static(s):
    import html as H
    btns = ''
    for i, (k, lab) in enumerate([('all', 'All'), ('G', 'Mitreski'), ('J', 'Maingard'), ('T', 'Kok')]):
        on = i == 0
        btns += '<button type="button" data-filter="%s" aria-pressed="%s" style="min-height: 40px; padding: 0 16px; border-radius: 999px; border: 1.5px solid %s; background: %s; color: %s; font: inherit; font-weight: 600; font-size: 14px; cursor: pointer">%s</button>' % (k, 'true' if on else 'false', '#13294A' if on else '#C9D3E4', '#13294A' if on else '#FFFFFF', '#FFFFFF' if on else '#13294A', lab)
    s = re.sub(r'<sc-for list="\{\{ filters \}\}".*?</sc-for>', btns, s, flags=re.S)
    tpl = re.search(r'<sc-for list="\{\{ items \}\}"[^>]*>(.*?)</sc-for>', s, re.S)
    items = ''
    for p in PUBS:
        d = {'p.href': 'https://pubmed.ncbi.nlm.nih.gov/%s/' % p[0], 'p.y': p[1], 'p.j': H.escape(p[2]), 'p.t': H.escape(p[3]), 'p.a': H.escape(p[4]), 'p.who': ' · '.join(NAMES[c] for c in p[5])}
        li = re.sub(r'\{\{\s*(p\.[a-z]+)\s*\}\}', lambda mm: d[mm.group(1)], tpl.group(1))
        items += li.replace('<li ', '<li data-who="%s" ' % p[5], 1)
    s = s[:tpl.start()] + items + s[tpl.end():]
    return s.replace('{{ shown }}', '<span data-shown>%d</span>' % len(PUBS))
sections = ''
for f, p, variant in [(f, p, None) for f, p in pages] + VARIANTS:
    s = body(f)
    if variant:
        keep = {'patient': ['patient'], 'clinician': ['referral', 'clinical']}[variant]
        for aid in ('patient', 'referral', 'clinical'):
            if aid not in keep:
                s = re.sub(r'\s*<!--[^>]*-->\s*<article id="%s".*?</article>' % aid, '', s, flags=re.S)
        s = s.replace('mode="none" active="none"', 'mode="%s" active="%s"' % (variant, 'none' if variant == 'patient' else 'refer'), 1)
        s = s.replace('Choose your portal.', 'Your patient portal.' if variant == 'patient' else 'Clinician portals.')
        s = s.replace('repeat(auto-fit, minmax(340px, 1fr))', 'repeat(auto-fit, minmax(340px, 600px))' if variant == 'patient' else 'repeat(auto-fit, minmax(340px, 1fr))')
    s = re.sub(r'<dc-import name="Header" mode="([a-z]+)" active="([a-z]+)"[^>]*></dc-import>', lambda m: header(m.group(1), m.group(2)), s)
    if f in tabdefs:
        s = re.sub(r'<sc-for list="\{\{ tabs \}\}".*?</sc-for>', tabs(tabdefs[f], 'imaging'), s, flags=re.S)
        def ifrep(m):
            name = m.group(1).lower()
            return '<div data-panel="%s"%s>' % (name, '' if name == 'imaging' else ' hidden')
        s = re.sub(r'<sc-if value="\{\{ is([A-Za-z]+) \}\}"[^>]*>', ifrep, s)
        s = s.replace('</sc-if>', '</div>')
    if f == 'Research': s = research_static(s)
    s = re.sub(r'<span data-portrait="([a-z]+)"[^>]*>[A-Z]+</span>', portrep, s)
    s = re.sub(r'<span data-headshot="([a-z]+)"[^>]*>[A-Z]+</span>', headrep, s)
    s = re.sub(r'bb-([a-z]+)', lambda m: 'bb-%s-%s' % (m.group(1), p), s)
    sections += '<section class="page" data-page="%s"%s>\n%s\n</section>\n' % (p, '' if p == 'home' else ' hidden', s)

# links: X.dc.html#a -> #/page/a ; X.dc.html -> #/page
def linkrep(m):
    name, anchor = m.group(1), m.group(2)
    if name == 'Portals' and anchor == 'patient': return 'href="#portals-patient"'
    if name == 'Portals' and anchor in ('referral', 'clinical'): return 'href="#portals-clinician--%s"' % anchor
    return 'href="#%s%s"' % (pid[name], '--' + anchor if anchor else '')
sections = re.sub(r'href="([A-Za-z-]+)\.dc\.html(?:#([A-Za-z0-9_-]+))?"', linkrep, sections)
sections = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: uris[m.group(1)], sections)
assert '{{' not in sections, re.findall(r'.{60}\{\{.{40}', sections)[:3]
assert '/_blob/' not in sections

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>inOne Imaging — Website prototype</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@600;700&display=swap" rel="stylesheet">
<style>
''' + open(os.path.join(HERE, 'design.css')).read() + '''
</style>
</head>
<body>
''' + sections + '''<nav id="cmp" class="hide-sm" aria-label="Compare home page options" style="position: fixed; right: 16px; top: 136px; z-index: 50; display: flex; gap: 2px; padding: 2px; background: #FFFFFF; border: 1px solid #D5D2E2; border-radius: 999px; box-shadow: 0 6px 20px rgba(20,24,56,.18); font: 600 13px \\'Hanken Grotesk\\', system-ui, sans-serif">
<span style="padding: 6px 8px; color: #5E6080">Compare home:</span>
<a href="#home" style="padding: 6px 12px; border-radius: 999px; text-decoration: none; color: #1A1F4A">Current</a>
<a href="#home-warm" style="padding: 6px 12px; border-radius: 999px; text-decoration: none; color: #1A1F4A">Warm</a>
</nav>

<script>
(function(){
  function show(){
    var h = location.hash.replace(/^#\\/?/, '').split(/--|\\//);
    var page = h[0] || 'home', anchor = h[1];
    var target = document.querySelector('.page[data-page="' + page + '"]');
    if (!target) { page = 'home'; target = document.querySelector('.page[data-page="home"]'); }
    document.querySelectorAll('.page').forEach(function(s){ s.hidden = s !== target; });
    if (anchor && anchor.indexOf('tab-') === 0) { var tb = target.querySelector('button[data-tab="' + anchor.slice(4) + '"]'); if (tb) { tb.click(); tb.scrollIntoView({behavior: 'smooth', block: 'center'}); return; } }
    var el = anchor && target.querySelector('[id="' + anchor + '"]');
    if (el) el.scrollIntoView({behavior: 'smooth'}); else window.scrollTo(0, 0);
    var cmp = document.getElementById('cmp'); if (cmp) cmp.style.display = page.indexOf('home') === 0 ? 'flex' : 'none';
    document.title = 'inOne Imaging — ' + page.charAt(0).toUpperCase() + page.slice(1);
  }
  window.addEventListener('hashchange', show);
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="#"]');
    if (a) {
      var href = a.getAttribute('href');
      var key = href.slice(1).split('--')[0];
      if (!document.querySelector('.page[data-page="' + key + '"]')) {
        e.preventDefault();
        var cur = document.querySelector('.page:not([hidden])');
        var el = cur && cur.querySelector('[id="' + href.slice(1) + '"]');
        if (el) el.scrollIntoView({behavior: 'smooth'});
      }
      return;
    }
    var b = e.target.closest('button[data-tab]');
    if (!b) return;
    var list = b.parentElement, scope = list.parentElement;
    list.querySelectorAll('button[data-tab]').forEach(function(t){
      var on = t === b;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.style.borderBottomColor = on ? t.dataset.color : 'transparent';
      t.style.color = on ? t.dataset.color : '#5E6080';
    });
    scope.querySelectorAll('[data-panel]').forEach(function(p){ p.hidden = p.dataset.panel !== b.dataset.tab; });
  });
  document.addEventListener('click', function(e){
    var fb = e.target.closest('button[data-filter]'); if (!fb) return;
    var grp = fb.parentElement, page = fb.closest('.page'), k = fb.dataset.filter, n = 0;
    grp.querySelectorAll('button[data-filter]').forEach(function(x){ var on = x === fb; x.setAttribute('aria-pressed', on); x.style.background = on ? '#13294A' : '#FFFFFF'; x.style.color = on ? '#FFFFFF' : '#13294A'; x.style.borderColor = on ? '#13294A' : '#C9D3E4'; });
    page.querySelectorAll('li[data-who]').forEach(function(li){ var show = k === 'all' || li.dataset.who.indexOf(k) >= 0; li.hidden = !show; if (show) n++; });
    var sh = page.querySelector('[data-shown]'); if (sh) sh.textContent = n;
  });
  document.addEventListener('submit', function(e){ e.preventDefault(); });
  show();
})();
</script>
<script>
''' + open(os.path.join(HERE, 'questionnaire.js')).read() + '''
</script>
<script>
''' + open(os.path.join(HERE, 'workwithus.js')).read() + '''
</script>
</body>
</html>
'''
out = os.path.join(HERE, '..', 'index.html')
open(out, 'w').write(html)
print(out, len(html) // 1024, 'KB')

# HTML architecture

The skeleton, navigation, inline editing, and speaker-notes wiring for a craft-slides deck.
Everything is inline in one `.html` file. Read at Phase 3.

## Skeleton

```html
<!DOCTYPE html>
<html lang="en">  <!-- or lang="th" for a Thai-primary deck -->
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Deck title</title>
  <!-- Fonts: Google Fonts / Fontshare, with a Thai face in every stack if bilingual -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400&family=Hanken+Grotesk:wght@400;600;700&family=Noto+Serif+Thai:wght@400;600&display=swap" rel="stylesheet" />
  <style>
    :root { /* === THEME === palette + type scale from the chosen preset === */ }
    /* === PASTE viewport-base.css HERE (full) === */
    /* === SLIDE LAYOUTS — flex/grid on inner wrappers, never on .slide === */
    .reveal { opacity: 0; transform: translateY(32px);
      transition: opacity .7s cubic-bezier(.16,1,.3,1), transform .7s cubic-bezier(.16,1,.3,1); }
    .slide.visible .reveal { opacity: 1; transform: none; }
    .slide.visible .reveal:nth-child(2){transition-delay:.1s}
    .slide.visible .reveal:nth-child(3){transition-delay:.2s}
    .slide.visible .reveal:nth-child(4){transition-delay:.3s}
  </style>
</head>
<body>
  <div class="deck-viewport">
    <main class="deck-stage" id="deckStage">
      <section class="slide active" data-notes="What to say on the opening slide.">
        <div class="pane center"> … </div>
      </section>
      <!-- more <section class="slide" data-notes="…"> … -->
    </main>
  </div>
  <div class="deck-controls" id="deckControls"></div>
  <!-- inline editor + notes chrome injected/handled by the script below -->
  <script> /* === CONTROLLER === */ </script>
</body>
</html>
```

## Controller (stage scaling + navigation)

```js
class Deck {
  constructor() {
    this.slides = [...document.querySelectorAll('.slide')];
    this.stage = document.getElementById('deckStage');
    this.i = 0;
    this.scale(); addEventListener('resize', () => this.scale());
    this.keys(); this.touch(); this.wheel();
    this.show(0);
  }
  scale() {
    const f = Math.min(innerWidth / 1920, innerHeight / 1080);
    const x = (innerWidth - 1920 * f) / 2, y = (innerHeight - 1080 * f) / 2;
    this.stage.style.transform = `translate(${x}px,${y}px) scale(${f})`;
  }
  show(n) {
    this.i = Math.max(0, Math.min(n, this.slides.length - 1));
    this.slides.forEach((s, k) => {
      s.classList.toggle('active', k === this.i);
      s.classList.toggle('visible', k === this.i);
    });
    this.onChange && this.onChange(this.i);
  }
  next(){ this.show(this.i + 1) } prev(){ this.show(this.i - 1) }
  keys() {
    addEventListener('keydown', (e) => {
      if (document.body.classList.contains('editing')) return;
      if (['ArrowRight',' ','ArrowDown','PageDown'].includes(e.key)) { e.preventDefault(); this.next(); }
      if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) { e.preventDefault(); this.prev(); }
      if (e.key === 'Home') this.show(0);
      if (e.key === 'End') this.show(this.slides.length - 1);
    });
  }
  touch() {
    let x = 0;
    addEventListener('touchstart', (e) => x = e.touches[0].clientX, { passive: true });
    addEventListener('touchend', (e) => { const d = e.changedTouches[0].clientX - x;
      if (Math.abs(d) > 45) (d < 0 ? this.next() : this.prev()); }, { passive: true });
  }
  wheel() {
    let lock = false;
    addEventListener('wheel', (e) => {
      if (lock || document.body.classList.contains('editing')) return;
      const p = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      (p > 0 ? this.next() : this.prev()); lock = true; setTimeout(() => lock = false, 900);
    }, { passive: true });
  }
}
const deck = new Deck();
```

Required: keyboard (arrows / space / PageUp-Down / Home / End), touch swipe, mouse wheel,
and the one-transform stage scale. Optional nav dots in `#deckControls`.

## Speaker notes

Each content slide carries a `data-notes="…"` — what the presenter says, not what's on the
slide. A press of **N** toggles a notes overlay for the current slide:

```js
const notes = document.createElement('div');
notes.style.cssText = 'position:fixed;left:0;right:0;bottom:0;max-height:30vh;overflow:auto;'
  + 'padding:18px 28px;background:rgba(10,10,10,.92);color:#eee;font:16px/1.5 system-ui;'
  + 'border-top:2px solid currentColor;z-index:9000;display:none;white-space:pre-wrap;';
document.body.appendChild(notes);
deck.onChange = (i) => { notes.textContent = deck.slides[i].dataset.notes || '(no notes)'; };
addEventListener('keydown', (e) => {
  if ((e.key === 'n' || e.key === 'N') && e.target.getAttribute('contenteditable') !== 'true')
    notes.style.display = notes.style.display === 'none' ? 'block' : 'none';
});
```

Notes never print and never show on the slide itself. They are the deck's teleprompter.

## Inline editing (on by default)

Edit text in place — hover the top-left hotzone or press **E**; ⌘/Ctrl+S saves to
`localStorage`. Do **not** use a CSS `~` sibling selector to reveal the toggle (the
`pointer-events:none` hover chain breaks) — use JS with a ~400 ms hide delay.

```js
(function editor(){
  const KEY = 'craft-slides:' + location.pathname;
  const SEL = 'h1,h2,h3,p,li,.kicker,.label,.stat-num,.stat-label';
  const els = [...document.querySelectorAll('.deck-stage ' + SEL)];
  els.forEach((el, i) => el.dataset.eid = 'e' + i);
  try { const s = JSON.parse(localStorage.getItem(KEY) || '{}');
        els.forEach(el => { if (s[el.dataset.eid] != null) el.innerHTML = s[el.dataset.eid]; }); } catch {}
  let on = false, t = null;
  const tgl = document.createElement('button');
  tgl.textContent = '✏'; tgl.title = 'Edit (E)';
  tgl.style.cssText = 'position:fixed;top:16px;left:16px;z-index:10001;width:44px;height:44px;'
    + 'border-radius:50%;border:1px solid currentColor;background:rgba(0,0,0,.8);color:#fff;'
    + 'cursor:pointer;opacity:0;pointer-events:none;transition:opacity .3s;';
  const hot = document.createElement('div');
  hot.style.cssText = 'position:fixed;top:0;left:0;width:84px;height:84px;z-index:10000;cursor:pointer;';
  document.body.append(hot, tgl);
  const save = () => { const d = {}; els.forEach(el => d[el.dataset.eid] = el.innerHTML);
                       localStorage.setItem(KEY, JSON.stringify(d)); };
  const set = (v) => { on = v; document.body.classList.toggle('editing', v);
    tgl.style.opacity = v ? 1 : 0; tgl.style.pointerEvents = v ? 'auto' : 'none';
    els.forEach(el => el.setAttribute('contenteditable', v)); if (!v) save(); };
  const show = (v) => { tgl.style.opacity = v ? 1 : (on ? 1 : 0); tgl.style.pointerEvents = v||on ? 'auto':'none'; };
  hot.onmouseenter = () => { clearTimeout(t); show(true); };
  hot.onmouseleave = () => { t = setTimeout(() => show(false), 400); };
  tgl.onmouseenter = () => clearTimeout(t);
  tgl.onmouseleave = () => { t = setTimeout(() => show(false), 400); };
  tgl.onclick = hot.onclick = () => set(!on);
  addEventListener('keydown', (e) => {
    if ((e.key === 'e' || e.key === 'E') && e.target.getAttribute('contenteditable') !== 'true') set(!on);
    if ((e.metaKey || e.ctrlKey) && (e.key === 's')) { e.preventDefault(); save(); }
  });
})();
```

If the user asks for a locked / export-only deck, omit the editor block.

## Images

Use relative `src` paths (not absolute filesystem paths) so PDF export and deploy resolve
them. Keep an `assets/` folder beside the HTML. Never repeat the same image across slides
except a logo on the cover and closing.

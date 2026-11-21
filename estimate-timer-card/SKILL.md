---
name: estimate-timer-card
description: When starting a long-running task or experiment, produce a time estimate first (by decomposing the work into its operations and comparing each with past cases), report the plan and the estimate, and present a countdown timer card set to that estimate — 7-segment style digits that count down the remaining time in white with a green progress bar, then switch to a red count-up "overrun" display if the work overruns. Use this for tasks and experiments expected to take roughly five minutes or longer, including detached background runs. Do not use it for quick tasks, casual chat, or when the user is in a hurry; the card costs on the order of 1,700 tokens to generate, so it is a ritual for work where the estimate genuinely matters.
---

# Estimate Timer Card

A long task reported only in words leaves the user with no feel for how the wait is going. Pairing the estimate with a live timer card makes the estimate a shared object: the user can see the remaining time shrink, and an overrun turns visibly red instead of silently stretching.

The card's three text labels live in a `LABELS` object in the template. The values shipped are Japanese, from the original use; localise them.

## Procedure

1. **Estimate first, by decomposition.** Break the work into the operations it actually involves (data loading, model or feature extraction, generation, evaluation, rendering, transfers). For each, compare with past cases: what is shared, what differs — features already cached or extracted from raw inputs, how many evaluation arms or grid points, output size. Past runtimes transfer only across the shared parts; never quote a past total for a differently-shaped job. (This procedure is bundled here so the skill stands alone.)
2. **Report the plan and the estimate in text**, as usual: what will be done, the conditions, and the total estimate.
3. **Present the timer card** with `TOTAL_SEC` set to the estimate in seconds and `STARTED_AT` set to the moment the work actually starts (epoch milliseconds — e.g. `date +%s%3N` when launching it). The card's script only runs when a client displays it, which may be long after the work began; baking the real start time in is what keeps the display honest for detached background runs. The same timestamp is the source for the actual-vs-estimate figure in step 5. (A device clock that differs from the agent's clock shifts the display by that difference — small compared with starting at first display.)
4. **Delivery timing matters: the card belongs in the launch message, before the work starts** — which means the work itself must run detached or delegated, so the completion report arrives as a later message. If the work will be done synchronously inside the same reply, do not present the card at all: a card created during the turn only becomes visible in the final message, where a timer for already-finished work is noise. In that case, report the actual elapsed time in the completion report instead.
5. **On completion, report the actual elapsed time against the estimate.** The card needs no stopping — if the work overran, it is already counting up in red as an overrun, which is the honest picture. Note the overrun and its cause briefly when reporting.

## Card specification

The design was settled over several iterations (2026-11-19). Keep it as specified; do not improvise the layout.

- Dark panel (`#17171a`, radius 16px, padding 15px 17px 13px) regardless of app theme — it is a clock face.
- Left: a small bold label, 16px — `LABELS.remaining` in muted grey (`#9a958c`) while counting down, `LABELS.overrun` in red (`#ff5a5a`) once over.
- Digits: **drawn 7-segment displays (SVG), not a font.** A segment font would need an external fetch, which is unreliable inside a card; drawn segments always work. Each digit is 7 rounded rects in a 40×72 drawing area inside a `-4 0 48 72` viewBox (the padding leaves room for the skew), group tilted `skewX(-4)`, lit segments filled with the display colour, unlit segments at `rgba(255,255,255,0.07)` so the ghost segments show like a real LCD. Colons are two circles. Main display height 46px.
- Counting down: digits white (`#ffffff`), showing the remaining time as HH:MM:SS. At zero the display flips: digits and label turn red and it counts **up** the overrun from 00:00:00.
- Under the display: a progress bar (height 7px, track `#333338`), filling green (`#2fbf71`) with the elapsed fraction of the estimate; at 100% it stays full and turns red (`#e5484d`).
- Bottom centre: `LABELS.planned` (15px, muted) plus the planned time in the same segment digits at 20px height, muted (`#c9c5bd`).
- **No buttons.** An earlier version had a restart button; it was removed. The estimate is a commitment, not a toy.
- Updates run inside the card (`setInterval` 200ms, computed from `Date.now()` against the persisted `startedAt`); no state writes per tick. Only re-render the digits when the displayed second or the over/under mode changes.

## Template

Replace `TOTAL_SEC` (the estimate, in seconds) and `STARTED_AT` (the work's start, epoch ms; 0 = start on first display). Everything else is used as-is.

```html
<style>
html, body { margin: 0; padding: 0; }
</style>
<div id="root"></div>
<script>
// The three labels live here; localise to the user's language.
var LABELS = { remaining: "残り", overrun: "超過", planned: "予定" };
var TOTAL_SEC = 60;
var STARTED_AT = 0;  // task start, epoch ms (e.g. `date +%s%3N` at launch); 0 = start on first display
TOTAL_SEC = Math.max(1, Math.round(Number(TOTAL_SEC) || 0));
var DEFAULTS = { startedAt: STARTED_AT || null };
function readState(defaults) {
  try {
    var s = window.hatchWidget && window.hatchWidget.getState(defaults);
    return (s && typeof s === "object") ? Object.assign({}, defaults, s) : defaults;
  } catch (e) { return defaults; }
}
function writeState(next) { try { window.hatchWidget.setState(next); } catch (e) {} }
var state = readState(DEFAULTS);
var SVGNS = "http://www.w3.org/2000/svg";
var SEG = { "0":"abcdef", "1":"bc", "2":"abged", "3":"abgcd", "4":"fgbc", "5":"afgcd", "6":"afedcg", "7":"abc", "8":"abcdefg", "9":"abcdfg" };
var SEG_RECT = { a:[7,0,26,8], g:[7,32,26,8], d:[7,64,26,8], f:[0,7,8,26], b:[32,7,8,26], e:[0,39,8,26], c:[32,39,8,26] };
var labelEl = null, fillEl = null, intervalId = null;
var mainDigits = [], mainColons = [], lastShown = "", lastMode = "";
function el(tag, text, style){ var n = document.createElement(tag); if (text != null) n.textContent = text; if (style) n.setAttribute("style", style); return n; }
function pad(n){ return (n < 10 ? "0" : "") + n; }
function fmt(sec){
  sec = Math.min(Math.max(Math.floor(sec), 0), 359999);
  var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
  return pad(h) + ":" + pad(m) + ":" + pad(s);
}
function buildDigit(heightPx){
  var svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("viewBox", "-4 0 48 72");
  svg.setAttribute("height", heightPx);
  svg.setAttribute("width", Math.round(heightPx * 48 / 72));
  var g = document.createElementNS(SVGNS, "g");
  g.setAttribute("transform", "skewX(-4)");
  var segs = {};
  "abcdefg".split("").forEach(function(name){
    var r = document.createElementNS(SVGNS, "rect");
    var v = SEG_RECT[name];
    r.setAttribute("x", v[0]); r.setAttribute("y", v[1]);
    r.setAttribute("width", v[2]); r.setAttribute("height", v[3]);
    r.setAttribute("rx", 3);
    r.setAttribute("fill", "rgba(255,255,255,0.07)");
    g.appendChild(r);
    segs[name] = r;
  });
  svg.appendChild(g);
  return { svg: svg, segs: segs };
}
function buildColon(heightPx, color){
  var svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("viewBox", "0 0 14 72");
  svg.setAttribute("height", heightPx);
  svg.setAttribute("width", Math.round(heightPx * 14 / 72));
  var dots = [];
  [26, 46].forEach(function(cy){
    var c = document.createElementNS(SVGNS, "circle");
    c.setAttribute("cx", 7); c.setAttribute("cy", cy); c.setAttribute("r", 3.6);
    c.setAttribute("fill", color);
    svg.appendChild(c);
    dots.push(c);
  });
  return { svg: svg, dots: dots };
}
function setDigit(d, ch, litColor){
  var on = SEG[ch] || "";
  "abcdefg".split("").forEach(function(name){
    d.segs[name].setAttribute("fill", on.indexOf(name) >= 0 ? litColor : "rgba(255,255,255,0.07)");
  });
}
function setDisplay(digits, colons, str, litColor){
  var di = 0;
  for (var i = 0; i < str.length; i++){
    if (str[i] === ":") continue;
    setDigit(digits[di], str[i], litColor);
    di++;
  }
  colons.forEach(function(c){ c.dots.forEach(function(d){ d.setAttribute("fill", litColor); }); });
}
function tick(){
  if (!state.startedAt) return;
  var elapsed = (Date.now() - state.startedAt) / 1000;
  var remain = TOTAL_SEC - elapsed;
  var over = remain < 0;
  var str = over ? fmt(-remain) : fmt(Math.ceil(remain));
  var mode = over ? "over" : "left";
  if (str !== lastShown || mode !== lastMode) {
    lastShown = str; lastMode = mode;
    setDisplay(mainDigits, mainColons, str, over ? "#ff5a5a" : "#ffffff");
    labelEl.textContent = over ? LABELS.overrun : LABELS.remaining;
    labelEl.style.color = over ? "#ff5a5a" : "#9a958c";
  }
  fillEl.style.width = (over ? 100 : Math.min(100, Math.max(0, elapsed / TOTAL_SEC * 100))) + "%";
  fillEl.style.background = over ? "#e5484d" : "#2fbf71";
}
function buildDisplay(heightPx, color){
  var wrap = el("div", null, "display:flex;align-items:center;gap:2px");
  var digits = [], colons = [];
  for (var i = 0; i < 8; i++){
    if (i === 2 || i === 5) {
      var col = buildColon(heightPx, color);
      colons.push(col); wrap.appendChild(col.svg);
    } else {
      var d = buildDigit(heightPx);
      digits.push(d); wrap.appendChild(d.svg);
    }
  }
  return { wrap: wrap, digits: digits, colons: colons };
}
function render(){
  var root = document.getElementById("root"); root.textContent = "";
  var box = el("div", null, "background:#17171a;border-radius:16px;padding:15px 17px 13px;box-sizing:border-box;max-width:560px;margin:0 auto;font-family:inherit");
  var row = el("div", null, "display:flex;align-items:center;gap:12px");
  labelEl = el("div", LABELS.remaining, "font-size:16px;font-weight:600;color:#9a958c;min-width:2.2em");
  row.appendChild(labelEl);
  var main = buildDisplay(46, "#ffffff");
  mainDigits = main.digits; mainColons = main.colons;
  row.appendChild(main.wrap);
  box.appendChild(row);
  var track = el("div", null, "margin-top:12px;height:7px;border-radius:4px;background:#333338;overflow:hidden");
  fillEl = el("div", null, "height:100%;width:0%;background:#2fbf71;border-radius:4px;transition:width 0.3s linear");
  track.appendChild(fillEl);
  box.appendChild(track);
  var planRow = el("div", null, "margin-top:10px;display:flex;align-items:center;justify-content:center;gap:9px");
  planRow.appendChild(el("div", LABELS.planned, "font-size:15px;color:#9a958c"));
  var plan = buildDisplay(20, "#c9c5bd");
  setDisplay(plan.digits, plan.colons, fmt(TOTAL_SEC), "#c9c5bd");
  planRow.appendChild(plan.wrap);
  box.appendChild(planRow);
  root.appendChild(box);
  lastShown = ""; lastMode = "";
  if (intervalId) clearInterval(intervalId);
  intervalId = setInterval(tick, 200);
  tick();
}
if (!state.startedAt) {
  state = { startedAt: STARTED_AT || Date.now() };
  writeState(state);
}
window.addEventListener("hatch-widget-state", function(e){
  if (e.detail && e.detail.state && e.detail.state.startedAt) { state = e.detail.state; tick(); }
});
render();
</script>
```

## Notes

- One card per task. If the plan branches into parallel sub-tasks, one card for the whole job's estimate, not one per branch.
- If the estimate is revised mid-task, report it; if the revision materially changes the cost, treat it as a branch point (see `branch-point-check`). Present a fresh card with the new total rather than editing the old one — the old card's overrun record is part of the history.
- The general card mechanism (state bridge, isolation, build rules) is covered by the `in-chat-card` skill; this skill only adds the estimation procedure and this card's design.

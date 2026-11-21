---
name: questionnaire-card
description: Present a set of questions to the user as an in-chat HTML questionnaire card with a per-question answer field (radio buttons for single choice, checkboxes for multiple choice, a text field for free writing), persistent widget state, and a submit button; then read the submitted answers back from the widget state. Use this whenever the user has to answer several questions in chat — sweepstakes and campaign questionnaires, intake or application question sets, preference surveys, or a confirmation checklist where each item needs an OK / "concern" judgement plus an optional memo. Prefer this over listing questions in prose, which forces the user to map answers back to questions by hand. Do not use it for a single question with one or two bounded choices (use the options widget), for a questionnaire document handed to another person to fill in elsewhere, or for general survey-design advice.
---

# Questionnaire Card

Answering questions in prose is tedious: the user has to quote or number each answer so it can be matched back to its question, and long lists get misaligned. A card with one labelled field per question removes that mapping work entirely — the answer arrives already attached to its question, in the widget state.

All user-visible strings in the template live in a `LABELS` object. The values shipped below are Japanese, from the original use; localise them to the user's language.

## When to use

- A questionnaire the user personally answers in this chat: sweepstakes/campaign surveys, application or registration question sets, preference or feedback questions.
- A confirmation checklist: a list of items the user must approve, where each item needs an OK / "concern" judgement and an optional one-line memo.

## Card specification

- One field per question, chosen by answer type:
  - Single choice → radio buttons.
  - Multiple choice → checkboxes.
  - Free writing → a text input or textarea.
  - Confirmation items → an OK / "concern" toggle plus a memo text field.
- Show the question text and its choices exactly as the source gives them. Do not reword a questionnaire's questions or invent choices it does not have.
- Render each choice as its own row styled like a small card — border, muted background, padding, rounded corners. The whole row is the tap target (the label wraps the input), and the styling should make that affordance obvious. Mark a selected row with an accent-coloured border, and keep the option text in the primary text colour so it stays readable on the row background.
- Give free-text fields the same treatment — the row-coloured background plus a clear border — so the input area is obvious at a glance, not just a faint outline on the card background.
- Cap the card's width (`max-width: 560px`, centred) so it does not stretch across a wide screen on iPad or PC; on a phone it simply fills the available width. Everything else is fluid — fixed pixel padding and margins, no absolute positioning — so larger screens change only the card's width, never its structure.
- Long text must wrap inside its row, never overflow it: put `overflow-wrap:anywhere` on question labels and choice rows. Japanese text wraps anywhere by itself, but an unbroken string (a long URL, a long English word) overflows a row without this. Verified with a ~180-character option and an unbroken URL at phone width.
- **Split by rendered height, not by item count.** The app stops displaying a card at roughly 4,000–4,300px of card height (measured 2026-11-19). Keep each card's estimated height at or under **3,000px** and split longer questionnaires into multiple cards. Estimate: fixed overhead (title, submit button, note, padding) ≈ 170px; a four-choice radio/checkbox question ≈ 250px (about 55px per option row plus the label; scale with the option count); a free-text field ≈ 150px. That works out to roughly 11 four-choice questions per card — when in doubt, render and measure rather than guess.
- Include a submit button. Submitting writes `submitted: true` into the widget state; it does not send anything anywhere by itself.
- The submit button spans the full width of the card, and its label is set slightly larger than the body text (17px, weight 600) while the button's own size and padding stay as in the template. Directly under it, show a small muted note (`LABELS.afterSubmitNote`) — the answers are only picked up when the user next sends a chat message, and the note sets that expectation so the user does not wait on the card itself.
- Free-text answers about the user's own experiences or opinions are the user's to write. Never pre-fill them with invented content; leave the field empty, or a placeholder that is clearly a hint, not an answer.

## Build recipe

Follow the general build recipe in the `in-chat-card` skill — theme variables, `createElement` + `textContent`, `render()` called unconditionally via the guarded `readState`/`writeState` bootstrap, state only through the bridge, no `localStorage` or `<form>`, a short `fallback_text`. (An early card rendered as an empty black bubble because a script error before rendering left only the dark shell; the guarded bootstrap is what prevents that.) The questionnaire-specific additions:

- Exception to the theme-variable rule, learned 2026-11-19: the stock surface and surface-muted variables can render nearly identical (in dark mode the card background and the choice-row backgrounds looked the same to the user). When layers must read as visually separate — card vs. rows — define local variables with explicit values per theme and a clear lightness gap between layers, overriding them under `html[data-theme="dark"]`, as the template skeleton does. Keep the accent colours from the theme variables.
- Always build the next state by spreading the current one (`Object.assign({}, state, { … })`); never rebuild it from a fixed key list, or keys added later (checklist state, timestamps) are silently wiped on the next tap.
- Text fields save on `input`, debounced, **without** re-rendering — re-rendering on blur replaces the submit button between pointer-down and click and swallows the user's first tap on it.
- Any edit after submission resets `submitted` to `false`, so the button label never promises a re-submit gate that the state does not enforce.

## Reading the answers back

- The user signals completion in chat (e.g. "submitted!"). Then read the widget's state and map each answer to its question.
- If `submitted` is false but answers exist, the user changed answers after submitting, or never submitted — ask before acting on them.
- Echo the answers back compactly before acting on them, so the user can catch a mistake.
- A submitted card is not permission to send anything externally. If the answers feed an outside submission (for example a sweepstakes entry form), the actual send still needs the user's explicit OK on the final content — follow your submission-safety skill if you have one; otherwise get that OK explicitly.
- For confirmation checklists: items marked OK are done and drop off the next list; items marked "concern" come back with their memo as fix-waiting items. The card itself is a working surface, not a record — keep the durable outcome in the relevant file or memory, not only in widget state.

## Template skeleton

A minimal working fragment with one radio group, one checkbox group, one text field, and a submit button. Duplicate the group builders per question; keep question definitions in the `QUESTIONS` array so the state shape stays uniform. The example question labels are illustrative; real cards use the source questionnaire's own wording.

```html
<style>
:root{
  --q-bg:#FFFFFF; --q-row:#EFEAE2; --q-text:#26221E;
  --q-muted:#6E675C; --q-border:#C9C2B2;
}
html[data-theme="dark"]{
  --q-bg:#211F1D; --q-row:#3E3A36; --q-text:#F4F0E8;
  --q-muted:#B6AEA1; --q-border:#6B655C;
}
</style>
<div id="root"></div>
<script>
// All user-visible strings live here; localise to the user's language.
var LABELS = {
  submit: "提出する",
  submitted: "提出済み（再提出で更新）",
  afterSubmitNote: "提出後、チャットすると反映されます"
};
var QUESTIONS = [
  { id: "q1", label: "質問1（単一選択）", type: "radio",
    options: ["選択肢A", "選択肢B"] },
  { id: "q2", label: "質問2（複数選択）", type: "check",
    options: ["選択肢X", "選択肢Y", "選択肢Z"] },
  { id: "q3", label: "質問3（自由記述）", type: "text" }
];
var DEFAULTS = { answers: {}, submitted: false };
function normalize(s) {
  s = (s && typeof s === "object") ? s : {};
  return Object.assign({}, DEFAULTS, s,
    { answers: (s.answers && typeof s.answers === "object") ? s.answers : {} });
}
var state;
try { state = normalize(window.hatchWidget.getState(DEFAULTS)); }
catch (e) { state = normalize(null); }
var pendingTimer = null, submitBtn = null;

function writeState(next) {
  try { window.hatchWidget.setState(next); } catch (e) {}
}
function save(next) {
  state = next;
  writeState(next);
  render();
}
function setAnswer(id, value) {
  var answers = Object.assign({}, state.answers);
  answers[id] = value;
  // spread the current state so other keys survive, and any edit after
  // submission un-submits: the button label must not promise a gate
  // that the state does not enforce
  save(Object.assign({}, state, { answers: answers, submitted: false }));
}
function el(tag, text, style) {
  var node = document.createElement(tag);
  if (text != null) node.textContent = text;
  if (style) node.setAttribute("style", style);
  return node;
}
function render() {
  var root = document.getElementById("root");
  root.textContent = "";
  var box = el("div", null,
    "background:var(--q-bg);color:var(--q-text);" +
    "border:1px solid var(--q-border);border-radius:12px;padding:16px;" +
    "font-family:inherit;box-sizing:border-box;max-width:560px;margin:0 auto");
  QUESTIONS.forEach(function (q) {
    var block = el("div", null, "margin-bottom:16px");
    block.appendChild(el("div", q.label,
      "font-weight:600;margin-bottom:6px;overflow-wrap:anywhere"));
    if (q.type === "radio" || q.type === "check") {
      q.options.forEach(function (opt) {
        var cur = state.answers[q.id];
        var selected = q.type === "radio" ? cur === opt
          : Array.isArray(cur) && cur.indexOf(opt) >= 0;
        var row = el("label", null,
          "display:block;margin:6px 0;padding:10px 12px;cursor:pointer;" +
          "border:1px solid " + (selected ? "var(--hatch-widget-accent)"
                                          : "var(--q-border)") + ";" +
          "border-radius:10px;background:var(--q-row);" +
          "color:var(--q-text);overflow-wrap:anywhere");
        var input = document.createElement("input");
        input.type = q.type === "radio" ? "radio" : "checkbox";
        input.name = q.id;
        input.checked = selected;
        input.addEventListener("change", function () {
          if (q.type === "radio") { setAnswer(q.id, opt); return; }
          var arr = Array.isArray(state.answers[q.id])
            ? state.answers[q.id].slice() : [];
          var i = arr.indexOf(opt);
          if (input.checked && i < 0) arr.push(opt);
          if (!input.checked && i >= 0) arr.splice(i, 1);
          setAnswer(q.id, arr);
        });
        row.appendChild(input);
        row.appendChild(document.createTextNode(" " + opt));
        block.appendChild(row);
      });
    } else {
      var ta = document.createElement("textarea");
      ta.rows = 3;
      ta.value = state.answers[q.id] || "";
      ta.setAttribute("style",
        "width:100%;box-sizing:border-box;background:var(--q-row);" +
        "color:var(--q-text);border:1px solid var(--q-border);" +
        "border-radius:8px;padding:8px;font:inherit;font-size:16px");
      // save on input, debounced, WITHOUT render(): rebuilding the DOM
      // on blur replaces the submit button between pointer-down and
      // click, which swallowed the user's first tap on Submit
      ta.addEventListener("input", function () {
        var answers = Object.assign({}, state.answers);
        answers[q.id] = ta.value;
        state = Object.assign({}, state, { answers: answers, submitted: false });
        if (submitBtn) submitBtn.textContent = LABELS.submit;
        clearTimeout(pendingTimer);
        pendingTimer = setTimeout(function () { writeState(state); }, 400);
      });
      block.appendChild(ta);
    }
    box.appendChild(block);
  });
  var btn = el("button", state.submitted ? LABELS.submitted : LABELS.submit,
    "display:block;width:100%;box-sizing:border-box;" +
    "background:var(--hatch-widget-accent);color:var(--hatch-widget-on-accent);" +
    "border:none;border-radius:8px;padding:12px 20px;cursor:pointer;" +
    "font-size:17px;font-weight:600");
  submitBtn = btn;
  btn.addEventListener("click", function () {
    clearTimeout(pendingTimer);
    save(Object.assign({}, state, { submitted: true }));
  });
  box.appendChild(btn);
  box.appendChild(el("div", LABELS.afterSubmitNote,
    "margin-top:8px;font-size:12px;color:var(--q-muted);text-align:center"));
  root.appendChild(box);
}
window.addEventListener("hatch-widget-state", function (e) {
  if (!e.detail || !e.detail.state) return;
  var a = document.activeElement;
  if (a && a.tagName === "TEXTAREA") return;  // user is typing; keep their text
  var next = normalize(e.detail.state);
  if (JSON.stringify(next) === JSON.stringify(state)) return;  // echo of our own write
  state = next;
  render();
});
render();
</script>
```

For the confirmation-checklist variant, use `var DEFAULTS = { checks: {}, memos: {}, submitted: false };` and replace the question blocks with one row per item: the item text, two buttons per item that store `checks[id] = "ok" | "concern"` (fixed codes, not the display text) through the same spread-and-save pattern, and a memo text input stored as `memos[id]` that saves on `input` with the same no-re-render discipline as the textarea above.

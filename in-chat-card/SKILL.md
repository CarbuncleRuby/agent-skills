---
name: in-chat-card
description: Build in-chat HTML cards (widgets) for the Muse chat — interactive explainers, mini games, timers, trackers, custom inputs, charts and diagrams drawn with SVG/Canvas, and message-style interactive text — using the widget HTML fragment plus the hatchWidget state bridge, and read the user's interactions back from the widget state. Use this whenever a reply would be better as something the user can touch, move, play with, or keep updated across days, rather than as plain text. Do not use it for question-and-answer sets or confirmation checklists (use the questionnaire-card skill), for a single question with one or two bounded choices (use the options widget), or for durable documents, dashboards and apps the user keeps and revisits (use an artifact / space instead). For a countdown tied to a task's time estimate, use the estimate-timer-card skill instead.
---

# In-Chat Card

A card is a small web page embedded in the chat. Muse writes the HTML/CSS/JavaScript for it on the spot; the app renders it inside the message flow. The card can also be presented on its own, with no message text around it — when the card itself is the answer (a timer, a game, a tracker), returning only the card is a legitimate reply shape.

**Host requirement:** this skill assumes a chat host that injects `window.hatchWidget` into the card's frame (Muse's widget mechanism). On a host without that bridge, the state calls below need an equivalent channel, and the persistence and read-back sections do not apply as written.

## The one bridge: hatchWidget

The card runs in an isolated frame. Its only channel to the outside is the object the app injects into the frame, `window.hatchWidget`:

- `window.hatchWidget.getState(defaults)` — read the card's saved state (seeded with `defaults` on first run).
- `window.hatchWidget.setState(nextState)` — replace the saved state wholesale. The state is stored server-side per card and persists across days.
- The `hatch-widget-state` event fires when the state changes; re-render from `event.detail.state`.

Everything the user does in the card reaches Muse only through this state. Nothing is pushed to Muse: Muse learns about interactions by reading the state (the `widget.state` tool) when preparing a reply, typically after the user's next chat message. The state read returns the latest saved state at the moment of reading — not a snapshot from when the user sent their message — plus a `version` counting the writes so far. A version-0 read returns `{}`, which means "still on the seeded defaults", not empty data. Never answer questions about a card's current contents from memory or from earlier messages; read the state first.

## Isolation: inside vs outside

Inside its own frame, the card's JavaScript has ordinary web-page powers:

- Full DOM control: build and restyle elements, run timers and animations, draw on Canvas or with SVG.
- Programmatic interaction: dispatch synthetic taps/clicks on its own elements, set input values, pre-select options, auto-advance steps, typewriter effects.
- Pointer interaction: per-element handlers, and `document.elementFromPoint` for stroke-style input (e.g. tracing across characters to colour them). Set `touch-action:none` on the interactive surface or the chat's scroll will steal the gesture.

Limits that remain inside:

- Actions gated on a genuine user gesture may refuse synthetic events: opening the keyboard, reading the clipboard, file pickers, audio/video autoplay with sound, fullscreen.
- No live external data fetching (images aside); the card works with what Muse put in it plus its saved state.
- Muse cannot push updates into a card unprompted; a card changes only when its own script changes it, or when it re-renders from newer state.

Outside the frame, the card can do nothing at all: it cannot touch the app's message bubbles, other cards, the chat input field, or any app UI, and Muse's scripts cannot be attached to native messages. A card can imitate a message bubble visually (see "Message-lookalike text" below), but it stays a card.

## Token cost

A card costs its full source in tokens, because Muse generates the code: a small interactive card runs to roughly 800 tokens where the same content as plain text would be about 50, and the source stays in the conversation context for the session. Reading state back is cheap (under ~100 tokens). Use cards when interaction, persistence, or visual structure earns the cost — not as decoration for ordinary text.

## Build recipe

These rules carry the lessons of real failures (an early card rendered as an empty black bubble, most likely a script error before first render).

- Style with the theme variables only (`--hatch-widget-bg`, `-surface`, `-surface-muted`, `-text`, `-muted`, `-border`, `-accent`, `-on-accent`, `-focus`, `-shadow`), each for its semantic role; the card must work in light and dark themes. One exception: a self-contained fixed-palette object (e.g. a clock face) may ignore the theme, provided every colour inside it — background and text — is set explicitly. Another exception: when layers must read as visually separate and the stock variables render nearly identical (card background vs. row background in dark mode), define local variables with explicit per-theme values and a clear lightness gap, overriding under `html[data-theme="dark"]`. Accent colours still come from the theme variables.
- Keep the JavaScript minimal, and build the DOM with `createElement` + `textContent`, not `innerHTML` string assembly.
- Call `render()` unconditionally — even if reading the saved state fails, the card must still draw. Use this guarded bootstrap so the rule survives a throwing bridge:
  ```js
  function readState(defaults) {
    try {
      var s = window.hatchWidget && window.hatchWidget.getState(defaults);
      return (s && typeof s === "object") ? Object.assign({}, defaults, s) : defaults;
    } catch (e) { return defaults; }
  }
  function writeState(next) { try { window.hatchWidget.setState(next); } catch (e) {} }
  // var state = readState(DEFAULTS); … render();  // render() last, outside any try that can skip it
  ```
- State discipline: read the complete state once, replace it wholesale on every mutation, re-render on the `hatch-widget-state` event. On the event, skip the re-render when the incoming state equals the current one (it may be the echo of the card's own write), and never rebuild the DOM while a text field inside the card has focus — rebuilding under the user swallows taps and loses typed text. Never use `localStorage`, `sessionStorage`, or a `<form>` element.
- The fragment is only a fragment: no `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` wrappers. Set `box-sizing: border-box`; cap width (`max-width: 560px`, centred) so wide screens do not stretch the card.
- Size limits (platform values, measured 2026-11; they can change): the HTML is stored whole and must stay under 1 MB — never inline audio/video or large images as base64; share real media files as attachments instead. Displayed height caps out at roughly 4,000–4,300px; budget **3,000px** of estimated rendered height per card and split by height (not by item count) when a card would grow past it.
- Long text must wrap, never overflow: `overflow-wrap:anywhere` on labels and rows (an unbroken URL or long English word overflows otherwise).
- Pass a short `fallback_text` naming the card.
- For complex layouts, verify before delivering: render the fragment in local Playwright Chromium at phone and desktop widths and check for overflow and breakage.

## Message-lookalike text (example calibration, measured 2026-11-19)

When a card should read like an ordinary app message, measure the host app's native text on the target device and match it. The method below is general; the numbers are one example calibration — an iPhone at 390 CSS px wide (screenshots 1170×2532, DPR 3), on the app version current at measurement time. They are device- and app-version-specific; re-measure if either changes.

- The app's message text: character advance 17.0 CSS px (i.e. font-size ≈ 17px), line pitch ≈ 21.7 CSS px.
- The card renders a specified font-size at about 98.5% of its nominal value. Setting `font-size: 17.2px` with `line-height: 1.28` matched the native advance and pitch.
- Left inset: both bubbles start at screen x = 16 CSS px; with the card's own box at `padding-left: 16px`, the text starts aligned with native text (confirmed visually).
- What cannot be matched: the card font's glyphs are drawn about 6% smaller in ink height than the app font's (44 vs 47 device px at the same advance). Ink height is baked into the font design — CSS has no glyph-height property, and scaling font-size up to match it also thickens strokes and widens the advance (a version built that way looked wrong and slightly bold; the 17.2px near-match was kept as final). Perfect typographic identity with native messages is not achievable unless the exact app font is available to the frame; say so rather than iterating forever.
- Measurement method, for re-checks: full-width Japanese characters advance exactly 1em, so font-size = (ink span of a line in device px ÷ its character count, with a small correction for the last glyph's ink width) ÷ DPR. Line pitch = distance between the tops of consecutive text lines. Glyph ink height = the height of a line's ink band; compare like-for-like glyph mixes (kanji lines vs kana lines differ).

## Reading interactions back

- After the user says they used the card, read its state and echo what you found compactly before acting on it (e.g. which characters are coloured, which items are ticked), so the user can catch a mistake.
- An interaction with a card is not permission for anything outside the card. If the card's contents feed an external action (a submission, a send), that action still needs the user's explicit OK on the final content — follow your submission-safety skill if you have one.
- The state shows the current values, not a history: intermediate steps the user took inside the card are not recoverable, only the latest saved state and its write count.

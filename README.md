# MotionGarden — Grow with every move 🌿

A responsive Arabic-first interactive Three.js garden experience, with calming original audio, a three-move mini-quest, a hand-tracking option, and touch/mouse fallback. No API keys, logins, accounts, or backend needed.

## Run it

1. Extract the ZIP.
2. Open a terminal in the `MotionGarden` folder.
3. Run `python -m http.server 8000` (or `npx serve .`).
4. Open `http://localhost:8000` in a browser.
5. Click **ادخلي الحديقة** to begin — browsers require a user gesture before playback.

**To use on mobile/iPad:** host with GitHub Pages / Netlify static hosting over HTTPS. The camera cannot generally run from plain `file://` or non-secure HTTP pages. Chrome, Safari, or Edge recent versions recommended; camera access requires permission.

## Experience controls
- The three on-screen buttons or keys `1`, `2`, `3` trigger sunrise, plant a flower, and breeze.
- Click-and-drag / swipe across the 3D scene to explore.
- The ♪ button opens independent water, birds, breeze, and subtle music volume toggles, plus master volume and mute.
- Camera button opens optional hand tracking via MediaPipe Hands. Open palm triggers sunrise, thumb-index pinch plants a flower, and waving palm changes the breeze. Camera inference runs locally in the browser. (Library/model files are loaded externally over HTTPS.)
- Restart runs a fresh three-move quest.

## Audio
The four small OGG loops in `assets/audio/` are **original synthesized nature-inspired ambiences and an original soft music pad**, not field recordings. Generate them again using `python generate_audio.py` (requires Python, NumPy, SciPy, FFmpeg). They are original and available for reuse in this project. They were created to ensure the working demo contains actual sounds without dependence on paid or hotlinked audio services. For a future production version, replace these with verified CC0 professional field recordings for more realistic audio.

## Tech and cost
- Three.js pinned at 0.180.0 from jsDelivr CDN (MIT license).
- MediaPipe Hands 0.4 from jsDelivr CDN (Apache 2.0, Google), loaded only when activated.
- Web Audio API for interaction chimes, original local OGG audio for ambience.
- HTML/CSS/JavaScript only. No build pipeline, keys, subscriptions or paid API.
- Static publishing on GitHub Pages is free for public repositories subject to provider terms.

## Notes
- Internet is required for the initial Three.js library load and for optional MediaPipe assets; the included audio loops are local files.
- Gesture detection quality varies with camera, lighting, hand position and hardware. Fallback touch/mouse buttons always remain available.
- This is a light movement/engagement prototype, not a fitness measurement or medical rehabilitation product.

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Clean Prompt</title>
<style>
:root{
  --bg1:#0066ff;
  --bg2:#0044cc;
  --bg3:#002288;
  --neon:#33aaff;
  --accent:#33aaff;
  --text-yellow:#ffd900;
  --glass: rgba(0,0,0,0.42);
  --glass-strong: rgba(0,0,0,0.6);
}

body{
  margin:0;
  padding:0;
  font-family:"Segoe UI", Arial, sans-serif;
  display:flex;
  align-items:center;
  justify-content:center;
  height:100vh;
  background: linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
  background-size:300% 300%;
  animation: fadeBlue 12s ease-in-out infinite alternate;
  transition: background 0.4s, color 0.3s;
}

@keyframes fadeBlue {
  0%{ background-position:0% 50%; filter:brightness(1.1); }
  50%{ background-position:50% 50%; filter:brightness(1.25); }
  100%{ background-position:100% 50%; filter:brightness(1.1); }
}

body.dark{
  background:black !important;
  animation:none;
}

.container{
  width:90%;
  max-width:700px;
  padding:30px;
  border-radius:20px;
  backdrop-filter:blur(16px);
  background:var(--glass);
  border:1px solid var(--accent);
  box-shadow:0 0 25px var(--accent);
  animation:softFade 4s ease-in-out infinite alternate;
}

@keyframes softFade {
  0%{ box-shadow:0 0 8px rgba(0,153,255,0.2); opacity:0.96; }
  100%{ box-shadow:0 0 20px rgba(0,153,255,0.35); opacity:1; }
}

.settings{
  text-align:right;
  margin-bottom:10px;
}

.icon{
  font-size:28px;
  cursor:pointer;
  color:#ffd900;
}

h2{
  text-align:center;
  color:var(--accent);
  text-shadow:0 0 10px var(--accent);
  margin-bottom:20px;
}

textarea{
  width:100%;
  height:150px;
  border-radius:12px;
  border:2px solid var(--accent);
  background:var(--glass-strong);
  color:var(--text-yellow);
  padding:12px;
  font-size:16px;
  resize:none;
  outline:none;
  animation:softFade 4s ease-in-out infinite alternate;
}

/* User-selectable text color */
.color-picker{
  margin-top:15px;
  display:flex;
  justify-content:center;
  gap:12px;
}
.color-picker input{
  width:50px;
  height:30px;
  border:none;
  outline:none;
  cursor:pointer;
  border-radius:6px;
}

button{
  margin-top:18px;
  width:100%;
  padding:14px;
  border-radius:12px;
  border:none;
  font-size:17px;
  cursor:pointer;
  background:var(--accent);
  color:#000;
  transition:0.3s;
  box-shadow:0 0 12px var(--accent);
}

button:hover{
  background:#0088dd;
}

.output{
  margin-top:20px;
  padding:18px;
  border-radius:12px;
  min-height:90px;
  border:2px solid var(--accent);
  background:var(--glass-strong);
  color:white;
  white-space:pre-line;
  opacity:0;
  transition:0.3s;
  animation:softFade 4s ease-in-out infinite alternate;
}

.output.show{
  opacity:1;
}
</style>
</head>
<body>

<div class="container">
  <div class="settings">
    <span id="modeIcon" class="icon" role="button" title="Toggle mode">☀️</span>
  </div>

  <h2>CLEAN PROMPT</h2>

  <textarea id="userInput" placeholder="Type here..."></textarea>

  <div class="color-picker" aria-hidden="false">
    <label style="color:var(--text-yellow); font-size:15px; align-self:center;">Text Color:</label>
    <input type="color" id="textColorPicker" value="#ffd900" title="Choose text color">
  </div>

  <button id="generateBtn" type="button">Generate Improved Prompt</button>

  <div id="output" class="output" aria-live="polite"></div>
</div>

<script>
/* Elements */
const userInput = document.getElementById('userInput');
const output = document.getElementById('output');
const generateBtn = document.getElementById('generateBtn');
const modeIcon = document.getElementById('modeIcon');
const textColorPicker = document.getElementById('textColorPicker');

/* Ensure functions are bound after DOM ready (they are here) */
modeIcon.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  modeIcon.textContent = document.body.classList.contains('dark') ? '🌙' : '☀️';
});

/* Change text color handler */
textColorPicker.addEventListener('input', () => {
  const color = textColorPicker.value;
  document.documentElement.style.setProperty('--text-yellow', color);
  userInput.style.color = color;
});

/* Keep a single typing interval reference to cancel previous typing */
let typingInterval = null;
function typeWriter(element, text){
  // cancel previous interval if exists
  if (typingInterval) {
    clearInterval(typingInterval);
    typingInterval = null;
  }
  element.textContent = '';
  element.classList.add('show');
  let i = 0;
  const speed = 16;
  typingInterval = setInterval(() => {
    if (i >= text.length) {
      clearInterval(typingInterval);
      typingInterval = null;
      return;
    }
    element.textContent += text.charAt(i);
    i++;
    element.scrollTop = element.scrollHeight;
  }, speed);
}

/* Minimal, robust refine logic */
function refinePrompt(raw){
  raw = (raw || '').trim();
  if (!raw) return null;

  const goal = raw.split(/[.?!]/)[0] || raw;
  const context = 'Any relevant background or assumptions.';
  const constraints = 'No strict constraints given.';
  const outputFormat = 'A clear, structured response.';
  const tone = 'Neutral, clear, and informative.';

  const final = [
    'Refined Prompt:',
    '',
    `• Objective: ${goal}`,
    `• Context: ${context}`,
    `• Constraints: ${constraints}`,
    `• Desired output: ${outputFormat}`,
    `• Tone: ${tone}`,
    '',
    'Instruction for AI:',
    `Please produce the requested output. ${goal}. Context: ${context}. Follow constraints: ${constraints}. Output format: ${outputFormat}. Use tone: ${tone}.`
  ].join('\n');

  return final;
}

/* Generate button: use event listener instead of inline onclick */
generateBtn.addEventListener('click', () => {
  try {
    const raw = userInput.value;
    if (!raw || raw.trim().length < 2) {
      typeWriter(output, 'Please write something meaningful.');
      return;
    }
    const refined = refinePrompt(raw);
    if (!refined) {
      typeWriter(output, 'Unable to refine prompt. Please provide more details.');
      return;
    }
    typeWriter(output, refined);
  } catch (err) {
    // show minimal error and log for debugging
    console.error('generate error', err);
    typeWriter(output, 'An unexpected error occurred. Check console for details.');
  }
});

/* Optional: allow Enter+Ctrl to generate */
userInput.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    generateBtn.click();
  }
});
</script>

</body>
</html>

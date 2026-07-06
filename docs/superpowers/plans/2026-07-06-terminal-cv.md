# Terminal CV Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the GitHub profile README (`Esmail-ibraheem/Esmail-ibraheem`) with a Claude Code–style terminal session: an animated SVG hero that "boots" Esmail's CLI, followed by a markdown body where each CV section is a slash command.

**Architecture:** Two artifacts. (1) `assets/hero.svg` — a fully self-contained animated terminal window driven by CSS `@keyframes` on one 20-second master loop (GitHub renders SVG inside `<img>`, so CSS animations play but scripts/external loads do not). (2) `README.md` — the "rest of the session" as real markdown: `<samp>` tool-call lines, clickable links, recolored stat cards. No build step, no CI.

**Tech Stack:** Hand-written SVG + CSS keyframes; GitHub-flavored markdown with inline HTML (`<samp>`, `<sub>`, `<img>`); github-readme-stats + streak-stats services for live numbers.

**Spec:** `docs/superpowers/specs/2026-07-06-terminal-cv-design.md` (approved). Palette, timeline, and section content are normative there; this plan turns them into exact files.

**Repo facts (verified):**
- Working dir `F:\Terminal_CV`, branch `terminal-cv`, remote `origin = https://github.com/Esmail-ibraheem/Esmail-ibraheem.git`.
- Platform is Windows; shell commands below are Git Bash (`Bash` tool) unless noted.
- No test framework exists or is wanted — verification is visual (browser + github.com rendering), per spec §7. TDD does not apply to static markdown/SVG assets; each task instead has an explicit render-verification step that must pass before commit.

---

## File structure

| File | Responsibility |
|------|----------------|
| `assets/hero.svg` | Create. The entire animated hero: window chrome, welcome box, typed prompt, spinner, tool call, output, footer. Self-contained (no external fonts/images/scripts). |
| `README.md` | Replace entirely. Hero embed + sections `whoami`, `/publications`, `/projects`, `/skills`, `/stats`, `/contact`, footer statusline. |
| `docs/superpowers/plans/2026-07-06-terminal-cv.md` | This plan. |

Nothing else changes. The old README's content (About Me, publications list) is absorbed into the new sections — the spec's §5 content lists are already final, copied from the current README.

## Design constants (from spec §3–4; used verbatim in both files)

- bg `#1F1E1D` · border `#3E3E38` · coral `#D97757` · cream `#F0EEE6` · dim `#8A8A82` · green `#4EBA65` · traffic lights `#E5695E` / `#D9A756` / `#4EBA65`
- Font: `ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace`, 14px, 22px line grid.
- Master loop = 20s, so 1s = 5% in every keyframe block. Char width budget = 8.4px at 14px; every text run whose width matters carries `textLength` so mask timing and box fit hold on any platform monospace font.
- Typing reveal: a bg-colored **cover rect** that steps right with `steps(14, end)` (one step per character of `who is esmail?`). This satisfies the spec's "animated clip/mask rect" intent with fewer moving parts and maximum `<img>`-mode compatibility: only `opacity` and `transform` are ever animated.
- Animated element count: 22 (scene, window, 4 welcome groups, prompt, typer, cursor gate, cursor, think gate, 5 spinner glyphs, 2 tool lines, 3 output lines, footer) — under the spec's <60 budget.

---

### Task 1: Animated hero (`assets/hero.svg`)

**Files:**
- Create: `assets/hero.svg`

- [ ] **Step 1: Create `assets/hero.svg` with exactly this content**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 500" width="840" height="500" role="img" aria-label="Esmail's Terminal CV. An animated terminal session answers 'who is esmail?': AI Research Engineer - LLMs, distributed training, MoE. 7 arXiv publications, PyTorch and CUDA.">
  <style>
    text {
      font-family: ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace;
      font-size: 14px;
      fill: #F0EEE6;
    }
    .t12 { font-size: 12px; }
    .dim { fill: #8A8A82; }
    .coral { fill: #D97757; }
    .green { fill: #4EBA65; }
    .b { font-weight: 700; }
    .i { font-style: italic; }

    /* Window chrome fades in once on load and persists; only the session
       content (#scene) loops. "Fade to bg" then empties the terminal instead
       of blinking the whole window off (no white flash on light pages). */
    #win    { animation: winIn 0.4s ease-out 1; }
    #scene  { animation: scene 20s linear infinite; }
    #wl1    { animation: wl1 20s linear infinite; }
    #wl3    { animation: wl3 20s linear infinite; }
    #wl4    { animation: wl4 20s linear infinite; }
    #wl5    { animation: wl5 20s linear infinite; }
    #prompt { animation: prompt 20s linear infinite; }
    #typer  { transform: translateX(118px); animation: type 20s steps(14, end) infinite; }
    #curgate { opacity: 0; animation: curgate 20s linear infinite; }
    #cursor { animation: blink 1s linear infinite; }
    #think  { opacity: 0; animation: think 20s linear infinite; }
    .sp     { animation: spin 0.8s linear infinite; opacity: 0; }
    .sp1 { animation-delay: 0s; }
    .sp2 { animation-delay: 0.16s; }
    .sp3 { animation-delay: 0.32s; }
    .sp4 { animation-delay: 0.48s; }
    .sp5 { animation-delay: 0.64s; }
    #tool1 { animation: tool1 20s linear infinite; }
    #tool2 { animation: tool2 20s linear infinite; }
    #out1  { animation: out1 20s linear infinite; }
    #out2  { animation: out2 20s linear infinite; }
    #out3  { animation: out3 20s linear infinite; }
    #foot  { animation: foot 20s linear infinite; }

    /* master timeline: 20s, 1s = 5% */
    @keyframes scene  { 0%, 92.5% { opacity: 1; } 97%, 100% { opacity: 0; } }
    @keyframes winIn  { 0% { opacity: 0; } 100% { opacity: 1; } }
    @keyframes wl1    { 0%, 2%   { opacity: 0; } 3.5%, 100% { opacity: 1; } }
    @keyframes wl3    { 0%, 4%   { opacity: 0; } 5.5%, 100% { opacity: 1; } }
    @keyframes wl4    { 0%, 5.5% { opacity: 0; } 7%, 100%   { opacity: 1; } }
    @keyframes wl5    { 0%, 6.5% { opacity: 0; } 8%, 100%   { opacity: 1; } }
    @keyframes prompt { 0%, 9.5% { opacity: 0; } 10%, 100%  { opacity: 1; } }
    @keyframes type   { 0%, 10% { transform: translateX(0); } 22%, 100% { transform: translateX(118px); } }
    @keyframes curgate { 0%, 9.4% { opacity: 0; } 9.5%, 23.9% { opacity: 1; } 24%, 100% { opacity: 0; } }
    @keyframes blink  { 0%, 49.9% { opacity: 1; } 50%, 100% { opacity: 0; } }
    @keyframes think  { 0%, 24% { opacity: 0; } 24.5%, 34.5% { opacity: 1; } 35%, 100% { opacity: 0; } }
    @keyframes spin   { 0%, 19.9% { opacity: 1; } 20%, 100% { opacity: 0; } }
    @keyframes tool1  { 0%, 35% { opacity: 0; } 36%, 100% { opacity: 1; } }
    @keyframes tool2  { 0%, 37% { opacity: 0; } 38%, 100% { opacity: 1; } }
    @keyframes out1   { 0%, 40% { opacity: 0; transform: translateY(5px); } 42%, 100% { opacity: 1; transform: translateY(0); } }
    @keyframes out2   { 0%, 43% { opacity: 0; transform: translateY(5px); } 45%, 100% { opacity: 1; transform: translateY(0); } }
    @keyframes out3   { 0%, 46% { opacity: 0; transform: translateY(5px); } 48%, 100% { opacity: 1; transform: translateY(0); } }
    @keyframes foot   { 0%, 50% { opacity: 0; } 52%, 100% { opacity: 1; } }

    /* Static full-session frame for reduced-motion users and renderers
       without CSS animation (base styles above equal the final frame). */
    @media (prefers-reduced-motion: reduce) {
      #win, #scene, #wl1, #wl3, #wl4, #wl5, #prompt, #typer, #curgate, #cursor,
      #think, .sp, #tool1, #tool2, #out1, #out2, #out3, #foot { animation: none; }
    }
  </style>

  <!-- window chrome: fades in once, persists across content loops -->
  <g id="win">
    <rect x="0.5" y="0.5" width="839" height="499" rx="12" fill="#1F1E1D" stroke="#3E3E38"/>
    <line x1="1" y1="36.5" x2="839" y2="36.5" stroke="#3E3E38"/>
    <circle cx="24" cy="18.5" r="6" fill="#E5695E"/>
    <circle cx="44" cy="18.5" r="6" fill="#D9A756"/>
    <circle cx="64" cy="18.5" r="6" fill="#4EBA65"/>
    <text class="t12 dim" x="420" y="23" text-anchor="middle">esmail@sanaa — ~/esmail-ibraheem</text>
  </g>

  <!-- session content: loops every 20s -->
  <g id="scene">
      <!-- welcome box (wl2 is the blank spacer line) -->
      <g id="wl1">
        <rect x="32" y="58" width="412" height="128" rx="6" fill="none" stroke="#3E3E38"/>
        <text x="48" y="82"><tspan class="coral">✻</tspan><tspan class="b" x="65">Welcome to Esmail's Terminal CV!</tspan></text>
      </g>
      <g id="wl3"><text class="dim" x="48" y="126" textLength="302">/help for help · /cv for full résumé</text></g>
      <g id="wl4"><text class="dim" x="48" y="148" textLength="185">cwd: ~/esmail-ibraheem</text></g>
      <g id="wl5"><text class="dim" x="48" y="170" textLength="370">model: esmail-v25 · Sana'a University, Yemen</text></g>

      <!-- typed prompt -->
      <g id="prompt">
        <text class="coral b" x="32" y="214">&gt;</text>
        <text x="49" y="214" textLength="118">who is esmail?</text>
      </g>
      <!-- typed line: 14 chars × 8.4px — keep steps(14), translateX(118px), textLength="118" and cover width in sync -->
      <g id="typer">
        <rect x="49" y="199" width="122" height="20" fill="#1F1E1D"/>
        <g id="curgate"><rect id="cursor" x="49" y="201" width="8" height="17" fill="#F0EEE6"/></g>
      </g>

      <!-- thinking spinner (same row is reused by the tool call once it ends) -->
      <g id="think">
        <text class="sp sp1 coral" x="32" y="258">·</text>
        <text class="sp sp2 coral" x="32" y="258">✢</text>
        <text class="sp sp3 coral" x="32" y="258">✳&#xFE0E;</text>
        <text class="sp sp4 coral" x="32" y="258">✶</text>
        <text class="sp sp5 coral" x="32" y="258">✻</text>
        <text class="dim i" x="49" y="258">Thinking…</text>
      </g>

      <!-- tool call -->
      <g id="tool1"><text x="32" y="258"><tspan class="green">⏺&#xFE0E;</tspan><tspan x="49" class="b">Read</tspan><tspan>(about.md)</tspan></text></g>
      <g id="tool2"><text class="dim" x="49" y="280">⎿&#160;&#160;Read 12 lines (ctrl+r to expand)</text></g>

      <!-- output -->
      <g id="out1"><text x="49" y="324">AI Research Engineer — LLMs, distributed training, MoE</text></g>
      <g id="out2"><text x="49" y="346">7 arXiv publications · 86 repos · PyTorch &amp; CUDA</text></g>
      <g id="out3"><text class="dim i" x="49" y="368">"attention is all you need."</text></g>

      <!-- footer -->
      <g id="foot"><text class="dim" x="32" y="466">scroll ↓&#xFE0E; for the full session · ✻ 42k tokens · esc to interrupt</text></g>
  </g>
</svg>
```

Layout notes for the implementer (why these numbers):
- Baselines sit on the 22px grid: welcome box lines 82/104(blank)/126/148/170; prompt 214; thinking/tool 258; `⎿` 280; output 324/346/368; footer 466.
- `textLength` values = character count × 8.4px (14-char typed line → 118px; 36 → 302; 22 → 185; 44 → 370). The cover rect (width 122 at x 49) hides exactly the pinned 118px typed run and steps right 118px in 14 steps, so reveal timing matches characters on every platform font.
- `&#160;` (no-break spaces) in the `⎿` line prevent XML whitespace collapsing without needing `xml:space`.
- Timeline mapping (1s = 5%): welcome 2–8%, typing 10–22%, thinking 24–35%, tool call 35–38%, output 40–48%, footer 50–52%, hold, content fade-out 92.5–97%, empty terminal until 100%, loop restarts. The window chrome (`#win`) fades in once over 0.4s at load and never loops — the "fade to bg" empties the terminal rather than blanking the image (which would flash white on light-theme pages).

- [ ] **Step 2: Validate the file is well-formed XML**

Run (PowerShell tool):
```powershell
[xml](Get-Content -Raw assets\hero.svg) | Out-Null; "XML OK"
```
Expected: `XML OK` (any parse error means a bad entity/escape — fix before proceeding).

- [ ] **Step 3: Verify the animation in a real browser**

Run (PowerShell tool): `Start-Process (Resolve-Path assets\hero.svg)` — opens default browser.

If running agentically with no way to watch a 20s loop, write a one-page harness `scratchpad/hero-check.html` embedding `<img src="hero.svg">` and screenshot it at ~3s, 6s, 9s, 12s if browser tooling is available; otherwise pause and ask the human to confirm the checklist:
- [ ] Welcome box lines stagger in, then `> who is esmail?` types character-by-character with a blinking block cursor
- [ ] Spinner cycles `· ✢ ✳ ✶ ✻` in coral, then is replaced by `⏺ Read(about.md)` + dim `⎿` line on the same row
- [ ] Three output lines slide in; dim footer appears; ~8s hold; fade to dark; loop restarts without a visual jump
- [ ] No text overflows the welcome box or window at 100% and 200% zoom

- [ ] **Step 4: Commit**

```bash
git add assets/hero.svg
git commit -m "feat: add animated terminal hero SVG

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Terminal session body (`README.md`)

**Files:**
- Modify (full replacement): `README.md`

- [ ] **Step 1: Fetch the primary language of each pinned repo** (spec §5.4 wants name + one-line description + language)

Run:
```bash
for r in nanograd Axon Nexus NeuroFlow Galvatron ExpertRAG; do
  echo -n "$r: "; curl -s "https://api.github.com/repos/Esmail-ibraheem/$r" | grep -m1 '"language"'
done
```
Expected: one language per repo (likely `Python`/`Jupyter Notebook`). Use these to replace the `Python` placeholders in Step 2. If the API rate-limits or returns `null` for a repo, keep `Python` for that repo — correct for this account per repo history — and note it in the commit message.

- [ ] **Step 2: Replace `README.md` entirely with this content** (fill in languages from Step 1)

````markdown
<p align="center">
  <img src="assets/hero.svg" width="840" alt="✻ Welcome to Esmail's Terminal CV! — > who is esmail? — AI Research Engineer: LLMs, distributed training, MoE · 7 arXiv publications · PyTorch & CUDA">
</p>

### `> whoami`

<samp>⏺ <b>Read</b>(about.md)</samp><br>
<samp>&nbsp;&nbsp;⎿&nbsp;&nbsp;Read 3 lines</samp>

**AI Research Engineer** with a deep passion for neural networks, large language models, and scalable ML systems. Strong foundation in **PyTorch** and **CUDA**; committed to open-source development and to bridging the gap between research and real-world applications by translating papers into practical implementations.

<sub>see also: [portfolio ↗](https://esmail-ibraheem.github.io/portfolio/)</sub>

---

### `> /publications`

<samp>⏺ <b>Read</b>(publications/)</samp><br>
<samp>&nbsp;&nbsp;⎿&nbsp;&nbsp;7 papers · ordered by most proud of</samp>

1. [ExpertRAG: Efficient RAG with Mixture of Experts — Optimizing Context Retrieval for Adaptive LLM Responses](https://arxiv.org/abs/2504.08744)
2. [Galvatron: Automatic Distributed Training for Large Transformer Models](https://arxiv.org/abs/2504.03662)
3. [Theoretical Foundations and Mitigation of Hallucination in Large Language Models](https://arxiv.org/abs/2507.22915)
4. [Mixture of Transformers: Macro-Level Gating for Sparse Activation in Large Language Model Ensembles](http://dx.doi.org/10.13140/RG.2.2.25049.02400)
5. [Bachelor Thesis: AI Engine: Deep Learning and Neural Network Engine](http://dx.doi.org/10.13140/RG.2.2.22814.24643)
6. [Universal Approximation Theorem for a Single-Layer Transformer](https://arxiv.org/abs/2507.10581)
7. [Mixture of Attention Schemes (MoAS): Learning to Route Between MHA, GQA, and MQA](https://arxiv.org/abs/2512.20650)

---

### `> /projects`

<samp>⏺ <b>Bash</b>(ls ~/projects)</samp><br>
<samp>&nbsp;&nbsp;⎿&nbsp;&nbsp;6 directories</samp>

- [**nanograd**](https://github.com/Esmail-ibraheem/nanograd) — ML/DL ecosystem engine: GPT, Llama, Stable Diffusion, ViT · `Python`
- [**Axon**](https://github.com/Esmail-ibraheem/Axon) — paper implementations: InstructGPT, Llama, transformers, diffusion · `Python`
- [**Nexus**](https://github.com/Esmail-ibraheem/Nexus) — dynamic GPU allocation for Mixture-of-Experts · `Python`
- [**NeuroFlow**](https://github.com/Esmail-ibraheem/NeuroFlow) — node-based AI training pipelines · `Python`
- [**Galvatron**](https://github.com/Esmail-ibraheem/Galvatron) — large-scale distributed transformer training · `Python`
- [**ExpertRAG**](https://github.com/Esmail-ibraheem/ExpertRAG) — MoE-routed retrieval-augmented generation · `Python`

---

### `> /skills`

<samp>⏺ <b>Bash</b>(esmail --status)</samp>

```text
Core       Python · PyTorch · CUDA
Research   LLMs · Mixture-of-Experts · RAG · diffusion models
Systems    distributed training · GPU scheduling · inference optimization
Tools      Hugging Face · Git · Linux
```

---

### `> /stats`

<samp>⏺ <b>Bash</b>(gh stats --user Esmail-ibraheem)</samp>

<p>
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=Esmail-ibraheem&show_icons=true&hide_border=true&bg_color=1F1E1D&title_color=D97757&text_color=F0EEE6&icon_color=D97757&ring_color=D97757" alt="GitHub stats card">
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Esmail-ibraheem&layout=compact&hide_border=true&bg_color=1F1E1D&title_color=D97757&text_color=F0EEE6" alt="Top languages card">
</p>

<img src="https://streak-stats.demolab.com/?user=Esmail-ibraheem&background=1F1E1D&ring=D97757&fire=D97757&currStreakLabel=D97757&sideLabels=F0EEE6&currStreakNum=F0EEE6&sideNums=F0EEE6&dates=8A8A82&hide_border=true" alt="Contribution streak card">

---

### `> /contact`

<samp>⏺ <b>Read</b>(contact.md)</samp>

[Portfolio](https://esmail-ibraheem.github.io/portfolio/) · [LinkedIn](https://www.linkedin.com/in/esmail-a-gumaan) · [Google Scholar](https://scholar.google.com/citations?user=FbQKSXkAAAAJ) · [Hugging Face](https://huggingface.co/Esmail-AGumaan) · [ORCID](https://orcid.org/0009-0003-1270-5905) · [ResearchGate](https://www.researchgate.net/profile/Esmail-Gumaan) · [Semantic Scholar](https://www.semanticscholar.org/author/2354181125)

---

<sub><samp>~/esmail-ibraheem · esmail-v25 · ✻ 128k context · ? for shortcuts</samp></sub>
````

Content rules being enforced (from spec §5): every link lives in plain markdown, never inside a fenced block (the `/skills` block deliberately contains no links); tool-call lines are `<samp>` with `&nbsp;`-indented `⎿` results; dim metadata uses `<sub>`; no star counts; hero `<img>` is not wrapped in a link.

- [ ] **Step 3: Sanity-check the markdown**

- `git diff --stat` — only `README.md` changed.
- Confirm all 21 links are present (portfolio 1 + publications 7 + projects 6 + contact 7): `grep -o "](http" README.md | wc -l` → expected `21`.
- Confirm no fenced code block contains a `](` link.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: replace profile README with terminal CV session

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Push and verify on github.com

- [ ] **Step 1: Push the branch**

```bash
git push -u origin terminal-cv
```
Expected: new branch on origin. (Pushing a non-default branch changes nothing user-visible on the profile.)

- [ ] **Step 2: Verify rendering on github.com** (spec §7.2 — the branch view uses the same sanitizer + camo proxy as the profile)

Open `https://github.com/Esmail-ibraheem/Esmail-ibraheem/tree/terminal-cv` and check:
- [ ] Hero SVG animates through the camo proxy (typing, spinner, loop)
- [ ] `<samp>` / `<sub>` / `<b>` render (tool-call lines look terminal-ish, not stripped)
- [ ] All 21 links clickable; stat cards render in the palette
- [ ] Page reads acceptably in both GitHub light and dark themes (hero + cards are dark-baked by design)

If browser tooling is unavailable to the agent, fetch `https://github.com/Esmail-ibraheem/Esmail-ibraheem/blob/terminal-cv/README.md` and confirm the HTML still contains `samp`, the camo-proxied `hero.svg` URL, and the link count — then ask the human for the final visual pass.

- [ ] **Step 3: Hand off for merge (human decision)**

Do **not** merge to `main` autonomously — the profile page goes live worldwide on merge (spec §7.3 reserves this for the user). Report completion, link the branch view, and remind: if the SVG is later edited, rename it (`hero-v2.svg`) to bust the camo cache (spec §6).

---

## Verification summary (before claiming done — see superpowers:verification-before-completion)

1. `assets/hero.svg` parses as XML and plays its full 20s timeline in a browser with a seamless loop.
2. `README.md` on the pushed branch renders on github.com with animation, styled tool-call lines, and 21 working links.
3. Human confirms visuals and merges to `main` themselves.

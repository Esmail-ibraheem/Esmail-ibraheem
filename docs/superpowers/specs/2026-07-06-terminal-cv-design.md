# Terminal CV — Design Spec

**Date:** 2026-07-06
**Repo:** `Esmail-ibraheem/Esmail-ibraheem` (GitHub profile README)
**Branch:** `terminal-cv`
**Status:** Approved by user (scope, branding, sections, and technical approach each confirmed via Q&A)

## 1. Concept

Replace the entire profile README with one continuous session in Esmail's own
Claude Code–style CLI ("full terminal takeover", approved). The page opens with
an **animated SVG hero** that boots the CLI and types the first question live.
Below it, the session continues as **real markdown** — selectable text and
clickable links — where each CV section is a slash command the visitor "ran".

Branding is **personalized** (approved): it is *Esmail's* CLI, not a Claude Code
screenshot — `✻ Welcome to Esmail's Terminal CV!` — while keeping the iconic
visual vocabulary: welcome box, `>` prompts, `✻ Thinking…` spinner, `⏺` tool
calls with `⎿` result lines, dim statusline.

### Goals
- Instantly recognizable Claude Code aesthetic (dark, coral accent, monospace).
- Animated typing hero that works on github.com with no JS/CSS in markdown.
- All CV content (7 publications, 6 projects, contact links) remains clickable,
  selectable, and indexable — content lives in markdown, not inside images.
- Trivially editable later: adding a paper = one markdown line.

### Non-goals
- No GitHub Action / cron regeneration; the only live data is via stat-card services.
- No light-theme SVG variant (dark background is baked in and looks right on both themes).
- No GIF fallback, no shields.io badges (they break the terminal illusion).
- No changes to any other repo.

## 2. Files

| File | Purpose |
|------|---------|
| `README.md` | Full replacement of current profile README: the markdown session body, embedding the hero at top. |
| `assets/hero.svg` | Self-contained animated terminal window (no external resources — GitHub's camo proxy blocks them). Referenced relatively: `<img src="assets/hero.svg" …>` so it works once merged to the default branch. |
| `docs/superpowers/specs/…` | This spec (and later the implementation plan). |

## 3. Palette & typography (shared by SVG and stat cards)

| Token | Value | Use |
|-------|-------|-----|
| bg | `#1F1E1D` | terminal background (baked into SVG and stat cards) |
| surface border | `#3E3E38` | window border, box-drawing strokes |
| coral (accent) | `#D97757` | `✻`, prompt `>`, titles, spinner, links accent |
| cream (text) | `#F0EEE6` | primary text |
| dim | `#8A8A82` | secondary text, hints, statusline |
| green | `#4EBA65` | `⏺` completed tool-call bullet |
| red / yellow / green dots | `#E5695E` / `#D9A756` / `#4EBA65` | faux window traffic lights |

Font stack (SVG `font-family`): `ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace`, 14px, line-height 22px.

## 4. Animated hero (`assets/hero.svg`)

Dark terminal window, `viewBox 0 0 840 500`, rounded corners (rx 12), faux
title bar with traffic-light dots and title `esmail@sanaa — ~/esmail-ibraheem`.

**Scene timeline** (single master loop ≈ 20s; every element's CSS keyframes are
percentages of the same 20s duration so the loop stays in sync):

| t (s) | Event |
|-------|-------|
| 0.0–0.4 | window + title bar fade in |
| 0.4–1.6 | welcome box lines appear staggered: `✻ Welcome to Esmail's Terminal CV!` / blank / `/help for help · /cv for full résumé` / `cwd: ~/esmail-ibraheem` / `model: esmail-v25 · Sana'a University, Yemen` |
| 2.0–4.4 | `> who is esmail?` types char-by-char (~0.15s/char) with blinking block cursor |
| 4.8–7.0 | `✻ Thinking…` — spinner glyph cycles `·` `✢` `✳` `✶` `✻` (coral); disappears when done |
| 7.0–7.6 | `⏺ Read(about.md)` (green bullet) then dim `⎿  Read 12 lines (ctrl+r to expand)` |
| 8.0–9.6 | three output lines fade/slide in: `AI Research Engineer — LLMs, distributed training, MoE` / `7 arXiv publications · 86 repos · PyTorch & CUDA` / dim italic `"attention is all you need."` |
| 10.0 | dim footer: `scroll ↓ for the full session · ✻ 42k tokens · esc to interrupt` |
| 10–18.5 | hold |
| 18.5–20 | fade to bg, loop restarts |

**Technical constraints (hard requirements):**
- Animations via CSS `@keyframes` inside the SVG `<style>` (GitHub renders SVG in `<img>`, where CSS/SMIL animations play but scripts and external loads do not).
- Typing effect: reveal via animated clip/mask rect over the text; the typed `<text>` gets an explicit `textLength` so mask timing aligns regardless of the viewer's platform monospace font. Any box-drawing column alignment likewise uses `textLength` pinning.
- Zero external references (fonts, images, imports). System monospace stack only.
- Keep animated node count modest (< ~60 animated elements) for render performance.

## 5. Markdown session body (`README.md`)

Global pattern per section: prompt-styled heading → fake tool-call line(s) in
inline monospace (`<samp>`) → payload as real markdown with clickable links.
Dim metadata uses `<sub>`. No fenced code block may contain content that needs
to be a link (links don't render inside code blocks).

Sections in order:

1. **Hero** — `<img src="assets/hero.svg">` full width (wrapped in `<picture>`/plain `img`; no link wrapper).
2. **`> whoami`** — 2–3 line About distilled from the current README's About Me
   (AI Research Engineer; neural networks, LLMs, scalable ML systems; PyTorch &
   CUDA; open-source and research-to-practice focus), plus portfolio link.
3. **`> /publications`** — `⏺ Read(publications/)` + `⎿ 7 papers · ordered by most proud of`, then a numbered list, each title a link (order preserved from current README):
   1. ExpertRAG: Efficient RAG with Mixture of Experts — Optimizing Context Retrieval for Adaptive LLM Responses — <https://arxiv.org/abs/2504.08744>
   2. Galvatron: Automatic Distributed Training for Large Transformer Models — <https://arxiv.org/abs/2504.03662>
   3. Theoretical Foundations and Mitigation of Hallucination in Large Language Models — <https://arxiv.org/abs/2507.22915>
   4. Mixture of Transformers: Macro-Level Gating for Sparse Activation in Large Language Model Ensembles — <http://dx.doi.org/10.13140/RG.2.2.25049.02400>
   5. Bachelor Thesis: AI Engine: Deep Learning and Neural Network Engine — <http://dx.doi.org/10.13140/RG.2.2.22814.24643>
   6. Universal Approximation Theorem for a Single-Layer Transformer — <https://arxiv.org/abs/2507.10581>
   7. Mixture of Attention Schemes (MoAS): Learning to Route Between MHA, GQA, and MQA — <https://arxiv.org/abs/2512.20650>
4. **`> /projects`** — `⏺ Bash(ls ~/projects)` + listing of the six pinned repos, each name a repo link with one-line description and language; **no star counts** (they go stale):
   nanograd (ML/DL ecosystem engine — GPT, Llama, Stable Diffusion, ViT) · Axon (paper implementations: InstructGPT, Llama, transformers, diffusion) · Nexus (dynamic GPU allocation for MoE) · NeuroFlow (node-based AI training pipelines) · Galvatron (large-scale distributed transformer training) · ExpertRAG (MoE-routed RAG). All under `https://github.com/Esmail-ibraheem/<name>`.
5. **`> /skills`** — `⏺ esmail --status`: a fenced code block (no links needed) styled as a `/status` readout grouping: Core (Python · PyTorch · CUDA), Research (LLMs · MoE · RAG · diffusion), Systems (distributed training · GPU scheduling · inference optimization), Tools (HuggingFace · Git · Linux). Derived from repos/papers; user may edit the list at review.
6. **`> /stats`** — `⏺ Bash(gh stats --user Esmail-ibraheem)` + stat cards recolored to the palette (`bg_color=1F1E1D`, `title_color=D97757`, `text_color=F0EEE6`, `icon_color=D97757`, `hide_border=true`):
   - `github-readme-stats.vercel.app/api?username=Esmail-ibraheem&show_icons=true…`
   - `github-readme-stats.vercel.app/api/top-langs/?username=Esmail-ibraheem&layout=compact…`
   - `streak-stats.demolab.com/?user=Esmail-ibraheem&background=1F1E1D&ring=D97757&fire=D97757…`
7. **`> /contact`** — `⏺ Read(contact.md)` + link list: Portfolio <https://esmail-ibraheem.github.io/portfolio/> · LinkedIn <https://www.linkedin.com/in/esmail-a-gumaan> · Google Scholar <https://scholar.google.com/citations?user=FbQKSXkAAAAJ> · Hugging Face <https://huggingface.co/Esmail-AGumaan> · ORCID <https://orcid.org/0009-0003-1270-5905> · ResearchGate <https://www.researchgate.net/profile/Esmail-Gumaan> · Semantic Scholar <https://www.semanticscholar.org/author/2354181125>
8. **Footer statusline** — dim single line: `~/esmail-ibraheem · esmail-v25 · ✻ 128k context · ? for shortcuts`.

## 6. Error handling / degradation

- Stat-card services down → images degrade to descriptive alt text; session still reads coherently.
- SVG hero fails to load → `alt` text carries the welcome line.
- GitHub caches images via camo: after any SVG change, rename the asset (e.g. `hero-v2.svg`) if the cache must bust immediately.
- Glyph-width drift across platform fonts → `textLength` pinning inside SVG (§4); markdown body avoids cross-line box-drawing that depends on alignment.

## 7. Verification

1. Open `assets/hero.svg` in a local browser: full timeline plays, loop is seamless, no layout drift at 100%/200% zoom.
2. Push `terminal-cv` branch; view the branch's README on github.com (same sanitizer/proxy as profile view): check animation plays, `<samp>`/`<sub>` render, all links clickable, both dark and light GitHub themes look right.
3. User merges to `main` → profile page shows it; final visual check.

## 8. Decisions log

| Question | Decision |
|----------|----------|
| Scope | Full terminal takeover of README (old About/Publications content absorbed) |
| Branding | Personalized CLI ("Esmail's Terminal CV"), Claude Code visual vocabulary, no literal Claude Code branding |
| Sections | All: whoami, publications, projects, skills, stats, contact (+ hero, footer) |
| Approach | Animated SVG hero + terminal-flavored markdown body (motion where it matters, clickable content everywhere else) |
| Star counts in projects | Omitted — go stale, no auto-update mechanism in scope |

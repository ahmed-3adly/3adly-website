# 3adly Design System

> Source of truth for visual language, tokens, and component patterns across the 3adly portfolio site. If a decision isn't here, it isn't real yet.

**Status:** v1 — dark-first, light mode planned (not built).
**Last updated:** 2026-04-28 (normalize pass — token-name truth, missing tokens added)

---

## 1. Foundations

### 1.1 Philosophy

Two ideas drive every decision:

1. **Restraint signals taste.** A senior portfolio earns trust by showing what it leaves out. Color is rationed. Motion is purposeful. Whitespace is non-negotiable.
2. **The medium fits the message.** A landing surface and a case study do different jobs. Forcing them into one visual mode flattens both. We run two modes that share a foundation.

### 1.2 The two modes

| Mode | Where it lives | Personality |
|---|---|---|
| **Showcase** | Homepage, marketing surfaces, About, Skills, Work index, Contact | Confident, energetic, motion-aware. The site's "front door." |
| **Editorial** | Case studies, longform writing, deep-dives | Quiet, type-led, reading-first. The site's "library." |

Both modes share the **same tokens** (color, type, spacing, motion). They differ in **which patterns are allowed** and **how loud** they're allowed to be.

### 1.3 When to use which mode

Use **Showcase** when:
- The page is meant to convince in under 10 seconds.
- The user is scanning, not reading.
- Personality matters more than precision.

Use **Editorial** when:
- The user is committing 3+ minutes.
- The content earns its space (real numbers, real artifacts, real reasoning).
- Decoration would interrupt comprehension.

If you can't tell, default to **Editorial**. Restraint is harder to undo than additions.

### 1.4 Non-goals

- Not a multi-product design system. This serves one site.
- Not a Storybook replacement. This is a written contract; code is canonical.
- Not Material/HIG-shaped. We don't ship buttons in 14 variants.

---

## 2. Color tokens

All values are dark-mode. Light-mode values are TODO; the **token names are stable**, only the hex values will change.

### 2.1 Surfaces

| Token | Value | Role |
|---|---|---|
| `--bg-canvas` | `#0a0a0f` | Page background. The blackest surface. |
| `--bg-surface` | `#14141c` | Cards, raised panels, modal backdrops. |
| `--bg-surface-elevated` | `#1d1d28` | Hover/active state of `--bg-surface`. |
| `--bg-inverse` | `#f5f5f7` | Reserved — used only when light surfaces are intentional (rare). |

**Do** use `--bg-canvas` as the html/body background.
**Don't** put `--bg-surface` on full-bleed sections; reserve it for contained components.

### 2.2 Foreground (text + icons)

| Token | Value | Role |
|---|---|---|
| `--fg-primary` | `#f5f5f7` | Body copy, headlines. Off-white, easier than pure white. |
| `--fg-secondary` | `#a8a8b3` | Subheads, captions, secondary labels. |
| `--fg-muted` | `#6e6e7a` | Metadata, timestamps, eyebrow text in low-emphasis contexts. |
| `--fg-disabled` | `#4a4a55` | Disabled controls only. |

**Do** use `--fg-secondary` for almost all "supporting" copy.
**Don't** introduce gray values outside this scale. If you need a new gray, the design is wrong.

### 2.3 Borders

| Token | Value | Role |
|---|---|---|
| `--border-hairline` | `rgba(255, 255, 255, 0.08)` | Default 1px border. Used everywhere in Editorial mode. |
| `--border-strong` | `rgba(255, 255, 255, 0.18)` | Hover/focus elevation of hairline. |
| `--border-accent` | `var(--accent)` | Accent border for selected/active states. |

**Do** use hairlines as the primary structural device in Editorial — not shadows.
**Don't** mix hairlines and box-shadows on the same component.

### 2.4 Accent

| Token | Value | Role |
|---|---|---|
| `--accent` | `#5b6cff` | The site's single signature color. Iris — saturated blue with violet lean. |
| `--accent-muted` | `rgba(91, 108, 255, 0.16)` | Tinted backgrounds (selected chips, focus halos). |
| `--accent-strong` | `#3d52ff` | Hover/active state of `--accent`. |

**The accent is the only chromatic color in the system.** Use it for:
- One CTA per page (max).
- Focus rings.
- Active state of nav.
- Numbered eyebrows in Editorial mode.
- Pull-quote rules.

**Don't** use the accent for:
- Body text (kills readability + cheapens it).
- Backgrounds larger than ~10% of viewport.
- Multiple elements in the same viewport that aren't related.

### 2.5 Status (used sparingly)

| Token | Value | Role |
|---|---|---|
| `--status-success` | `#4ade80` | Live status dots, "shipped" badges. |
| `--status-warning` | `#fbbf24` | "In progress," beta. |
| `--status-danger` | `#f87171` | Errors, destructive actions only. |

Status colors live outside the accent system. Don't mix them with `--accent` in the same component.

### 2.6 Focus + selection

| Token | Value | Role |
|---|---|---|
| `--focus-ring` | `var(--accent)` | 2px outline, 2px offset, on every focusable element. |
| `--selection-bg` | `var(--accent-muted)` | `::selection` background. |
| `--selection-fg` | `var(--fg-primary)` | `::selection` text. |

### 2.7 Light mode (TODO)

When light mode lands, only the values change — names stay. Sketch:

```
--bg-canvas: #ffffff  →  ~ #fafafa
--fg-primary: #f5f5f7 →  ~ #0a0a0f
--border-hairline: rgba(255,255,255,0.08) → rgba(0,0,0,0.08)
--accent: #5b6cff → unchanged or slightly darker (#4a5cee) for AA contrast on white
```

---

## 3. Typography

### 3.1 Families

| Family | Role | Weights loaded |
|---|---|---|
| **General Sans** | Display only — hero, section openers, project titles, big numbers. | 500, 600, 700, 800 |
| **Geist Mono** | Everything else — body, UI, labels, captions, eyebrows, code, metadata. | 400, 500, 600 |

Two-family system, mono-forward. Body is monospaced — this is the engineering signal of the portfolio. Reading speed is slightly slower; the trade is intentional.

Display is General Sans (Fontshare). It's a humanist sans with crisp geometric counters — neutral enough to share a viewport with mono body without fighting it, distinctive enough to carry headline weight on its own.

Do not introduce a third face. Do not add a proportional sans for body.

The Tailwind utility for display is **`font-display`** (maps to `--font-display`). The utility for mono is **`font-mono`** (maps to `--font-mono`). UI labels and buttons use `font-mono` — only headlines, project titles, and other display roles use `font-display`.

### 3.2 Scale

| Role | Family | Size | Line-height | Tracking | Weight | Use |
|---|---|---|---|---|---|---|
| `display-xl` | Syne | 96 / 6rem | 0.95 | -0.04em | 800 | One per page max. Hero only. |
| `display-lg` | Syne | 72 / 4.5rem | 1.00 | -0.03em | 800 | Hero on smaller pages, primary section openers. |
| `display-md` | Syne | 48 / 3rem | 1.05 | -0.02em | 700 | Section openers in Editorial. |
| `headline` | Syne | 32 / 2rem | 1.15 | -0.01em | 700 | Subsection headers. |
| `title` | Syne | 24 / 1.5rem | 1.30 | 0 | 700 | Project titles, card headers. |
| `body-lg` | Geist Mono | 17 / 1.0625rem | 1.70 | 0 | 400 | Editorial reading body. |
| `body` | Geist Mono | 15 / 0.9375rem | 1.70 | 0 | 400 | Default. |
| `body-sm` | Geist Mono | 13 / 0.8125rem | 1.60 | 0 | 400 | Secondary copy, lists, UI labels. |
| `caption` | Geist Mono | 12 / 0.75rem | 1.50 | 0 | 400 | Image captions, footnotes, metadata. |
| `eyebrow` | Geist Mono | 11 / 0.6875rem | 1.20 | 0.12em | 600 | UPPERCASE numbered labels. |

**Mono body sizing.** Geist Mono renders denser per character than a proportional sans, so body sizes drop ~1px from the original sans scale (16→15, 18→17, 14→13, 13→12, 12→11) and line-heights bump from 1.6 to 1.70 for breathing room. Don't bump them up "to match Inter" — the system is calibrated for mono.

**Code differentiation.** Inline code and code blocks share the family (Geist Mono) with body. Differentiate visually:
- Inline: `--bg-surface` background, `--space-1` x/y padding, `--radius-xs`.
- Block: `--bg-surface` background, `--space-4` padding, 1px `--border-hairline`, `--radius-sm`. Drop one weight (400 → 400 stays, but reduce contrast slightly via `--fg-secondary`).

### 3.3 Reading width

Mono body needs tighter line lengths than proportional sans because the visual density per word is higher.

- Editorial body copy: **max-width 60ch** (~640px at body-lg). Never wider.
- Showcase body copy: **max-width 55ch** for paragraphs. Hero subheads can go wider but cap at 640px.

If a paragraph runs longer than ~5 lines at these widths, break it. Mono punishes long blocks more than sans does.

### 3.4 Vertical rhythm

- Heading-to-following-paragraph: `0.5em` of the heading's line-height.
- Paragraph-to-paragraph: `1em` of body line-height.
- Section-to-section: `clamp(64px, 8vw, 128px)`.

### 3.5 Headline rules

- Headlines never end with a period.
- Sentence case for `display-*` and `headline` (General Sans reads better in mixed case).
- Title case is forbidden anywhere.
- `eyebrow` is uppercase (the only uppercase role).
- Numerals in headlines use General Sans's lining figures; numerals in body use Geist Mono's tabular figures (tabular by default — alignment in tables is automatic, no extra config).

---

## 4. Spacing, radii, shadows

### 4.1 Spacing scale

4px base unit. Tokens are named by pixel value for clarity:

```
--space-1:  4px
--space-2:  8px
--space-3:  12px
--space-4:  16px
--space-6:  24px
--space-8:  32px
--space-12: 48px
--space-16: 64px
--space-24: 96px
--space-32: 128px
--space-48: 192px
```

**Rule:** snap to the scale. If your design needs `13px`, you mean `12px`.

### 4.2 Radii

```
--radius-none: 0
--radius-xs:   2px   /* tags, chips, hairline corners */
--radius-sm:   8px   /* buttons, small inputs */
--radius-md:   16px  /* cards in Showcase */
--radius-full: 9999px /* pills, avatars */
```

**Editorial mode uses `--radius-none` or `--radius-xs` only.** Sharp corners read more editorial, less product-y.

### 4.3 Shadows

```
--shadow-subtle:   0 1px 2px rgba(0, 0, 0, 0.4), 0 0 0 1px var(--border-hairline)
--shadow-elevated: 0 8px 24px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--border-hairline)
```

**Shadow rules:**
- Editorial mode: shadows are **forbidden**. Use hairlines only.
- Showcase mode: shadows are allowed on cards (ProjectCard, modal-style overlays). One shadow per component max.
- Never combine `--shadow-elevated` with `border` — pick one.

---

## 5. Motion

### 5.1 Durations

```
--duration-fast:       120ms  /* hover state changes */
--duration-base:       240ms  /* default for most transitions */
--duration-slow:       480ms  /* layout shifts, reveal animations */
--duration-deliberate: 720ms  /* Editorial section reveals */
```

### 5.2 Easings

```
--ease-standard:   cubic-bezier(0.2, 0, 0, 1)        /* default */
--ease-decelerate: cubic-bezier(0, 0, 0.2, 1)        /* enter animations */
--ease-accelerate: cubic-bezier(0.4, 0, 1, 1)        /* exit animations */
--ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1) /* Showcase-only flourish */
```

### 5.3 Motion budgets per mode

| | Showcase | Editorial |
|---|---|---|
| Hover lifts (`translateY(-4px)`) | ✅ | ❌ |
| Marquee scroll | ✅ (one per page max) | ❌ |
| Spring easings | ✅ | ❌ |
| Cursor-following effects | ❌ (deprecated, see §13.4) | ❌ |
| Section-on-scroll reveal | ✅ subtle | ✅ very subtle |
| Page transitions | ✅ | ✅ |
| Auto-playing loops | ✅ if reduced-motion respected | ❌ |

### 5.4 `prefers-reduced-motion`

Every animation must respect it. Reduce duration to `0.01ms` (effectively off) for users who opt out. Already wired in `globals.css`; preserve when refactoring.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Do not gate *content* on motion. If a reveal animation hides content, the content must still be readable when motion is off.

---

## 6. Breakpoints + grid

### 6.1 Breakpoints

```
--bp-sm:  640px
--bp-md:  768px
--bp-lg:  1024px
--bp-xl:  1280px
--bp-2xl: 1536px
```

Mobile-first. Default styles target ≤640px.

### 6.2 Container widths

| Context | Max-width |
|---|---|
| Site shell (Showcase) | 1280px |
| Editorial reading column | 720px (≈65ch at body-lg) |
| Editorial wide media | 1080px |
| Editorial full-bleed | 100vw, padding via `--space-6` on small screens |

### 6.3 Grid

12-column for Showcase Work index; CSS subgrid for Editorial DesignSystemGrid. Outside those two, prefer flex/auto-flow over grid — grid is a tool, not a default.

---

## 7. Showcase mode spec

### 7.1 What's allowed

- `--accent` as a tinted CTA, focus ring, and active-nav indicator.
- `translateY(-2px to -4px)` hover lifts on interactive cards.
- One marquee per page (Skills section is the canonical use).
- Spring easings on entrance animations.
- `--shadow-subtle` and `--shadow-elevated` on cards.
- `--radius-md` on cards.

### 7.2 What's forbidden

- Full-page glow effects.
- Gradient text on body copy (gradient on `display-xl` headline only, and only if it earns its place — default to solid `--fg-primary`).
- Multiple accent colors in the same viewport.
- More than one motion-heavy section per page.
- Backdrop-blur. (Removed in the perf pass — see §13.3. Do not reintroduce.)

### 7.3 Motion budget

Maximum one of: marquee, spring entrance, persistent scroll-tied transform — per page. Stacking them caused the freeze incident; do not regress.

---

## 8. Editorial mode spec

### 8.1 What's allowed

- Hairline borders (`--border-hairline`) as the primary structural device.
- Numbered eyebrows (`01`, `02`, …) in `--accent`.
- Sticky sidebars on long-form sections.
- Pull quotes with a 2px `--accent` left rule.
- Sharp corners (`--radius-none` / `--radius-xs`).
- Subtle staggered reveal on grids (≤200ms stagger, ≤480ms duration).

### 8.2 What's forbidden

- Gradients of any kind.
- Glow effects.
- Marquees.
- DotNav (it implies "pages of marketing"; case studies have one reading flow).
- CursorGlow.
- `--shadow-*` (use hairlines only).
- `--radius-md` or larger.
- Hover lifts on non-interactive elements.

### 8.3 Voice in Editorial

Editorial copy carries the case study's argument. Visual restraint exists so the *reasoning* is what stays with the reader. If you find yourself adding an icon to "spice up" a section, the section's writing isn't earning its space.

### 8.4 Mono body in Editorial

Body is mono. This shapes the writing:
- Sentences are shorter than they'd be in sans body. Aim for 15–22 words.
- Paragraphs cap at 5 lines at 60ch. Beyond that, break or summarize.
- Lists carry weight in mono — use them where sans would use prose.
- Numbers, file paths, identifiers, and code render as body — no separate styling needed.

---

## 9. Component patterns — Showcase

> All Showcase components live in `components/sections/` and `components/ui/`.

### 9.1 Hero (`components/sections/Hero.tsx`)

**Anatomy:**
- Eyebrow (`eyebrow`, `--fg-muted`) — optional location/role tag.
- Headline (`display-xl`, `--fg-primary`) — 1–2 lines, sentence case.
- Subhead (`body-lg`, `--fg-secondary`) — max 2 sentences, ≤60ch.
- CTA cluster — primary button (`--accent`), secondary link (text + arrow).

**States:**
- Default
- Reduced-motion (no marquee, no spring)

**Rules:**
- One Hero per page.
- The headline never gets a gradient unless the gradient is the page's single moment of color theatre.
- Subhead can never be `display-*` sized.

### 9.2 About (`components/sections/About.tsx`)

**Anatomy:**
- Section eyebrow + `headline`.
- Two-column on `lg`+: copy left (60ch), portrait/visual right.
- One stat or pull-line (optional, `display-md` weight 700).

**Rules:**
- Copy is `body-lg`. Always.
- Portrait/visual is decorative; remove it if it doesn't earn its space.

### 9.3 Skills (`components/sections/Skills.tsx`)

**Anatomy:**
- Section eyebrow + `headline`.
- Marquee row(s) of `TagChip` components.

**Rules:**
- Marquee speed: 28s linear infinite (matches existing `.animate-marquee`).
- Pause on hover OR on `prefers-reduced-motion`.
- Max two rows.

### 9.4 Experience (`components/sections/Experience.tsx`)

**Anatomy:**
- Timeline entries: company / role / dates / 1–2 bullet lines.
- Hairline border-left, dot marker per entry, `--accent` for the current role's dot.

**Rules:**
- No card shadows. Hairlines only (this section borrowed Editorial's restraint and it works).
- Bullet lines are `body-sm`.
- Dates use `mono-sm`.

### 9.5 Work (`components/sections/Work.tsx`)

**Anatomy:**
- Section eyebrow + `headline`.
- Grid of `ProjectCard` — 1 col mobile, 2 col tablet, 3 col desktop.

**Rules:**
- Cards use `--shadow-subtle` and `--radius-md`.
- One row of cards per "category" (don't mix client work with side projects in the same row).

### 9.6 Contact (`components/sections/Contact.tsx`)

**Anatomy:**
- Headline (`display-md` or `display-lg` depending on page weight).
- Email link (`title`, accent on hover).
- Social links row, icons only, `--fg-secondary` → `--fg-primary` on hover.

**Rules:**
- No form. A direct email link converts better and signals seniority.
- Email opens `mailto:`. Do not interpose a contact modal.

### 9.7 FloatingNav (`components/ui/FloatingNav.tsx`)

**Anatomy:**
- Top-of-viewport pill, `--bg-surface` opaque (no backdrop-blur — see §13.3).
- Logo left, section links center, CTA right.
- Active section: `--accent` underline 2px below link.

**States:**
- Default (top of page): full opacity, expanded.
- Scrolled: opacity ramps from 0 → 1 between 80px and 160px scroll. Compact spacing.
- Mobile (<md): hamburger; menu opens as full-height sheet.

**Rules:**
- Must work without the scroll listener (degrade gracefully). Test with JS throttled.

### 9.8 DotNav (`components/ui/DotNav.tsx`)

**Anatomy:**
- Right-edge fixed column of dots, one per Showcase section.
- Active dot: filled `--accent`, scale 1.25.
- Inactive: 1px `--border-strong`, no fill.

**Rules:**
- Showcase only. Do not render in Editorial mode.
- Hide on `<lg`.
- Must respect `prefers-reduced-motion` for the scale transition.

### 9.9 ProjectCard (`components/ui/ProjectCard.tsx`)

**Anatomy:**
- Cover image (16:10 aspect ratio).
- Title (`title`).
- Tag row (TagChip × 1–4).
- Optional one-line summary (`body-sm`, `--fg-secondary`).

**States:**
- Default
- Hover: `translateY(-4px)`, `--shadow-elevated`.
- Focus-visible: 2px `--focus-ring`, 2px offset.

**Rules:**
- No backdrop-blur (perf, §13.3).
- One image per card; no carousels.

### 9.10 TagChip (`components/ui/TagChip.tsx`)

**Anatomy:**
- 1px `--border-hairline`, transparent background.
- `eyebrow` text size, `--fg-secondary`.
- `--radius-full`, padding `--space-2 --space-3`.

**States:**
- Default
- Hover (interactive only): `--border-strong`, `--fg-primary`.
- Selected: `--accent-muted` background, `--accent` border.

**Rules:**
- No backdrop-blur (perf, §13.3).
- Use sparingly. A row of 12 chips is noise.

---

## 10. Component patterns — Editorial

> Editorial components live in `components/work/` (case-study primitives).

### 10.1 SectionHeader

**Anatomy:**
- Numbered eyebrow (`01` — `eyebrow`, `--accent`).
- Title (`display-md`, `--fg-primary`).
- 2px hairline rule beneath, full column width.
- Optional one-line description (`body-lg`, `--fg-secondary`).

**Rules:**
- Numbers are explicit (`01`, `02`, …) — this is the Editorial signature.
- Sequence matters; numbers must read in order top-to-bottom.

### 10.2 ProjectAtGlance

**Anatomy:**
- Metadata grid: Role / Timeframe / Team / Stack / Status.
- Each cell: eyebrow label + body value.
- Status: dot (`--status-success` or `--status-warning`) + word.

**Rules:**
- 4 cols on `lg`+, 2 cols below.
- All hairlines, no shadows.
- The animated status dot is the only motion this component uses.

### 10.3 ProblemSpace

**Anatomy:**
- Two-column on `lg`+: narrative left (65ch), sticky sidebar right (constraints, stakes, scope).
- Editorial body copy (`body-lg`).
- Sidebar uses `body-sm` and hairline-bordered list.

**Rules:**
- Sidebar items are facts, not arguments. (If it has a verb, it goes in the narrative.)
- Sticky offset: 96px from top.

### 10.4 PullQuote

**Anatomy:**
- 2px left rule in `--accent`.
- Quote in `display-md`, weight 600, `--fg-primary`.
- Attribution: eyebrow + name + role (`body-sm`, `--fg-secondary`).

**Rules:**
- One pull quote per ~2,000 words. More than that, you're padding.
- Must be a real quote, not a paraphrase.

### 10.5 CaseStudyImage

**Anatomy:**
- Aspect-ratio container (16:9, 4:5, 1:1, or full-bleed).
- Optional caption beneath (`caption`, `--fg-muted`).

**Rules:**
- Captions are sentences, not labels. ("Final dashboard, week 6 — annotation density doubled after merchant interviews." — not "Dashboard.")
- Full-bleed images break the reading column intentionally; use to mark a structural pivot, not for decoration.

### 10.6 HeroStory

**Anatomy:**
- Five labeled blocks in sequence: **Challenge** / **Insight** / **Approach** / **Tradeoff** / **Outcome**.
- Each block: eyebrow label + 1–3 paragraph narrative.
- Optional inline image per block.

**Rules:**
- All five blocks must be filled. If one is empty, the case study isn't ready.
- Tradeoff cannot be empty. ("None" is not an answer.)

### 10.7 DesignSystemGrid

**Anatomy:**
- Hairline-bordered cells in CSS subgrid.
- Each cell: token swatch / label / value.
- Staggered reveal (≤200ms stagger, ≤480ms duration).

**Rules:**
- Used to *show* a system, not to decorate. Don't sprinkle it across pages.
- If a cell's content is just decorative, delete the cell.

### 10.8 Reflection

**Anatomy:**
- Numbered learnings: `01` (italic title) — paragraph.
- Italic title in General Sans 600.
- Paragraph in `body-lg`.

**Rules:**
- 3–5 reflections max. More than 5 is a list, not a reflection.
- Must include at least one thing you'd do differently.

---

## 11. Accessibility

### 11.1 Contrast

- `--fg-primary` on `--bg-canvas`: AAA (≥7:1).
- `--fg-secondary` on `--bg-canvas`: AA (≥4.5:1) — verify on every component change.
- `--fg-muted` is **decorative only**; never use for primary information.
- `--accent` on `--bg-canvas`: AA Large (≥3:1) — sufficient for headlines and 18px+ text. Do not use accent for body copy (fails AA).

### 11.2 Focus

- Every focusable element renders a visible focus ring.
- `outline: 2px solid var(--focus-ring)` with `outline-offset: 2px`.
- Never use `outline: none` without an equivalent visual replacement.
- Skip-to-content link required at the top of every page.

### 11.3 Motion

- All animation respects `prefers-reduced-motion: reduce` (§5.4).
- Marquees pause for users who opt out.
- No animation longer than 720ms (loses attention, perceived as broken).

### 11.4 Semantic HTML

- `<main>` wraps the primary content of every page.
- One `<h1>` per page.
- Heading levels do not skip (h1 → h2 → h3, not h1 → h3).
- Buttons that look like links use `<a>`. Buttons that perform actions use `<button>`.
- Decorative SVGs: `aria-hidden="true"`. Meaningful SVGs: `<title>` element.

### 11.5 Keyboard

- All interactive elements reachable by Tab.
- Tab order matches visual order.
- Modal/sheet components trap focus.
- Esc closes any open overlay.

---

## 12. Content + voice

### 12.1 Tone

| Surface | Tone |
|---|---|
| Hero headlines | Confident, specific. State what you do, not what you "love." |
| Body copy | Clear, evidence-led. Numbers over adjectives. |
| Case study narrative | First-person, deliberate. "I" not "we" unless it really was a we. |
| Microcopy | Short, lowercase OK ("about", "work", "contact" in nav). |

### 12.2 Voice rules

- No "passionate," no "leverage," no "ecosystem," no "synergy."
- Specific over general: "shipped a refactor that cut p95 by 40%" beats "improved performance."
- Past tense for completed work, present for ongoing.
- Numbers as digits in body (`5 years`, not `five years`). Spelled out only when starting a sentence.

### 12.3 Capitalization

- Sentence case for headlines.
- Title case forbidden everywhere.
- ALL CAPS only for `eyebrow` role.
- Brand names in their canonical casing (iPhone, GitHub, e.g.).

### 12.4 Microcopy patterns

| Pattern | Example |
|---|---|
| CTA primary | "See the work" / "Read the case study" — verb-led, specific. |
| CTA secondary | "Email me" — no exclamation marks. |
| Empty state | Honest. "No projects in this category yet." Don't pretend. |
| Loading | Skeletons over spinners. If a spinner is needed, it's `--fg-muted`. |
| Error | "Couldn't load this. [Reload]" — not "Oops!" |

---

## 13. Implementation notes

### 13.1 Tailwind 4 `@theme` mapping

`app/globals.css` is the source. Tokens map into Tailwind 4's `@theme` block so utility classes pick them up automatically. Type scale is exposed as `@layer components` classes alongside.

```css
@import "tailwindcss";

@theme {
  /* fonts */
  --font-display: "General Sans", system-ui, sans-serif;
  --font-mono: var(--font-mono-stack), ui-monospace, Menlo, monospace;

  /* surfaces, foreground, borders, accent, status — see globals.css for values */

  /* decorative (used sparingly) */
  --color-grid-line: rgba(255, 255, 255, 0.028); /* hero grid pattern */

  /* radii — full scale */
  --radius-none: 0;
  --radius-xs: 2px;
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-full: 9999px;

  /* shadows, motion durations + eases — see globals.css */
}

/* focus + selection — :root tokens, not @theme */
:root {
  --focus-ring: var(--color-accent);
  --selection-bg: var(--color-accent-muted);
  --selection-fg: var(--color-fg-primary);
}

/* type scale (§3.2) as @layer components — encodes family + size + leading + tracking + weight */
@layer components {
  .display-xl { font-family: var(--font-display); font-size: 6rem; line-height: 0.95; ... }
  /* …display-lg, display-md, headline, title, body-lg, body, body-sm, caption, eyebrow */
}
```

Use utilities: `bg-bg-canvas`, `text-fg-primary`, `border-border-hairline`, `font-display`, `font-mono`, `rounded-md`, etc. Type roles use the named classes: `<h1 class="display-xl">`, `<p class="body-lg">`, `<span class="eyebrow">`. Don't use raw hex anywhere outside `globals.css`.

### 13.2 Suggested file structure

```
app/
  globals.css           # @theme tokens (above)
  layout.tsx            # font loading (Syne, Geist Mono)
components/
  ui/                   # Showcase primitives
  sections/             # Showcase sections (Hero, About, …)
  work/                 # Editorial primitives (SectionHeader, PullQuote, …)
design.md               # ← this file
```

### 13.3 Migration notes — completed

The April 27 perf pass and the April 28 normalize pass cleared the legacy violations:

- ✅ **`CursorGlow.tsx`**: deleted.
- ✅ **Hero gradient text**: removed. Hero headline is solid `--fg-primary` with the outline-stroke "ADLY" treatment as the single moment of typographic theatre.
- ✅ **Pink/purple gradient (`#ff3cac`/`#7b2fff`)**: removed from `@theme`. Iris (`--accent`) is the only chromatic color.
- ✅ **`@keyframes glow`**: deleted.
- ✅ **Backdrop-blur**: confirmed absent across nav, project cards, project header, at-glance, tag chips, experience timeline, contact, about. Do not reintroduce.
- ✅ **Token-name truth (Apr 28)**: `--font-syne` Tailwind utility renamed to `--font-display` (face is General Sans). UI buttons in Hero and Contact moved from display to mono per §3.1. Hardcoded `rgba(255,255,255,…)` in Hero replaced with `--color-grid-line` (decorative grid) and `--color-border-strong` (text-stroke). Card radii (`rounded-2xl`, `rounded-3xl`, `rounded-xl`) snapped to `--radius-md`.

### 13.4 Font loading

Two faces only: General Sans (display, via Fontshare CDN) and Geist Mono (everything else, via `next/font`).

```tsx
// app/layout.tsx
import { Geist_Mono } from "next/font/google";

const geistMono = Geist_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-mono-stack",
  display: "swap",
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`dark ${geistMono.variable}`}>
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link
          rel="stylesheet"
          href="https://api.fontshare.com/v2/css?f[]=general-sans@500,600,700,800&display=swap"
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
```

In `globals.css`, both are exposed through `@theme` tokens:

```css
--font-display: "General Sans", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: var(--font-mono-stack), ui-monospace, SFMono-Regular, Menlo, monospace;
```

Tailwind utilities: `font-display` (headlines) and `font-mono` (body, UI, labels). Drop any reference to `font-syne`, `Syne`, or `GeistSans`.

### 13.5 Performance

- LCP target: ≤2.5s on 4G mid-tier mobile.
- CLS target: ≤0.05.
- INP target: ≤200ms.
- Images: Next.js `<Image>` everywhere; specify width/height; use `priority` on the Hero image only.
- No third-party scripts in the critical path. Analytics defers to `idle`.

---

## 14. Open questions / TODO

- [ ] **Light mode values.** Names are stable; values pending. Target: when site has 5+ pages.
- [ ] **Hero gradient call.** Keep one moment of `--accent` gradient on `display-xl`, or go fully solid? Test both, decide based on conversion.
- [ ] **CursorGlow.tsx fate.** Recommendation: delete. Awaiting confirmation.
- [ ] **Font preloading.** General Sans loads via Fontshare CDN (no preload), Geist Mono via `next/font`. Audit LCP with Lighthouse — if General Sans hurts LCP, self-host the 700/800 weights and `<link rel="preload">` them.
- [ ] **Mono readability monitoring.** Mono body is opinionated. After 3+ case studies ship, gut-check whether Editorial mode reads well at length. If not, the escape hatch is allowing General Sans (only) for `body-lg` in Editorial — but treat this as a last resort.
- [ ] **Type scale migration.** §3.2 scale now exists as `@layer components` classes (`.display-xl`, `.body-lg`, etc.) in globals.css. Existing components still hand-roll `text-[clamp(...)]` values. Migrate component-by-component when each section is next touched.
- [ ] **Print styles.** Not addressed. Add when a case study needs to be printable as a leave-behind.

---

*If you change a token, update this file in the same commit. The doc is canonical; drift here is design debt.*

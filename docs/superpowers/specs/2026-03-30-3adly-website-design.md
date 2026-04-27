# 3adly Website — Design Spec
**Date:** 2026-03-30
**Status:** In progress — brainstorming session paused, resume tomorrow
**Project path:** `/Users/nour/Desktop/adly/claude/3adly-website/`

---

## Overview

Ahmed Adly's personal website — a CV + portfolio site with a bold, creative design that positions him as a **Product Designer who builds with AI**.

---

## Goals

1. **Get hired** — appeal to recruiters and hiring managers
2. **Attract freelance clients** — convince businesses to hire for design projects
3. **Build personal brand** — establish identity as a designer + AI builder

---

## Positioning

> *"Product Designer who builds — using AI to go from idea to working product."*

Key differentiator: not just a designer, but someone who ships using AI tools. This is rare in 2026 and commands higher rates.

---

## Visual Direction

**Bold & Expressive**

- Dark background (`#080810` range)
- Vivid gradient accents: pink (`#ff3cac`) → purple (`#7b2fff`)
- Ambient glow / radial gradient effects
- Heavy typography, uppercase labels
- Glowing tag chips for skills
- Cursor glow effect
- Motion-forward — animations are part of the identity

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Next.js 14+ (App Router) |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Deployment | Vercel |
| Data | JSON files (projects, experience) — no CMS needed initially |

**Why Next.js:** Dynamic, SEO-ready, easy to add features later, free Vercel hosting, projects managed via JSON without touching code.

---

## Layout

**Immersive Single-Page Scroll**

One long page with cinematic sections. Dot navigation on the side. Smooth scroll animations as each section enters the viewport. Floating navbar appears after first scroll.

---

## Page Sections (Main Page `/`)

### 01 — Hero
- Full viewport height
- Ambient glow background (radial gradients, no image)
- Name: **AHMED ADLY** — large, bold, commanding
- Tagline: `Product Designer · AI Builder` (gradient text)
- Two CTAs: `See my work ↓` (primary) + `Download CV` (secondary)
- Animated entrance (Framer Motion)

### 02 — Selected Work
- Section title + subtitle
- 5 project cards in a grid/masonry layout
- Each card: cover image, project name (anonymized for some), tags (`Design` / `AI` / `Mobile` / `Web`), year
- Hover: overlay with short description
- Click: navigates to `/work/[slug]` case study page
- Staggered scroll-in animation

### 03 — About
- Split layout: photo/avatar left, text right
- 2–3 short paragraphs — personal story, not a CV dump
- Animated stat counters: years of experience, projects delivered, tools mastered
- Tone: direct, human, confident

### 04 — Skills & Tools
- Two groups:
  - **Design:** Figma, Prototyping, Design Systems, User Research, Branding
  - **Build:** Next.js, Claude API, Tailwind, Framer Motion, Python
- Displayed as glowing chip tags
- Subtle entrance animation per chip

### 05 — Experience
- Vertical timeline
- Each entry: Role · Company · Year range · One-line description
- Clean and scannable for recruiters

### 06 — Contact
- Big bold CTA: `Available for work`
- Email link (mailto)
- Social links: LinkedIn, Behance (or Dribbble)
- Ambient glow footer effect

---

## Extra Details (Main Page)
- **Floating nav:** Hidden on load, slides in after first scroll. Links: Work · About · Contact. "Available for work" green dot badge.
- **Cursor glow:** Soft radial gradient follows cursor (desktop only)
- **Side dot nav:** Small dots on right edge, each represents a section

---

## Project Case Study Pages (`/work/[slug]`)

Each of the 5 projects gets a dedicated page:

**Structure:**
1. **Header** — Project name, tags, year, hero image
2. **Overview** — The problem / challenge (1–2 paragraphs)
3. **Process** — How you approached it (research, iterations, decisions)
4. **Solution** — Final designs, key screens, outcomes
5. **Next Project** — Link to next case study

**Note on naming:** Some projects will use anonymized names (e.g. "Fintech Platform" instead of Naya, "Music Streaming App" instead of Anaphora) due to copyright/NDA considerations.

---

## Featured Projects (5 total)

| # | Working Title | Original | Type |
|---|---|---|---|
| 1 | Alkoupon | Alkoupon | Web / AI |
| 2 | Fintech Platform | Naya Finance | App / Design System |
| 3 | Music Streaming App | Anaphora | Mobile / Brand |
| 4 | Media CMS | Rotana | Web / Complex UI |
| 5 | Event App | Riseup | Mobile / Brand |

---

## File Structure (planned)

```
3adly-website/
├── app/
│   ├── page.tsx              ← main single-page site
│   ├── work/
│   │   └── [slug]/
│   │       └── page.tsx      ← case study page
│   └── layout.tsx
├── components/
│   ├── sections/             ← Hero, Work, About, Skills, Experience, Contact
│   ├── ui/                   ← CursorGlow, FloatingNav, DotNav, ProjectCard
│   └── work/                 ← CaseStudyLayout, ProjectHeader
├── data/
│   ├── projects.json         ← project list + metadata
│   └── experience.json       ← work history
├── public/
│   └── work/                 ← project images
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-03-30-3adly-website-design.md  ← this file
```

---

## What's Left to Decide (next session)

- [x] Review and approve this spec
- [x] Finalize the tagline / hero copy (Tagline: "Product Designer · AI Builder", Intro: "I turn complex ideas into shipped products using design thinking and AI.")
- [x] Confirm experience timeline entries (Extracted from 2024 CV)
- [x] Decide on photo vs illustration/avatar for About section (Chose: Illustration)
- [x] Confirm social links to include (LinkedIn, Behance)
- [x] Start implementation plan (Blueprint created and running)

---

## Visual Companion Session

Server started during brainstorming — screens saved at:
`.superpowers/brainstorm/25475-1774906457/`

Screens created:
- `visual-direction.html` — 3 visual styles (chose: Bold & Expressive)
- `layout-concept.html` — 3 layout types (chose: Immersive Single-Page Scroll)
- `page-sections.html` — section flow map

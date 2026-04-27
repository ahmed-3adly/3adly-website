# Blueprint: Ahmed Adly's Personal Website

**Objective:** Build a bold, creative personal website for Ahmed Adly using Next.js 14, Tailwind CSS, and Framer Motion, positioning him as a "Product Designer who builds with AI".

**Source Specification:** `docs/superpowers/specs/2026-03-30-3adly-website-design.md`
**Mode:** Direct Execution (no git/gh detected)

## Execution Rules
- Execute exactly one step at a time.
- Verify the step using the Verification Commands before proceeding.
- Do not skip steps or change the dependency order.
- This is a direct execution plan (run commands and edit files directly in the repository).

---

## Step 1: Scaffold Next.js Project & Configure Styling
**Context:** The project directory contains only specs and some brainstorm HTML files. We need to initialize a fresh Next.js 14+ App Router project (no `src/` directory, to match the spec's `app/` at the root), configure Tailwind with the specified brand colors, and install necessary dependencies like Framer Motion and Lucide icons.
**Task List:**
- Initialize Next.js in the current directory (`npx create-next-app@latest . --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*" --use-npm`). Wait, since we are in a non-empty directory, create-next-app might complain. Alternatively, create in a temp folder and move the files, or create manually. Actually, `create-next-app` usually allows it if the directory only contains hidden folders or non-conflicting files. Alternatively, run `npm init -y` and install `next react react-dom` manually. Let's use `npx create-next-app@latest . --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*" --use-npm --force` or similar, or just create `package.json` manually if it fails.
- Install `framer-motion`, `lucide-react`, and `clsx` + `tailwind-merge` for UI components.
- Configure `tailwind.config.ts`: Add custom colors `darkBg` (`#080810`), `accentPink` (`#ff3cac`), and `accentPurple` (`#7b2fff`).
- Update `app/globals.css` with dark mode base styles and radial gradients as described in the spec.
**Verification:**
- `npm run build` succeeds.
- Next.js default page is accessible via `npm run dev` (manually verified or curl).
**Exit Criteria:** Next.js project is fully scaffolded, Tailwind is configured with brand colors, and Framer Motion is installed.

## Step 2: Establish Data Layer & Types
**Context:** The site relies on local JSON files (`data/projects.json` and `data/experience.json`) for content rather than a CMS. We need to create these structured files and their corresponding TypeScript interfaces to ensure type safety across the application.
**Task List:**
- Create `types/index.ts` defining `Project` and `Experience` interfaces.
- Create `data/projects.json` containing the 5 featured projects from the spec: "Alkoupon", "Fintech Platform", "Music Streaming App", "Media CMS", and "Event App".
- Create `data/experience.json` with 3-4 placeholder entries (Role, Company, Year range, Description).
- Create placeholder images for the 5 projects in `public/work/` (e.g., using simple SVGs or placeholder boxes) so the UI doesn't break.
**Verification:**
- Run `npx tsc --noEmit` to ensure types are valid.
- Write a quick Node script or test file to parse the JSON files using the defined types, ensuring they match.
**Exit Criteria:** Data files are created, correctly typed, and accessible.

## Step 3: Core UI Components (Nav, Cursor, Tag Chips)
**Context:** Before building complex sections, we need the reusable UI primitives specified in the design: a custom cursor glow, floating navigation, dot navigation for scroll tracking, and glowing tag chips for skills.
**Task List:**
- Build `components/ui/CursorGlow.tsx` (a Framer Motion div that tracks mouse position).
- Build `components/ui/FloatingNav.tsx` (sticky/fixed nav that appears after scrolling past hero).
- Build `components/ui/DotNav.tsx` (vertical right-aligned dots linked to section IDs).
- Build `components/ui/TagChip.tsx` (pill shape with glow effect for skills).
- Build `components/ui/ProjectCard.tsx` (grid item with hover overlay and Framer Motion entrance).
**Verification:**
- Import and render all components temporarily in `app/page.tsx`.
- Run `npm run build` to ensure no compile or lint errors.
**Exit Criteria:** Reusable UI components exist, use Framer Motion correctly, and follow the visual direction.

## Step 4: Landing Page Sections (Hero, About, Skills, Experience, Contact)
**Context:** The main page `/` is an immersive single-page scroll experience. We need to build individual sections matching the visual direction (dark background, large typography, glowing effects).
**Task List:**
- Build `components/sections/Hero.tsx`: Full viewport height, ambient glow, bold name, tagline, and CTAs.
- Build `components/sections/About.tsx`: Split layout with a placeholder avatar/photo, short bio paragraphs, and animated stat counters.
- Build `components/sections/Skills.tsx`: Two groups ("Design" and "Build") using the `TagChip` component.
- Build `components/sections/Experience.tsx`: Vertical timeline mapping over `data/experience.json`.
- Build `components/sections/Contact.tsx`: Bold CTA, email link, social links, ambient footer glow.
**Verification:**
- `npm run build` and `npm run lint` succeed.
**Exit Criteria:** All individual sections are implemented and ready to be assembled.

## Step 5: Assembly & Selected Work Section
**Context:** We must assemble all sections into the single-page layout in `app/page.tsx` and implement the "Selected Work" section, which maps over the `projects.json` data to display a grid of project cards.
**Task List:**
- Build `components/sections/Work.tsx`: Read data from `data/projects.json` and render a grid/masonry of `ProjectCard`s.
- Update `app/page.tsx` to include all sections sequentially (`Hero`, `Work`, `About`, `Skills`, `Experience`, `Contact`) with correct IDs for navigation.
- Integrate `CursorGlow`, `FloatingNav`, and `DotNav` into the main layout or page.
**Verification:**
- Check for hydration errors or React key warnings in the console (if running dev).
- Ensure `npm run build` succeeds without errors.
**Exit Criteria:** The home page is completely functional and visually aligns with the spec.

## Step 6: Dynamic Case Study Pages
**Context:** Each of the 5 projects needs a dedicated case study page accessible via `/work/[slug]`. These pages read from `projects.json` and display detailed project information.
**Task List:**
- Create dynamic route `app/work/[slug]/page.tsx`.
- Build `components/work/ProjectHeader.tsx` (title, tags, year, hero image).
- Build `components/work/CaseStudyLayout.tsx` for structured content (Overview, Process, Solution, Next Project link).
- Implement `generateStaticParams` or dynamic data fetching in `[slug]/page.tsx` to generate paths for the 5 projects based on `projects.json`.
- Add a 404/not-found fallback for invalid slugs.
**Verification:**
- Run `npm run build` to ensure static pages for all 5 projects are successfully generated during the build step.
**Exit Criteria:** All case study pages are functional, dynamically generated, and styled correctly.
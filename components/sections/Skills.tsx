"use client";

import { motion } from "framer-motion";
import { TagChip } from "@/components/ui/TagChip";

const DESIGN_SKILLS = [
  "Figma",
  "Prototyping",
  "Design Systems",
  "User Research",
  "Branding",
  "Wireframing",
  "Interaction Design",
  "Accessibility",
];

const BUILD_SKILLS = [
  "Next.js",
  "Claude API",
  "Tailwind CSS",
  "Framer Motion",
  "Python",
  "TypeScript",
  "React",
  "Vercel",
];

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

export function Skills() {
  return (
    <section id="skills" aria-labelledby="skills-heading" className="relative py-32 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.p
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[11px] font-semibold tracking-[0.2em] uppercase text-accent mb-4 font-mono"
        >
          04 — Skills & Tools
        </motion.p>

        <motion.h2
          id="skills-heading"
          custom={0.1}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[clamp(2rem,5vw,3.5rem)] font-black tracking-tight text-fg-primary leading-none mb-16 font-display"
        >
          What I work with
        </motion.h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-16">
          {/* Design group */}
          <div>
            <motion.h3
              custom={0.2}
              variants={FADE_UP}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-80px" }}
              className="text-[11px] font-semibold text-fg-secondary tracking-[0.18em] uppercase mb-6 font-mono"
            >
              Design
            </motion.h3>
            <div className="flex flex-wrap gap-3">
              {DESIGN_SKILLS.map((skill, i) => (
                <TagChip key={skill} label={skill} delay={0.25 + i * 0.05} />
              ))}
            </div>
          </div>

          {/* Build group */}
          <div>
            <motion.h3
              custom={0.2}
              variants={FADE_UP}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-80px" }}
              className="text-[11px] font-semibold text-fg-secondary tracking-[0.18em] uppercase mb-6 font-mono"
            >
              Build
            </motion.h3>
            <div className="flex flex-wrap gap-3">
              {BUILD_SKILLS.map((skill, i) => (
                <TagChip key={skill} label={skill} delay={0.25 + i * 0.05} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

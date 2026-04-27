"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";

const STATS = [
  { value: "15+", label: "Years of experience" },
  { value: "50+", label: "Products shipped" },
  { value: "10+", label: "Design systems built" },
  { value: "∞", label: "Problems solved" },
];

const FADE_UP = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay: i * 0.1 },
  }),
};

function StatCard({ value, label, index }: { value: string; label: string; index: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });

  return (
    <motion.div
      ref={ref}
      custom={index}
      variants={FADE_UP}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
      className="flex flex-col items-center md:items-start gap-1"
    >
      <span className="text-5xl font-black tracking-tight text-fg-primary tabular-nums font-syne">
        {value}
      </span>
      <span className="text-[11px] text-fg-muted uppercase tracking-[0.18em] font-mono">
        {label}
      </span>
    </motion.div>
  );
}

export function About() {
  const sectionRef = useRef<HTMLElement>(null);
  const inView = useInView(sectionRef, { once: true, margin: "-80px" });

  return (
    <section id="about" ref={sectionRef} className="relative py-32 px-6">
      <div className="relative z-10 max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        {/* Left — avatar + stats */}
        <div className="flex flex-col items-center md:items-start gap-12">
          <motion.div
            initial={{ opacity: 0, scale: 0.92 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="relative w-56 h-56 rounded-3xl overflow-hidden border border-border-hairline bg-bg-surface flex items-center justify-center"
          >
            <span className="text-7xl font-black tracking-tighter select-none text-fg-primary font-syne">
              AA
            </span>
          </motion.div>

          <div className="grid grid-cols-2 gap-x-10 gap-y-8">
            {STATS.map((s, i) => (
              <StatCard key={s.label} value={s.value} label={s.label} index={i} />
            ))}
          </div>
        </div>

        {/* Right — text */}
        <div className="flex flex-col gap-8">
          <motion.p
            custom={0}
            variants={FADE_UP}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
            className="text-[11px] text-accent uppercase tracking-[0.2em] font-semibold font-mono"
          >
            03 — About me
          </motion.p>

          <motion.h2
            custom={1}
            variants={FADE_UP}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
            className="text-4xl md:text-5xl font-black tracking-tight leading-tight text-fg-primary font-syne"
          >
            I design products that people actually use.
          </motion.h2>

          <motion.p
            custom={2}
            variants={FADE_UP}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
            className="text-fg-secondary leading-relaxed text-[1.0625rem] font-mono"
          >
            I&apos;m a Product Designer with 15+ years of experience turning complex
            problems into clean, intuitive digital experiences. My work lives at
            the intersection of design thinking and modern technology — especially AI.
          </motion.p>

          <motion.p
            custom={3}
            variants={FADE_UP}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
            className="text-fg-muted leading-relaxed font-mono"
          >
            I don&apos;t just design screens — I collaborate with engineering,
            prototype with code, and ship products end to end. Currently at{" "}
            <span className="text-fg-primary font-medium">Extreme Solution</span>,
            building products used by thousands daily.
          </motion.p>

          <motion.div
            custom={4}
            variants={FADE_UP}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
            className="flex flex-wrap gap-3 pt-2"
          >
            {["Figma", "Next.js", "Framer", "AI Prototyping", "Design Systems"].map((tool) => (
              <span
                key={tool}
                className="px-4 py-1.5 rounded-full text-xs border border-border-hairline text-fg-secondary font-mono tracking-wider"
              >
                {tool}
              </span>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}

"use client";

import { motion } from "framer-motion";
import experienceData from "@/data/experience.json";
import { Experience as ExperienceType } from "@/types";

const experience = experienceData as ExperienceType[];

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

export function Experience() {
  return (
    <section id="experience" className="relative py-32 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.p
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[11px] font-semibold tracking-[0.2em] uppercase text-accent mb-4 font-mono"
        >
          05 — Experience
        </motion.p>

        <motion.h2
          custom={0.1}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[clamp(2rem,5vw,3.5rem)] font-black tracking-tight text-fg-primary leading-none mb-16 font-syne"
        >
          Where I&apos;ve worked
        </motion.h2>

        {/* Timeline */}
        <div className="relative">
          <div
            className="absolute left-0 top-0 bottom-0 w-px ml-[5px] bg-border-hairline"
            aria-hidden="true"
          />

          <div className="space-y-12 pl-10">
            {experience.map((entry, i) => (
              <motion.div
                key={entry.id}
                custom={0.2 + i * 0.1}
                variants={FADE_UP}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-80px" }}
                className="relative group"
              >
                {/* Timeline dot */}
                <div
                  className={`absolute -left-10 top-1 w-3 h-3 rounded-full border-2 transition-colors duration-300 ${
                    i === 0
                      ? "border-accent bg-bg-canvas"
                      : "border-border-strong bg-bg-canvas group-hover:border-accent"
                  }`}
                  aria-hidden="true"
                />

                <div className="border border-border-hairline rounded-xl p-6 transition-colors duration-300 group-hover:border-border-strong">
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-3">
                    <div>
                      <h3 className="text-lg font-bold text-fg-primary font-syne">
                        {entry.role}
                      </h3>
                      <p className="text-sm font-medium mt-0.5 text-accent font-mono">
                        {entry.company}
                      </p>
                    </div>
                    <span className="text-[11px] font-medium text-fg-muted tracking-[0.18em] uppercase whitespace-nowrap shrink-0 mt-0.5 font-mono tabular-nums">
                      {entry.yearRange}
                    </span>
                  </div>
                  <p className="text-fg-secondary text-sm leading-relaxed font-mono">
                    {entry.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

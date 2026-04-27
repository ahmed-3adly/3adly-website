"use client";

import { motion } from "framer-motion";
import { CaseStudyProblemSpace } from "@/types";

interface ProblemSpaceProps {
  data: CaseStudyProblemSpace;
}

export function ProblemSpace({ data }: ProblemSpaceProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6 }}
      className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-10 lg:gap-16"
    >
      <div className="space-y-6 max-w-[60ch]">
        {data.narrative.map((p, i) => (
          <p
            key={i}
            className="text-[1.0625rem] leading-[1.7] text-fg-secondary font-mono"
          >
            {p}
          </p>
        ))}
      </div>

      <aside className="border border-border-hairline p-6 md:p-7 h-fit lg:sticky lg:top-24">
        <p className="text-[11px] tracking-[0.2em] uppercase text-accent mb-5 font-mono">
          {data.sidebarLabel}
        </p>
        <ul className="space-y-4">
          {data.sidebar.map((item, i) => (
            <li key={i} className="flex gap-3 text-sm leading-relaxed text-fg-secondary font-mono">
              <span
                className="text-[11px] text-fg-muted tabular-nums pt-1 shrink-0"
                aria-hidden="true"
              >
                0{i + 1}
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </aside>
    </motion.div>
  );
}

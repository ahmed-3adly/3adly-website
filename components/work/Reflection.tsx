"use client";

import { motion } from "framer-motion";
import { CaseStudyReflection } from "@/types";

interface ReflectionProps {
  items: CaseStudyReflection[];
}

export function Reflection({ items }: ReflectionProps) {
  return (
    <div className="space-y-10">
      {items.map((item, i) => (
        <motion.div
          key={item.title}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, delay: i * 0.08 }}
          className="grid grid-cols-1 md:grid-cols-[60px_1fr] gap-4 md:gap-8 pb-10 border-b border-border-hairline last:border-b-0 last:pb-0"
        >
          <span
            className="text-[11px] tracking-[0.2em] uppercase text-accent tabular-nums pt-1 font-mono"
            aria-hidden="true"
          >
            {String(i + 1).padStart(2, "0")}
          </span>
          <div className="space-y-3">
            <h4 className="text-2xl md:text-[28px] leading-snug text-fg-primary font-syne font-bold italic">
              {item.title}
            </h4>
            <p className="text-fg-secondary text-[1.0625rem] leading-relaxed max-w-[60ch] font-mono">
              {item.body}
            </p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

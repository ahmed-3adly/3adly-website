"use client";

import { motion } from "framer-motion";
import { CaseStudyObservation } from "@/types";

interface DesignSystemGridProps {
  items: CaseStudyObservation[];
}

export function DesignSystemGrid({ items }: DesignSystemGridProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-border-hairline overflow-hidden border border-border-hairline">
      {items.map((item, i) => (
        <motion.div
          key={item.title}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, delay: i * 0.08 }}
          className="bg-bg-canvas p-7 md:p-8"
        >
          <div className="flex items-baseline gap-3 mb-3">
            <span
              className="text-[11px] tabular-nums text-accent font-mono"
              aria-hidden="true"
            >
              {String(i + 1).padStart(2, "0")}
            </span>
            <h4 className="text-fg-primary font-bold tracking-tight text-lg font-syne">
              {item.title}
            </h4>
          </div>
          <p className="text-fg-secondary text-sm leading-relaxed font-mono">
            {item.description}
          </p>
        </motion.div>
      ))}
    </div>
  );
}

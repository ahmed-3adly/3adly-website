"use client";

import { motion } from "framer-motion";

interface SectionHeaderProps {
  number: string;
  label: string;
  delay?: number;
}

export function SectionHeader({ number, label, delay = 0 }: SectionHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.5, delay }}
      className="flex items-center gap-4 mb-10"
    >
      <h2 className="text-[11px] tracking-[0.25em] uppercase text-accent shrink-0 font-mono font-semibold m-0">
        <span className="text-fg-muted mr-2" aria-hidden="true">{number}</span>
        {label}
      </h2>
      <span aria-hidden="true" className="h-px flex-1 bg-border-hairline" />
    </motion.div>
  );
}

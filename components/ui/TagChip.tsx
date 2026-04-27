"use client";

import { motion } from "framer-motion";

interface TagChipProps {
  label: string;
  delay?: number;
}

export function TagChip({ label, delay = 0 }: TagChipProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay }}
      className="inline-flex items-center px-4 py-2 rounded-full border border-border-hairline text-sm font-medium text-fg-secondary transition-colors hover:text-fg-primary hover:border-border-strong cursor-default select-none font-mono"
    >
      {label}
    </motion.div>
  );
}

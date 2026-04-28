"use client";

import { motion } from "framer-motion";

interface PullQuoteProps {
  quote: string;
}

export function PullQuote({ quote }: PullQuoteProps) {
  return (
    <motion.blockquote
      initial={{ opacity: 0, x: -16 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6 }}
      className="relative my-10 pl-6 md:pl-8"
    >
      <span aria-hidden="true" className="absolute left-0 top-1 bottom-1 w-[2px] bg-accent" />
      <p className="text-[28px] md:text-[40px] leading-[1.1] tracking-[-0.02em] text-fg-primary font-display font-bold">
        &ldquo;{quote}&rdquo;
      </p>
    </motion.blockquote>
  );
}

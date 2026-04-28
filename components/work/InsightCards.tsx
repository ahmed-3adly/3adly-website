"use client";

import { motion } from "framer-motion";

export interface Insight {
  number: string;
  title: string;
  body: string;
  quote?: string;
  attribution?: string;
}

interface InsightCardsProps {
  intro?: string;
  insights: Insight[];
}

export function InsightCards({ intro, insights }: InsightCardsProps) {
  return (
    <div className="space-y-12">
      {intro && (
        <p className="text-fg-secondary text-base md:text-[1.0625rem] leading-[1.7] max-w-[60ch] font-mono">
          {intro}
        </p>
      )}

      <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-14">
        {insights.map((insight, i) => (
          <motion.li
            key={insight.number}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: i * 0.06 }}
            className="space-y-5 pt-6 border-t border-border-hairline"
          >
            <span className="text-[11px] tracking-[0.25em] uppercase text-accent font-mono tabular-nums">
              Insight #{insight.number}
            </span>

            <h4 className="text-[1.5rem] md:text-[1.75rem] leading-[1.15] tracking-[-0.01em] text-fg-primary font-syne font-bold">
              {insight.title}
            </h4>

            <p className="text-fg-secondary text-base leading-[1.7] font-mono">
              {insight.body}
            </p>

            {insight.quote && (
              <figure className="pl-4 border-l-2 border-accent/60 mt-4 space-y-2">
                <blockquote className="text-fg-primary italic text-[1.0625rem] md:text-[1.125rem] leading-[1.5] font-syne">
                  &ldquo;{insight.quote}&rdquo;
                </blockquote>
                {insight.attribution && (
                  <figcaption className="text-[10px] tracking-[0.22em] uppercase text-fg-muted font-mono">
                    — {insight.attribution}
                  </figcaption>
                )}
              </figure>
            )}
          </motion.li>
        ))}
      </ul>
    </div>
  );
}

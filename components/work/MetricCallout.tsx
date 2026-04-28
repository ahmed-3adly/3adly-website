"use client";

import { motion } from "framer-motion";

export interface Metric {
  value: string;
  label: string;
  description?: string;
}

interface MetricCalloutProps {
  metrics: Metric[];
  intro?: string;
}

const COLS_CLASS: Record<number, string> = {
  2: "md:grid-cols-2",
  3: "md:grid-cols-3",
  4: "md:grid-cols-4",
};

export function MetricCallout({ metrics, intro }: MetricCalloutProps) {
  const cols = COLS_CLASS[metrics.length] ?? "md:grid-cols-3";

  return (
    <div className="space-y-10">
      {intro && (
        <p className="text-fg-secondary text-base md:text-[1.0625rem] leading-[1.7] max-w-[60ch] font-mono">
          {intro}
        </p>
      )}

      <div className={`grid grid-cols-1 ${cols} gap-px bg-border-hairline`}>
        {metrics.map((metric, i) => (
          <motion.div
            key={`${metric.value}-${i}`}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: i * 0.08 }}
            className="bg-bg-canvas p-8 md:p-10 space-y-3"
          >
            <p className="text-[clamp(3rem,7vw,5rem)] leading-[0.95] tracking-[-0.04em] text-accent font-syne font-bold tabular-nums">
              {metric.value}
            </p>

            <p className="text-[11px] tracking-[0.25em] uppercase text-fg-primary font-mono">
              {metric.label}
            </p>

            {metric.description && (
              <p className="text-fg-secondary text-sm leading-[1.65] font-mono max-w-[28ch]">
                {metric.description}
              </p>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}

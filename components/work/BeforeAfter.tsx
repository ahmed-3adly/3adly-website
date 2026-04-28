"use client";

import Image from "next/image";
import { motion } from "framer-motion";

export interface BeforeAfterPanel {
  label?: string;
  title: string;
  description: string;
  image?: { src: string; alt: string };
}

interface BeforeAfterProps {
  before: BeforeAfterPanel;
  after: BeforeAfterPanel;
  caption?: string;
}

export function BeforeAfter({ before, after, caption }: BeforeAfterProps) {
  return (
    <motion.figure
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6 }}
      className="space-y-5"
    >
      {caption && (
        <figcaption className="text-[11px] tracking-[0.22em] uppercase text-fg-muted font-mono">
          {caption}
        </figcaption>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-border-hairline">
        <Panel kind="before" panel={before} />
        <Panel kind="after" panel={after} />
      </div>
    </motion.figure>
  );
}

function Panel({
  kind,
  panel,
}: {
  kind: "before" | "after";
  panel: BeforeAfterPanel;
}) {
  const labelColor = kind === "after" ? "text-accent" : "text-fg-muted";
  const defaultLabel = kind === "before" ? "Before" : "After";

  return (
    <div className="bg-bg-canvas p-6 md:p-8 space-y-5">
      <p className={`text-[11px] tracking-[0.25em] uppercase font-mono ${labelColor}`}>
        {panel.label ?? defaultLabel}
      </p>

      {panel.image && (
        <div className="relative aspect-[16/10] overflow-hidden bg-bg-surface border border-border-hairline">
          <Image
            src={panel.image.src}
            alt={panel.image.alt}
            fill
            sizes="(min-width: 768px) 50vw, 100vw"
            className="object-cover"
          />
        </div>
      )}

      <h5 className="text-[1.125rem] md:text-[1.25rem] leading-[1.25] tracking-[-0.01em] text-fg-primary font-syne font-semibold">
        {panel.title}
      </h5>

      <p className="text-fg-secondary text-sm md:text-[15px] leading-[1.65] font-mono">
        {panel.description}
      </p>
    </div>
  );
}

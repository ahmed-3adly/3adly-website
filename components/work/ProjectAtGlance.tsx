"use client";

import { motion } from "framer-motion";
import { CaseStudyAtGlance } from "@/types";

interface ProjectAtGlanceProps {
  data: CaseStudyAtGlance;
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-[160px_1fr] gap-2 md:gap-8 py-5 border-b border-border-hairline last:border-b-0">
      <p className="text-[11px] tracking-[0.2em] uppercase text-fg-muted pt-1 font-mono">
        {label}
      </p>
      <div className="text-fg-primary text-[1.0625rem] leading-relaxed font-mono">
        {children}
      </div>
    </div>
  );
}

export function ProjectAtGlance({ data }: ProjectAtGlanceProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.5 }}
      className="border border-border-hairline px-6 md:px-10"
    >
      <Row label="Role">{data.role}</Row>
      <Row label="Scope">
        <ul className="space-y-1.5">
          {data.scope.map((item) => (
            <li key={item} className="flex gap-3">
              <span className="text-accent mt-1.5 shrink-0" aria-hidden="true">
                ·
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </Row>
      <Row label="Timeline">{data.timeline}</Row>
      <Row label="Team">{data.team}</Row>
      {data.context && <Row label="Context">{data.context}</Row>}
      <Row label="Status">
        <span className="inline-flex items-center gap-2">
          <span className="relative flex h-2 w-2" aria-hidden="true">
            <span className="absolute inline-flex h-full w-full rounded-full bg-status-success opacity-60 animate-ping" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-status-success" />
          </span>
          {data.status}
        </span>
      </Row>
    </motion.div>
  );
}

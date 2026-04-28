"use client";

import { motion } from "framer-motion";
import { Award, ExternalLink } from "lucide-react";
import certificationsData from "@/data/certifications.json";
import { Certification } from "@/types";

const certifications = certificationsData as Certification[];

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

export function Certifications() {
  return (
    <section id="certifications" className="relative py-32 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.p
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[11px] font-semibold tracking-[0.2em] uppercase text-accent mb-4 font-mono"
        >
          06 — Certifications
        </motion.p>

        <motion.h2
          custom={0.1}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[clamp(2rem,5vw,3.5rem)] font-black tracking-tight text-fg-primary leading-none mb-16 font-syne"
        >
          What I&apos;ve studied recently
        </motion.h2>

        <ul className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {certifications.map((cert, i) => (
            <motion.li
              key={cert.id}
              custom={0.15 + i * 0.08}
              variants={FADE_UP}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-80px" }}
              className="group relative border border-border-hairline rounded-xl p-6 transition-colors duration-300 hover:border-border-strong"
            >
              <div className="flex items-start gap-4">
                <div className="shrink-0 mt-0.5 p-2 rounded-lg border border-border-hairline text-fg-muted group-hover:text-accent group-hover:border-accent/40 transition-colors">
                  <Award size={18} aria-hidden="true" />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-3 mb-1.5">
                    <h3 className="text-base font-bold text-fg-primary font-syne leading-snug">
                      {cert.name}
                    </h3>
                    <span className="text-[10px] font-medium text-fg-muted tracking-[0.18em] uppercase whitespace-nowrap shrink-0 mt-1 font-mono tabular-nums">
                      {cert.date}
                    </span>
                  </div>

                  <p className="text-sm text-accent font-mono">
                    {cert.issuer}
                    {cert.platform && (
                      <span className="text-fg-muted">
                        {" · "}
                        {cert.platform}
                      </span>
                    )}
                  </p>

                  {cert.detail && (
                    <p className="text-xs text-fg-muted font-mono mt-1.5">
                      {cert.detail}
                    </p>
                  )}

                  {cert.distinction && (
                    <span className="inline-block mt-3 text-[10px] font-semibold tracking-[0.18em] uppercase px-2 py-0.5 rounded-sm bg-accent text-fg-primary font-mono">
                      {cert.distinction}
                    </span>
                  )}

                  {cert.credentialUrl && (
                    <a
                      href={cert.credentialUrl}
                      target="_blank"
                      rel="noreferrer noopener"
                      className="inline-flex items-center gap-1.5 mt-3 text-[11px] tracking-[0.18em] uppercase text-fg-muted hover:text-accent transition-colors font-mono"
                    >
                      Verify
                      <ExternalLink size={12} aria-hidden="true" />
                    </a>
                  )}
                </div>
              </div>
            </motion.li>
          ))}
        </ul>
      </div>
    </section>
  );
}

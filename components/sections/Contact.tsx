"use client";

import { motion } from "framer-motion";
import { Mail, ExternalLink } from "lucide-react";

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

export function Contact() {
  return (
    <section id="contact" className="relative py-40 px-6 overflow-hidden">
      <div className="relative z-10 max-w-5xl mx-auto text-center">
        <motion.p
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[11px] font-semibold tracking-[0.2em] uppercase text-accent mb-4 font-mono"
        >
          06 — Contact
        </motion.p>

        <motion.h2
          custom={0.1}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[clamp(2.5rem,7vw,6rem)] font-black tracking-tighter leading-none text-fg-primary mb-4 font-syne"
        >
          Available
          <br />
          <span className="text-accent">for work</span>
        </motion.h2>

        <motion.p
          custom={0.25}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-fg-secondary text-[1.0625rem] max-w-xl mx-auto mb-12 leading-relaxed font-mono"
        >
          Open to full-time roles and freelance projects. Let&apos;s build something great together.
        </motion.p>

        <motion.a
          custom={0.35}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          href="mailto:hello@ahmedadly.com"
          className="inline-flex items-center gap-3 px-8 py-4 rounded-full font-semibold text-fg-primary text-base bg-accent hover:bg-accent-strong transition-colors duration-200 mb-12 font-syne"
        >
          <Mail size={18} aria-hidden="true" />
          hello@ahmedadly.com
        </motion.a>

        <motion.div
          custom={0.45}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="flex items-center justify-center gap-6 font-mono"
        >
          <a
            href="https://www.linkedin.com/in/3adly/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-fg-secondary hover:text-fg-primary transition-colors duration-200 text-sm font-medium group"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
              <rect x="2" y="9" width="4" height="12" />
              <circle cx="4" cy="4" r="2" />
            </svg>
            LinkedIn
            <ExternalLink size={12} className="opacity-0 group-hover:opacity-60 transition-opacity" aria-hidden="true" />
          </a>
          <span className="w-px h-4 bg-border-hairline" aria-hidden="true" />
          <a
            href="https://www.behance.net/3adly"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-fg-secondary hover:text-fg-primary transition-colors duration-200 text-sm font-medium group"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M22 7h-7V5h7v2zm1.726 10c-.442 1.297-2.029 3-5.101 3-3.074 0-5.564-1.729-5.564-5.675 0-3.91 2.325-5.92 5.466-5.92 3.082 0 4.964 1.782 5.375 4.426.078.506.109 1.188.095 2.14H15.97c.13 1.2.836 1.9 2.189 1.9.823 0 1.45-.42 1.592-1.04l3.975.1zM15.998 13h4.462c-.075-1.4-.857-2.1-2.17-2.1-1.35 0-2.098.7-2.292 2.1zM4.512 8.771H1.5v2.084H4.5c1.196 0 1.714-.569 1.714-1.041 0-.502-.519-1.043-1.702-1.043zm-3.012 4.85h1.5c1.25 0 2.044.6 2.044 1.6 0 1-.798 1.6-2.044 1.6H1.5v-3.2zM7.5 7h-7v10h7c3.5 0 4.5-1.6 4.5-3 0-1.4-.8-2.4-2-2.8.9-.4 1.5-1.2 1.5-2.2 0-1.8-1.5-2-4-2z" />
            </svg>
            Behance
            <ExternalLink size={12} className="opacity-0 group-hover:opacity-60 transition-opacity" aria-hidden="true" />
          </a>
        </motion.div>

        <motion.p
          custom={0.55}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mt-20 text-fg-disabled text-xs tracking-wider font-mono"
        >
          © {new Date().getFullYear()} Ahmed Adly. Designed & built with AI.
        </motion.p>
      </div>
    </section>
  );
}

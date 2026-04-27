"use client";

import { useEffect, useRef } from "react";
import { motion } from "framer-motion";

const MARQUEE_ITEMS = [
  "Product Design",
  "AI Integration",
  "UX Research",
  "Design Systems",
  "Shipped Products",
  "AI Builder",
  "Product Strategy",
  "Interaction Design",
];

const FADE = {
  hidden: { opacity: 0 },
  visible: (i: number) => ({
    opacity: 1,
    transition: { delay: i * 0.12, duration: 0.7 },
  }),
};

const RISE = {
  hidden: { y: "110%", opacity: 0 },
  visible: (i: number) => ({
    y: 0,
    opacity: 1,
    transition: {
      delay: i * 0.12,
      duration: 1,
      ease: [0.16, 1, 0.3, 1] as [number, number, number, number],
    },
  }),
};

export function Hero() {
  const sectionRef = useRef<HTMLElement>(null);
  const marqueeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const marquee = marqueeRef.current;
    if (!marquee) return;
    const io = new IntersectionObserver(
      ([entry]) => {
        marquee.style.animationPlayState = entry.isIntersecting ? "running" : "paused";
      },
      { threshold: 0 }
    );
    io.observe(marquee);
    return () => io.disconnect();
  }, []);

  const scrollToWork = () =>
    document.getElementById("work")?.scrollIntoView({ behavior: "smooth" });

  const scrollToContact = () =>
    document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" });

  return (
    <section
      id="hero"
      ref={sectionRef}
      className="relative min-h-screen flex flex-col overflow-hidden"
    >
      {/* Subtle grid background */}
      <div
        aria-hidden="true"
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: [
            "linear-gradient(rgba(255,255,255,0.028) 1px, transparent 1px)",
            "linear-gradient(90deg, rgba(255,255,255,0.028) 1px, transparent 1px)",
          ].join(", "),
          backgroundSize: "64px 64px",
        }}
      />

      {/* ── Top meta strip ── */}
      <motion.div
        custom={0}
        variants={FADE}
        initial="hidden"
        animate="visible"
        className="relative z-10 flex items-center justify-between px-7 md:px-14 pt-7 font-mono"
      >
        <span className="text-[10px] tracking-[0.22em] text-fg-muted uppercase">
          Ahmed Adly&nbsp;&nbsp;/&nbsp;&nbsp;Portfolio
        </span>
        <span className="flex items-center gap-2.5 text-[10px] tracking-[0.22em] text-fg-muted uppercase">
          <span className="w-1.5 h-1.5 rounded-full bg-status-success animate-pulse" />
          Available&nbsp;·&nbsp;Cairo, EG
        </span>
      </motion.div>

      {/* ── Main content ── */}
      <div className="relative z-10 flex-1 flex flex-col justify-center px-7 md:px-14 py-8">
        {/* Name block */}
        <div>
          {/* AHMED — solid */}
          <div className="overflow-hidden">
            <motion.h1
              custom={0}
              variants={RISE}
              initial="hidden"
              animate="visible"
              className="text-[clamp(4.5rem,14vw,13rem)] font-extrabold leading-[0.85] tracking-[-0.04em] uppercase text-fg-primary font-syne"
            >
              Ahmed
            </motion.h1>
          </div>

          {/* Role separator */}
          <motion.div
            custom={2}
            variants={FADE}
            initial="hidden"
            animate="visible"
            className="flex items-center gap-3 my-3"
          >
            <div className="flex-1 h-px bg-border-hairline" />
            <span className="text-xs tracking-[0.18em] text-fg-secondary uppercase font-mono">
              Product Designer
            </span>
            <span className="text-fg-muted text-xs font-mono">×</span>
            <span className="text-xs tracking-[0.18em] text-fg-secondary uppercase font-mono">
              AI Builder
            </span>
            <div className="w-10 h-px bg-border-hairline" />
          </motion.div>

          {/* ADLY — outline */}
          <div className="overflow-hidden">
            <motion.div
              custom={1}
              variants={RISE}
              initial="hidden"
              animate="visible"
              aria-hidden="true"
              className="text-[clamp(4.5rem,14vw,13rem)] font-extrabold leading-[0.85] tracking-[-0.04em] uppercase select-none font-syne"
              style={{
                WebkitTextStroke: "1.5px rgba(255,255,255,0.16)",
                color: "transparent",
              }}
            >
              Adly
            </motion.div>
          </div>
        </div>

        {/* Horizontal rule */}
        <motion.div
          custom={4}
          variants={FADE}
          initial="hidden"
          animate="visible"
          className="mt-8 mb-7 h-px bg-border-hairline"
        />

        {/* Tagline + CTAs */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-7">
          <motion.p
            custom={5}
            variants={FADE}
            initial="hidden"
            animate="visible"
            className="text-[0.95rem] text-fg-secondary max-w-xs leading-relaxed font-mono"
          >
            Turning complex ideas into{" "}
            <span className="text-fg-primary">shipped products</span> — at the
            intersection of design craft and AI.
          </motion.p>

          <motion.div
            custom={6}
            variants={FADE}
            initial="hidden"
            animate="visible"
            className="flex items-center gap-3 shrink-0"
          >
            <button
              onClick={scrollToWork}
              className="px-6 py-2.5 text-[0.82rem] font-semibold text-fg-primary rounded-full bg-accent hover:bg-accent-strong transition-colors duration-200 font-syne"
              style={{ letterSpacing: "0.02em" }}
            >
              View Work
            </button>
            <button
              onClick={scrollToContact}
              className="px-6 py-2.5 text-[0.82rem] font-semibold text-fg-secondary rounded-full border border-border-hairline hover:text-fg-primary hover:border-border-strong transition-colors duration-200 font-syne"
              style={{ letterSpacing: "0.02em" }}
            >
              Get in Touch
            </button>
          </motion.div>
        </div>
      </div>

      {/* ── Scroll indicator ── */}
      <motion.div
        custom={8}
        variants={FADE}
        initial="hidden"
        animate="visible"
        className="relative z-10 px-7 md:px-14 pb-5 flex items-center gap-3"
      >
        <motion.div
          animate={{ y: [0, 6, 0] }}
          transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
          className="w-px h-7 bg-gradient-to-b from-border-strong to-transparent"
        />
        <span className="text-[9px] tracking-[0.3em] text-fg-muted uppercase font-mono">
          Scroll
        </span>
      </motion.div>

      {/* ── Marquee ticker ── */}
      <motion.div
        custom={9}
        variants={FADE}
        initial="hidden"
        animate="visible"
        className="relative z-10 border-t border-border-hairline overflow-hidden py-3"
      >
        <div ref={marqueeRef} className="flex animate-marquee whitespace-nowrap">
          {[...MARQUEE_ITEMS, ...MARQUEE_ITEMS].map((item, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-4 mx-5 font-mono"
            >
              <span className="text-[9px] tracking-[0.3em] text-fg-muted uppercase">
                {item}
              </span>
              <span className="text-fg-disabled text-xs">·</span>
            </span>
          ))}
        </div>
      </motion.div>
    </section>
  );
}

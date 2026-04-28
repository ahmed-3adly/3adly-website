"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { Project } from "@/types";

interface ProjectHeaderProps {
  project: Project;
}

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, ease: "easeOut" as const, delay },
  }),
};

export function ProjectHeader({ project }: ProjectHeaderProps) {
  const showHeroImage = !project.caseStudy && !!project.heroImage;

  return (
    <div className="relative pt-32 pb-16 px-6 overflow-hidden">
      <div className="relative z-10 max-w-4xl mx-auto">
        {/* Tags + year row */}
        <motion.div
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          animate="visible"
          className="flex flex-wrap items-center gap-3 mb-6"
        >
          {project.tags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] tracking-[0.2em] uppercase px-3 py-1 rounded-full border border-border-hairline text-fg-secondary font-mono"
            >
              {tag}
            </span>
          ))}
          <span className="text-[11px] text-fg-muted ml-auto tabular-nums font-mono">
            {project.year}
          </span>
        </motion.div>

        {/* Title */}
        <motion.h1
          custom={0.1}
          variants={FADE_UP}
          initial="hidden"
          animate="visible"
          className="text-[clamp(2.5rem,7vw,5.5rem)] font-black tracking-tighter leading-none text-fg-primary mb-4 font-display"
        >
          {project.title}
        </motion.h1>

        {/* Type */}
        <motion.p
          custom={0.2}
          variants={FADE_UP}
          initial="hidden"
          animate="visible"
          className="text-base font-medium mb-6 text-accent font-mono tracking-wider"
        >
          {project.type}
        </motion.p>

        {/* Lede paragraph */}
        {project.lede && (
          <motion.p
            custom={0.28}
            variants={FADE_UP}
            initial="hidden"
            animate="visible"
            className="text-xl md:text-[22px] leading-[1.5] text-fg-secondary max-w-[60ch] mb-10 font-mono"
          >
            {project.lede}
          </motion.p>
        )}

        {/* Hero image — simple layout only */}
        {showHeroImage && (
          <motion.div
            custom={0.3}
            variants={FADE_UP}
            initial="hidden"
            animate="visible"
            className="relative w-full aspect-[16/9] overflow-hidden border border-border-hairline bg-bg-surface"
          >
            <Image
              src={project.heroImage}
              alt={`${project.title} hero`}
              fill
              className="object-cover"
              sizes="(max-width: 1024px) 100vw, 896px"
              priority
            />
          </motion.div>
        )}

        {!showHeroImage && !project.caseStudy && (
          <motion.div
            custom={0.3}
            variants={FADE_UP}
            initial="hidden"
            animate="visible"
            className="relative w-full aspect-[16/9] overflow-hidden border border-border-hairline bg-bg-surface flex items-center justify-center"
          >
            <span className="text-fg-muted text-sm font-medium font-mono">{project.title}</span>
          </motion.div>
        )}
      </div>
    </div>
  );
}

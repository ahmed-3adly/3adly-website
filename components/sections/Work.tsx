"use client";

import { motion } from "framer-motion";
import { ProjectCard } from "@/components/ui/ProjectCard";
import projectsData from "@/data/projects.json";
import { Project } from "@/types";

const projects = projectsData as Project[];

const FADE_UP = {
  hidden: { opacity: 0, y: 30 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

export function Work() {
  return (
    <section id="work" className="relative py-32 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.p
          custom={0}
          variants={FADE_UP}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-[11px] font-semibold tracking-[0.2em] uppercase text-accent mb-4 font-mono"
        >
          02 — Selected Work
        </motion.p>

        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-16">
          <motion.h2
            custom={0.1}
            variants={FADE_UP}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="text-[clamp(2rem,5vw,3.5rem)] font-black tracking-tight text-fg-primary leading-none font-syne"
          >
            Things I&apos;ve
            <br />
            shipped
          </motion.h2>

          <motion.p
            custom={0.2}
            variants={FADE_UP}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="text-fg-secondary max-w-xs text-sm leading-relaxed font-mono"
          >
            A selection of product design and AI-powered work from the last few years.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((project, index) => (
            <ProjectCard key={project.id} project={project} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}

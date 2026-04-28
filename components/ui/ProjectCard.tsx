"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Project } from "@/types";
import { ArrowUpRight } from "lucide-react";
import Image from "next/image";

interface ProjectCardProps {
  project: Project;
  index: number;
}

export function ProjectCard({ project, index }: ProjectCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
    >
      <Link
        href={`/work/${project.slug}`}
        className="group relative block w-full overflow-hidden rounded-md bg-bg-surface border border-border-hairline transition-colors duration-300 hover:border-border-strong"
      >
        <div className="relative aspect-[4/3] w-full bg-bg-surface overflow-hidden">
          {project.thumbnail ? (
            <Image
              src={project.thumbnail}
              alt={project.title}
              fill
              className="object-cover transition-transform duration-500 group-hover:scale-105"
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          ) : (
            <div className="absolute inset-0 bg-bg-surface-elevated flex items-center justify-center">
              <span className="text-fg-muted font-medium font-mono">{project.title}</span>
            </div>
          )}

          {/* Hover overlay */}
          <div className="absolute inset-0 bg-bg-canvas/85 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center p-6 text-center z-20">
            <p className="text-fg-primary text-sm font-medium leading-relaxed translate-y-4 group-hover:translate-y-0 transition-transform duration-300 font-mono">
              {project.overview.substring(0, 90)}...
            </p>
          </div>
        </div>

        {/* Card footer */}
        <div className="p-6 border-t border-border-hairline relative z-30">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h3 className="text-2xl font-bold text-fg-primary group-hover:text-accent transition-colors font-display">
                {project.title}
              </h3>
              <p className="text-fg-secondary mt-1 text-sm font-mono">{project.type}</p>
            </div>

            <div className="flex items-center space-x-2 shrink-0">
              <span className="text-fg-muted text-sm tabular-nums font-mono">{project.year}</span>
              <div className="p-2 rounded-full border border-border-hairline group-hover:border-accent group-hover:text-accent transition-colors text-fg-secondary">
                <ArrowUpRight size={18} />
              </div>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mt-4">
            {project.tags.map((tag) => (
              <span
                key={tag}
                className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-transparent text-fg-secondary border border-border-hairline font-mono tracking-wider uppercase"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </Link>
    </motion.div>
  );
}

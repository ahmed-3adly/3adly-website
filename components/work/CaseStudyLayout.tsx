"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowLeft, ArrowRight, CheckCircle2 } from "lucide-react";
import { Project } from "@/types";
import { SectionHeader } from "./SectionHeader";
import { ProjectAtGlance } from "./ProjectAtGlance";
import { ProblemSpace } from "./ProblemSpace";
import { HeroStory } from "./HeroStory";
import { DesignSystemGrid } from "./DesignSystemGrid";
import { Reflection } from "./Reflection";

interface CaseStudyLayoutProps {
  project: Project;
  nextProject: Project | null;
}

const FADE_UP = {
  hidden: { opacity: 0, y: 24 },
  visible: (delay: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const, delay },
  }),
};

function BackLink() {
  return (
    <motion.div custom={0} variants={FADE_UP} initial="hidden" animate="visible">
      <Link
        href="/#work"
        className="inline-flex items-center gap-2 text-[11px] tracking-[0.2em] uppercase text-fg-muted hover:text-fg-primary transition-colors duration-200 mb-12 font-mono"
      >
        <ArrowLeft size={14} aria-hidden="true" />
        All work
      </Link>
    </motion.div>
  );
}

function NextProject({ next }: { next: Project }) {
  return (
    <motion.div
      custom={0.25}
      variants={FADE_UP}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-80px" }}
      className="pt-16 mt-16 border-t border-border-hairline"
    >
      <p className="text-[11px] tracking-[0.22em] uppercase text-fg-muted mb-6 font-mono">
        Next project
      </p>
      <Link
        href={`/work/${next.slug}`}
        className="group flex items-center justify-between p-6 border border-border-hairline hover:border-border-strong transition-colors duration-200"
      >
        <div>
          <h3 className="text-2xl font-bold text-fg-primary group-hover:text-accent transition-colors font-display">
            {next.title}
          </h3>
          <p className="text-fg-muted text-sm mt-1 font-mono">{next.type}</p>
        </div>
        <div className="p-3 rounded-full border border-border-hairline group-hover:border-accent transition-colors duration-200">
          <ArrowRight
            size={20}
            className="text-fg-muted group-hover:text-accent transition-colors"
            aria-hidden="true"
          />
        </div>
      </Link>
    </motion.div>
  );
}

function SimpleSection({
  label,
  children,
  delay = 0,
}: {
  label: string;
  children: React.ReactNode;
  delay?: number;
}) {
  return (
    <motion.div
      custom={delay}
      variants={FADE_UP}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-80px" }}
      className="py-12 border-t border-border-hairline"
    >
      <p className="text-[11px] tracking-[0.22em] uppercase text-accent mb-4 font-mono">
        {label}
      </p>
      {children}
    </motion.div>
  );
}

function SimpleLayout({ project }: { project: Project }) {
  return (
    <>
      <SimpleSection label="Overview" delay={0.1}>
        <p className="text-fg-secondary text-[1.0625rem] leading-relaxed max-w-[60ch] font-mono">
          {project.overview}
        </p>
      </SimpleSection>

      <SimpleSection label="Process" delay={0.15}>
        <p className="text-fg-secondary text-[1.0625rem] leading-relaxed max-w-[60ch] font-mono">
          {project.process}
        </p>
      </SimpleSection>

      <SimpleSection label="Solution" delay={0.2}>
        <p className="text-fg-secondary text-[1.0625rem] leading-relaxed max-w-[60ch] mb-8 font-mono">
          {project.solution}
        </p>

        {project.outcomes.length > 0 && (
          <ul className="space-y-3">
            {project.outcomes.map((outcome) => (
              <li key={outcome} className="flex items-start gap-3">
                <CheckCircle2
                  size={18}
                  className="shrink-0 mt-0.5 text-accent"
                  aria-hidden="true"
                />
                <span className="text-fg-secondary text-sm leading-relaxed font-mono">
                  {outcome}
                </span>
              </li>
            ))}
          </ul>
        )}
      </SimpleSection>
    </>
  );
}

function RichLayout({ project }: { project: Project }) {
  const cs = project.caseStudy!;

  return (
    <div className="space-y-24 md:space-y-32">
      <section>
        <SectionHeader number="01" label="At a glance" />
        <ProjectAtGlance data={cs.atGlance} />
      </section>

      <section>
        <SectionHeader number="02" label="The problem space" />
        <ProblemSpace data={cs.problemSpace} />
      </section>

      {cs.heroStories.map((story, i) => (
        <section key={story.number}>
          <SectionHeader
            number={String(i + 3).padStart(2, "0")}
            label={`Hero story · ${story.number} of ${story.total}`}
          />
          <HeroStory story={story} />
        </section>
      ))}

      <section>
        <SectionHeader
          number={String(3 + cs.heroStories.length).padStart(2, "0")}
          label={cs.designSystemLabel ?? "What I built underneath"}
        />
        <DesignSystemGrid items={cs.designSystem} />
      </section>

      <section>
        <SectionHeader
          number={String(4 + cs.heroStories.length).padStart(2, "0")}
          label={cs.reflectionLabel ?? "What I'd do differently"}
        />
        <Reflection items={cs.reflection} />
      </section>

      {project.outcomes.length > 0 && (
        <section>
          <SectionHeader
            number={String(5 + cs.heroStories.length).padStart(2, "0")}
            label="In summary"
          />
          <ul className="space-y-4 max-w-[60ch]">
            {project.outcomes.map((outcome) => (
              <li key={outcome} className="flex items-start gap-4">
                <CheckCircle2
                  size={20}
                  className="shrink-0 mt-0.5 text-accent"
                  aria-hidden="true"
                />
                <span className="text-fg-secondary text-base leading-relaxed font-mono">
                  {outcome}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

export function CaseStudyLayout({ project, nextProject }: CaseStudyLayoutProps) {
  const isRich = !!project.caseStudy;

  return (
    <div className={`mx-auto px-6 pb-32 ${isRich ? "max-w-[1100px]" : "max-w-4xl"}`}>
      <BackLink />
      {isRich ? <RichLayout project={project} /> : <SimpleLayout project={project} />}
      {nextProject && <NextProject next={nextProject} />}
    </div>
  );
}

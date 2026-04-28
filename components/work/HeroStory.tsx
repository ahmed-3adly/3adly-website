"use client";

import { motion } from "framer-motion";
import { CaseStudyHeroStory } from "@/types";
import { PullQuote } from "./PullQuote";
import { CaseStudyImage } from "./CaseStudyImage";

interface HeroStoryProps {
  story: CaseStudyHeroStory;
}

function Block({
  label,
  paragraphs,
}: {
  label: string;
  paragraphs: string[];
}) {
  return (
    <div className="space-y-3">
      <p className="text-[11px] tracking-[0.22em] uppercase text-fg-muted font-mono">
        {label}
      </p>
      {paragraphs.map((p, i) => (
        <p
          key={i}
          className="text-fg-secondary text-base md:text-[1.0625rem] leading-[1.7] font-mono"
        >
          {p}
        </p>
      ))}
    </div>
  );
}

export function HeroStory({ story }: HeroStoryProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      {/* Story header */}
      <div className="flex items-baseline gap-4 mb-2">
        <span className="text-[11px] tracking-[0.25em] uppercase text-accent font-mono">
          {story.kicker} {story.number} / {story.total}
        </span>
      </div>

      <h3 className="text-[clamp(2rem,4.5vw,3rem)] leading-[1.05] tracking-[-0.02em] text-fg-primary font-display font-bold">
        {story.title}
      </h3>

      <div className="space-y-10 max-w-[60ch]">
        <Block label="The challenge" paragraphs={story.challenge} />

        {story.insight && story.insight.length > 0 && (
          <Block label="The insight" paragraphs={story.insight} />
        )}

        {story.pullQuote && <PullQuote quote={story.pullQuote} />}

        {story.approach.length > 0 && (
          <div className="space-y-4">
            <p className="text-[11px] tracking-[0.22em] uppercase text-fg-muted font-mono">
              {story.approachLabel ?? "My approach"}
            </p>
            <ul className="space-y-3.5">
              {story.approach.map((item, i) => (
                <li
                  key={i}
                  className="flex gap-4 text-fg-secondary text-base md:text-[1.0625rem] leading-[1.7] font-mono"
                >
                  <span
                    className="text-[11px] text-accent tabular-nums pt-1.5 shrink-0 font-mono"
                    aria-hidden="true"
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {story.tradeoff && story.tradeoff.length > 0 && (
          <Block
            label={story.tradeoffLabel ?? "The trade-off"}
            paragraphs={story.tradeoff}
          />
        )}

        <Block
          label={story.outcomeLabel ?? "Outcome"}
          paragraphs={story.outcome}
        />
      </div>

      <CaseStudyImage image={story.image} />
    </motion.article>
  );
}

"use client";

import { useEffect, useState } from "react";

export interface TOCSection {
  id: string;
  label: string;
}

interface SectionTOCProps {
  sections: TOCSection[];
}

export function SectionTOC({ sections }: SectionTOCProps) {
  const [active, setActive] = useState<string>(sections[0]?.id ?? "");

  useEffect(() => {
    if (sections.length === 0) return;

    const observers: IntersectionObserver[] = [];

    sections.forEach((section) => {
      const el = document.getElementById(section.id);
      if (!el) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              setActive(section.id);
            }
          });
        },
        { rootMargin: "-40% 0px -40% 0px", threshold: 0 },
      );

      observer.observe(el);
      observers.push(observer);
    });

    return () => observers.forEach((o) => o.disconnect());
  }, [sections]);

  if (sections.length === 0) return null;

  return (
    <nav
      aria-label="Case study sections"
      className="hidden lg:block fixed right-8 top-1/2 -translate-y-1/2 z-30"
    >
      <ul className="space-y-3">
        {sections.map((section) => {
          const isActive = active === section.id;
          return (
            <li key={section.id}>
              <a
                href={`#${section.id}`}
                className="group flex items-center gap-3 text-[10px] tracking-[0.25em] uppercase font-mono"
              >
                <span
                  aria-hidden="true"
                  className={`h-px transition-all duration-300 ${
                    isActive
                      ? "w-10 bg-accent"
                      : "w-4 bg-fg-muted group-hover:w-6 group-hover:bg-fg-secondary"
                  }`}
                />
                <span
                  className={`transition-colors duration-200 ${
                    isActive
                      ? "text-accent"
                      : "text-fg-muted group-hover:text-fg-secondary"
                  }`}
                >
                  {section.label}
                </span>
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const sections = [
  { id: "hero", label: "Hero" },
  { id: "work", label: "Selected Work" },
  { id: "about", label: "About" },
  { id: "skills", label: "Skills & Tools" },
  { id: "experience", label: "Experience" },
  { id: "certifications", label: "Certifications" },
  { id: "contact", label: "Contact" },
];

export function DotNav() {
  const [activeSection, setActiveSection] = useState("hero");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { threshold: 0.3 } // 30% of the section must be visible to count
    );

    sections.forEach((section) => {
      const el = document.getElementById(section.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="fixed right-6 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col space-y-4">
      {sections.map((section) => (
        <button
          key={section.id}
          onClick={() => scrollTo(section.id)}
          className="group relative flex items-center justify-center p-2"
          aria-label={`Scroll to ${section.label}`}
        >
          {/* Label tooltip on hover */}
          <span className="absolute right-8 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap bg-bg-surface px-2 py-1 text-xs text-fg-secondary pointer-events-none border border-border-hairline font-mono tracking-wider">
            {section.label}
          </span>

          <div
            className={`w-3 h-3 rounded-full transition-all duration-300 border ${
              activeSection === section.id
                ? "bg-accent border-accent scale-125"
                : "bg-transparent border-border-strong hover:border-fg-muted"
            }`}
          />
        </button>
      ))}
    </div>
  );
}

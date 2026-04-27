"use client";

import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export function FloatingNav() {
  const pathname = usePathname();
  const router = useRouter();
  const isCaseStudy = pathname?.startsWith("/work/") ?? false;
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // On case study pages, show immediately (no hero to scroll past).
    if (isCaseStudy) {
      setIsVisible(true);
      return;
    }

    const handleScroll = () => {
      setIsVisible(window.scrollY > 200);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isCaseStudy]);

  const goToSection = (id: string) => {
    if (pathname === "/") {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    } else {
      router.push(`/#${id}`);
    }
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.nav
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -100, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed top-6 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-full bg-bg-surface border border-border-hairline flex items-center space-x-6 text-sm font-medium font-mono text-fg-secondary"
        >
          {isCaseStudy && (
            <>
              <Link
                href="/#work"
                className="flex items-center gap-2 hover:text-accent transition-colors"
              >
                <ArrowLeft size={14} aria-hidden="true" />
                <span>All work</span>
              </Link>
              <div className="w-px h-4 bg-border-hairline" />
            </>
          )}

          <button onClick={() => goToSection("work")} className="hover:text-accent transition-colors">
            Work
          </button>
          <button onClick={() => goToSection("about")} className="hover:text-accent transition-colors">
            About
          </button>
          <button onClick={() => goToSection("contact")} className="hover:text-accent transition-colors">
            Contact
          </button>

          <div className="w-px h-4 bg-border-hairline" />

          <button
            onClick={() => goToSection("contact")}
            className="flex items-center space-x-2 px-3 py-1.5 rounded-full transition-colors border border-border-hairline hover:border-border-strong"
          >
            <span className="w-2 h-2 rounded-full bg-status-success animate-pulse" aria-hidden="true" />
            <span>Available for work</span>
          </button>
        </motion.nav>
      )}
    </AnimatePresence>
  );
}

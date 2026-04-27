"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { CaseStudyImage as CaseStudyImageType } from "@/types";

interface CaseStudyImageProps {
  image: CaseStudyImageType;
}

const RATIO_TO_PADDING: Record<string, string> = {
  "16/9": "56.25%",
  "16/10": "62.5%",
  "4/3": "75%",
  "3/2": "66.66%",
  "1/1": "100%",
};

export function CaseStudyImage({ image }: CaseStudyImageProps) {
  const ratio = image.ratio ?? "16/10";
  const paddingTop = RATIO_TO_PADDING[ratio] ?? "62.5%";

  return (
    <motion.figure
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6 }}
      className="my-12"
    >
      <div
        className="relative w-full overflow-hidden border border-border-hairline bg-bg-surface"
        style={{ paddingTop }}
      >
        {image.src ? (
          <Image
            src={image.src}
            alt={image.alt}
            fill
            className="object-cover"
            sizes="(max-width: 1024px) 100vw, 1100px"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-bg-surface">
            <span className="text-[11px] tracking-[0.2em] uppercase text-fg-muted font-mono">
              Image placeholder · {image.alt}
            </span>
          </div>
        )}
      </div>
      <figcaption className="mt-4 text-[11px] tracking-[0.18em] uppercase text-fg-muted font-mono">
        {image.caption}
      </figcaption>
    </motion.figure>
  );
}

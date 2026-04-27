import { Hero } from "@/components/sections/Hero";
import { Work } from "@/components/sections/Work";
import { About } from "@/components/sections/About";
import { Skills } from "@/components/sections/Skills";
import { Experience } from "@/components/sections/Experience";
import { Contact } from "@/components/sections/Contact";
import { FloatingNav } from "@/components/ui/FloatingNav";
import { DotNav } from "@/components/ui/DotNav";

export default function Home() {
  return (
    <main className="min-h-screen bg-bg-canvas">
      <FloatingNav />
      <DotNav />
      <Hero />
      <Work />
      <About />
      <Skills />
      <Experience />
      <Contact />
    </main>
  );
}

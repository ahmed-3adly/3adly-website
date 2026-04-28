import { notFound } from "next/navigation";
import projectsData from "@/data/projects.json";
import { Project } from "@/types";
import { ProjectHeader } from "@/components/work/ProjectHeader";
import { CaseStudyLayout } from "@/components/work/CaseStudyLayout";
import { FloatingNav } from "@/components/ui/FloatingNav";

const projects = projectsData as Project[];

export function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const project = projects.find((p) => p.slug === slug);
  if (!project) return {};
  return {
    title: `${project.title} — Ahmed Adly`,
    description: project.overview,
  };
}

export default async function CaseStudyPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const index = projects.findIndex((p) => p.slug === slug);

  if (index === -1) notFound();

  const project = projects[index];
  const nextProject = projects[(index + 1) % projects.length] ?? null;

  return (
    <main id="main-content" tabIndex={-1} className="min-h-screen bg-bg-canvas focus:outline-none">
      <FloatingNav />
      <ProjectHeader project={project} />
      <CaseStudyLayout project={project} nextProject={nextProject} />
    </main>
  );
}

export interface Project {
  id: string;
  slug: string;
  title: string;
  originalTitle?: string;
  type: string;
  tags: string[];
  year: string;
  heroImage: string;
  thumbnail: string;
  overview: string;
  process: string;
  solution: string;
  outcomes: string[];
  lede?: string;
  caseStudy?: CaseStudyContent;
}

export interface Experience {
  id: string;
  role: string;
  company: string;
  yearRange: string;
  description: string;
}

export interface CaseStudyAtGlance {
  role: string;
  scope: string[];
  timeline: string;
  team: string;
  context?: string;
  status: string;
}

export interface CaseStudyProblemSpace {
  narrative: string[];
  sidebarLabel: string;
  sidebar: string[];
}

export interface CaseStudyImage {
  src?: string;
  alt: string;
  caption: string;
  ratio?: string;
}

export interface CaseStudyHeroStory {
  number: string;
  total: string;
  kicker: string;
  title: string;
  challenge: string[];
  insight?: string[];
  pullQuote?: string;
  approachLabel?: string;
  approach: string[];
  tradeoffLabel?: string;
  tradeoff?: string[];
  outcomeLabel?: string;
  outcome: string[];
  image: CaseStudyImage;
}

export interface CaseStudyObservation {
  title: string;
  description: string;
}

export interface CaseStudyReflection {
  title: string;
  body: string;
}

export interface CaseStudyContent {
  oneLine: string;
  atGlance: CaseStudyAtGlance;
  problemSpace: CaseStudyProblemSpace;
  heroStories: CaseStudyHeroStory[];
  designSystemLabel?: string;
  designSystem: CaseStudyObservation[];
  reflectionLabel?: string;
  reflection: CaseStudyReflection[];
}

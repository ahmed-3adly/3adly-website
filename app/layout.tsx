import type { Metadata } from "next";
import { Fragment_Mono, Licorice } from "next/font/google";
import "./globals.css";

const fragmentMono = Fragment_Mono({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-mono-stack",
  display: "swap",
});

const licorice = Licorice({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-script-stack",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Ahmed Adly | Product Designer & AI Builder",
  description:
    "Product Designer who builds with AI. Turning complex ideas into shipped products.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`dark ${fragmentMono.variable} ${licorice.variable}`}>
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link
          rel="stylesheet"
          href="https://api.fontshare.com/v2/css?f[]=general-sans@500,600,700,800&display=swap"
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}

import type { Metadata } from "next";
import "../styles/globals.css";
import Providers from "./providers";
import TopLeftControls from "@/components/top-left-controls";

export const metadata: Metadata = {
  title: "ResuMAX - Your AI Resume Assistant",
  description: "Create and optimize your resume with AI-powered assistance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <TopLeftControls />
          {children}
        </Providers>
      </body>
    </html>
  );
}

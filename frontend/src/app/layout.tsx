import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AuthModeBadge } from "@/components/AuthModeBadge";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

const authMode = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true" ? "mock" : "firebase";
console.log(`[auth] mode detected (server render): ${authMode}`);

export const metadata: Metadata = {
  title: "resuMAX | AI Resume Optimizer",
  description: "AI-powered resume optimizer to tailor your applications.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-black text-white antialiased`}>
        {children}
        <AuthModeBadge />
      </body>
    </html>
  );
}

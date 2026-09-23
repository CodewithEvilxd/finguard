import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinGuard AI — Explainable Fraud & Anomaly Intelligence",
  description:
    "Enterprise financial risk platform combining XGBoost fraud classification, Isolation Forest anomaly scoring, and grounded AI investigation.",
  keywords: ["financial intelligence", "fraud detection", "explainable AI", "anomaly detection", "fintech compliance"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-canvas text-ink antialiased font-sans">
        <ClerkProvider>
          {children}
        </ClerkProvider>
      </body>
    </html>
  );
}

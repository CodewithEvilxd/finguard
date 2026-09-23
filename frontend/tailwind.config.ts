import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        canvas: {
          DEFAULT: "#fbfaf8",
          subtle: "#f4f2ee",
          elevated: "#ffffff",
        },
        ink: {
          DEFAULT: "#0f172a",
          muted: "#475569",
          faint: "#94a3b8",
        },
        border: {
          DEFAULT: "#e2e8f0",
          subtle: "#eedec8",
        },
        accent: {
          DEFAULT: "#ea580c",
          hover: "#c2410c",
          light: "#fff7ed",
          border: "#fed7aa",
        },
        navy: {
          DEFAULT: "#0f172a",
          dark: "#0a0f1d",
          light: "#1e293b",
        },
        status: {
          low: "#166534",
          lowBg: "#f0fdf4",
          lowBorder: "#bbf7d0",
          medium: "#854d0e",
          mediumBg: "#fefce8",
          mediumBorder: "#fef08a",
          high: "#c2410c",
          highBg: "#fff7ed",
          highBorder: "#fed7aa",
          critical: "#991b1b",
          criticalBg: "#fef2f2",
          criticalBorder: "#fecaca",
        },
      },
      fontFamily: {
        serif: ["Merriweather", "Georgia", "serif"],
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;

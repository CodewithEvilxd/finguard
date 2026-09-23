# Frontend and UI Specification

## Product aesthetic
FinGuard AI must look like a premium editorial fintech product, not a generic AI dashboard and not a cyberpunk concept poster.

## Visual language
- warm white/off-white background
- deep navy and charcoal typography
- warm orange as the main accent
- restrained muted blue/gray secondary accents
- thin rules and low-contrast borders
- large editorial headings
- generous whitespace
- simple flat icons
- subtle sketch-style annotations only where useful
- realistic product screenshots/UI as supporting visuals

Avoid: neon gradients, excessive glassmorphism, generic 3D AI brains, glowing holograms, random floating panels, excessive rounded cards, stock photos, and dense dashboard walls.

## Typography roles
1. Display: distinctive editorial heading face.
2. Sans: all product UI and body copy.
3. Optional handwritten accent: annotations only, never critical information.

## Required public routes
`/` — product landing/interface
`/login` — authentication
`/demo` — controlled demo

## Required protected/product routes
`/dashboard`
`/transactions`
`/alerts`
`/investigations`
`/accounts`
`/vendors`
`/analytics`
`/reports`
`/settings`

## Landing page
The first page opened must be an intentional product interface. It should answer:
- What is FinGuard AI?
- What problem does it solve?
- How does it work?
- Why is explainability important?
- How can I see the product?

Use a concise hero, real product preview, four capabilities (Detect, Explain, Investigate, Decide), short workflow, trust statement, and clear demo/sign-in CTA.

## Dashboard
Overview should contain:
- transaction volume
- active alerts
- high-risk count
- critical count
- resolution status
- risk trend
- recent alert queue
- investigation activity

## Investigation workspace
Include transaction facts, score, explanation factors, timeline, related entities, similar activity, AI assistant, analyst decision controls, and audit history.

## UX states
Every data screen needs loading, empty, error, permission-denied, and success states. Every actionable control needs keyboard focus and accessible labels.

## Accessibility
Target WCAG 2.2 AA practices: keyboard navigation, semantic structure, focus visibility, sufficient contrast, form labels, accessible charts/data alternatives, and reduced-motion support.

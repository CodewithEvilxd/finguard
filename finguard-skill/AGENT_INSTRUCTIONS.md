# Antigravity / Coding Agent Instructions

Read `skill/SKILL.md` before changing the repository. Then read the specific supporting files required by the task.

## Execution protocol
1. Inspect the existing repository before changing architecture.
2. Do not rewrite working modules without a measurable reason.
3. State assumptions inside the relevant design document rather than silently inventing them.
4. Implement one vertical slice at a time and keep the app runnable after each slice.
5. Prefer small, reviewable commits.
6. Run lint, typecheck, unit tests, integration tests, and a production build for affected services.
7. Verify critical user flows manually or with browser tests.
8. Update `skill/tracking/TRACKING.md` after every completed or blocked task.
9. If implementation differs from the plan, update the plan and architecture decision record.
10. Never mark a task complete because code merely exists; mark it complete only after verification.

## Product-first rule
The root URL `/` must render a polished product interface/landing page first. Do not redirect first-time visitors directly into a raw dashboard.

Required primary routes:
- `/` product interface / landing page
- `/login` authentication
- `/demo` controlled demo mode
- `/dashboard` operational overview
- `/transactions`
- `/alerts`
- `/investigations`
- `/accounts`
- `/vendors`
- `/analytics`
- `/reports`
- `/settings`

## UI rules
- No emoji.
- No placeholder lorem ipsum.
- No fake testimonials.
- No generic dashboard template look.
- No inaccessible color-only statuses.
- Use semantic HTML and keyboard navigation.
- Provide loading, empty, error, and success states.
- Responsive from 1280px desktop down to tablet; mobile can be a focused read-only experience for analytics if full analyst workflow is not appropriate.

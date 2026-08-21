# design-rules.md — anti-"vibecoded" checklist. Every UI deliverable must pass. (30 banned items + project positives.)

## Banned (the 30)
1. Harsh gradients
2. Lucide icons (default icon set) — use custom/SF Symbols-style or curated set
3. Purple gradient
4. Rainbow colors
5. Drop shadows (heavy/default)
6. "3 feature cards" row
7. Emoji as UI
8. Liquid glass
9. Em dashes in copy
10. Inter / Geist / Space Grotesk fonts
11. Colored left stripe on cards/callouts
12. Fake testimonials
13. Bento grids
14. Terminal window mockups
15. "It's not X, it's Y" copy
16. Checkmark bullets
17. 3 pricing tiers
18. No real product demos (show real screens/ink)
19. Soft/default corner radius everywhere
20. Purple + black palette
21. Missing skeleton loaders (must have them)
22. Radial orbs / blurred blobs
23. Dot grids background
24. Sparkle icons
25. Animated arrows
26. Missing Terms of Service
27. Missing Privacy Policy
28. Gratuitous hover animations
29. Neon colors
30. Basic pastel colors

Items 3–8 confirmed by user 2026-08-21.

## Project positives (fill per project)
- One palette in tokens, works light+dark.
- Distinctive type pair (not the banned trio); strong size contrast.
- Real content only (real data, real screenshots).
- Motion purposeful (state change, navigation); no idle animation; reduced-motion respected.
- Skeletons + empty + error states for every list.
- Illustrations sparingly, recolored to palette.
- Legal: ToS + Privacy before any public build.

## Process
1. Generate reference image per screen (image-to-code-skill) → 2. checklist pass → 3. implement → 4. Playwright screenshot → 5. checklist pass again.

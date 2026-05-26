# Design

## Theme
A dim, focused lecture hall environment. The visual weight is purely on the chaotic orbits. 

## Color Strategy
"Committed" dark mode using OKLCH. No pure blacks or whites; all neutrals are tinted slightly violet/indigo to evoke a sophisticated academic night-time feel.

Base Background: `oklch(12% 0.025 285)`
Surface Layer: `oklch(18% 0.035 285)`
Text (Primary): `oklch(95% 0.015 285)`
Text (Muted): `oklch(75% 0.03 285)`
Accent (Math highlight): `oklch(80% 0.15 80)` (A warm gold)
Accent (Divergence highlight): `oklch(75% 0.18 20)` (A stark orange-red)
Accent (Stable highlight): `oklch(85% 0.14 200)` (A sharp cyan)

## Typography
- **Headings/Display**: "Spectral" (Google Fonts) - A gorgeous, rigorous academic serif that feels like a modern mathematical manuscript.
- **Body/UI**: "Public Sans" (Google Fonts) - Clean, highly legible sans-serif for UI labels and body text, avoiding the "Inter" monoculture.
- **Monospace/Math**: "Fira Code" (Google Fonts) - Distinctive coding font for mathematical vectors and equations.

Fluid scale with $\ge 1.25$ ratio between steps. 
Body line height: `1.6`

## Motion
No generic spring or elastic animations.
All transitions use `ease-out-expo` (`cubic-bezier(0.19, 1, 0.22, 1)`) for a decisive, physical feel.
Avoid animating layout properties.

## Layout
- Asymmetric compositions to break away from the "centered stack" template.
- Fluid padding (`clamp()`) to ensure rhythmic spacing.
- No side-stripe borders, no nested cards, no generic metric grids.

# Thai & bilingual typography

Thai is a designed-for language here, not a fallback. Read this when the deck is Thai, or
mixes Thai and English (TH/EN). The goal: Thai that looks *chosen*, sits correctly next to
Latin, and never renders as tofu (□□□) because a font lacked Thai glyphs.

## The core problem

Most distinctive Latin display fonts (Fraunces, Cormorant, Clash Display, Archivo Black)
have **no Thai glyphs**. If a Thai word lands in such a heading, the browser falls back to a
random system Thai face — a metric and mood mismatch. The fix is always a **stacked
font-family**: the Latin face first, a chosen Thai companion second.

```css
--f-display: "Fraunces", "Noto Serif Thai", Georgia, serif;       /* headings */
--f-body:    "Hanken Grotesk", "Noto Sans Thai", system-ui, sans-serif; /* body */
--f-mono:    "Space Mono", "Noto Sans Thai", monospace;           /* labels */
```

Latin glyphs render in the Latin face; Thai glyphs fall through to the Thai companion. Pick
the companion deliberately so the two faces share weight and temperament.

## Thai fonts on Google Fonts (all free, CDN)

| Thai face | Character | Pair it with (Latin mood) |
| --- | --- | --- |
| `Noto Serif Thai` | Calm modern serif, loopless | Cormorant, Fraunces, Source Serif — literary / scholarly |
| `Noto Sans Thai` | Neutral humanist sans, loopless | DM Sans, Hanken Grotesk, Inter-alternatives — clean body |
| `IBM Plex Sans Thai` | Technical, even, loopless | IBM Plex / Space Grotesk — product / tech |
| `Sarabun` | Official Thai government face, friendly | Work Sans, Mukta — documents, reports |
| `Anuphan` | Modern geometric, loopless | Archivo, Manrope — confident modern |
| `Bai Jamjuree` | Squarish technical | JetBrains Mono, Chakra Petch — terminal / engineering |
| `Kanit` | Bold loopless display, strong | Archivo Black, Anton — posters, punchy |
| `Mitr` | Rounded geometric, warm | Poppins, Quicksand — friendly / approachable |
| `Chakra Petch` | Angular sci-fi | Orbitron, Rajdhani — futuristic |
| `Noto Looped Thai` / `Sarabun` (looped) | Traditional looped หัวกลม | when the brand wants classic Thai warmth |

**Loop vs loopless (หัวกลม / หัวตัด).** Looped Thai reads as traditional, official, warm;
loopless reads as modern, neutral, tech. Match the loop choice to the deck's mood — a
modern startup deck wants loopless; a heritage or government deck wants looped.

## Mixed-script rules

- **Pangu spacing (วรรคคั่น).** Put a thin space between Thai and adjacent Latin or numerals:
  write `ใช้ Claude` not `ใช้Claude`, `2026 ปี` not `2026ปี`. It reads as careful Thai
  typography.
- **No letter-spacing on Thai.** Negative tracking that flatters Latin display
  (`letter-spacing: -0.02em`) overlaps Thai glyphs and their marks. Scope tracking to Latin,
  or set `letter-spacing: 0` on Thai runs (`:lang(th)`).
- **More line-height.** Thai stacks vowels/tones above and below the baseline. Body wants
  `line-height: 1.55–1.75` (vs ~1.4 for Latin); display wants looser leading than the Latin
  default so marks don't collide with the line above.
- **No uppercase on Thai.** Thai has no letter case — `text-transform: uppercase` does
  nothing to Thai and signals a Latin-only rule misapplied. Keep kickers/labels lowercase or
  use a mono Latin label.
- **Don't italicize Thai.** Thai has no true italic; a synthetic slant looks broken. Use
  weight or color for emphasis instead.
- **Always include a Thai face in every stack** that can hold Thai — headings, body, labels.
  A missing Thai fallback is the tofu bug.

## Bilingual layout patterns

| Pattern | When | How |
| --- | --- | --- |
| **TH primary, EN secondary** | Thai audience, English as gloss | Thai headline large; English one step smaller in a muted tone beneath |
| **EN primary, TH secondary** | International deck made Thai-aware | mirror of the above |
| **Stacked bilingual cover** | brand lines, taglines | both languages, same weight, a hairline or dot between — e.g. `Open your game · เปิดเกมของคุณ` |
| **Parallel body** | teaching / contracts | two columns or two short paragraphs, TH and EN side by side |

Keep one language dominant per slide for rhythm; the second supports, it doesn't compete.
Load the Thai font(s) in the same `<link>` as the Latin fonts so nothing flashes.

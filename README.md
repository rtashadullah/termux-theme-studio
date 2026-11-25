# Termux Theme Studio

Python diye Termux theme banano / apply kora tool — **10 ta theme, prottek tar nijer font soho.**

Termux theme = 2 ta jinis:
1. **Color** — `~/.termux/colors.properties` (background, foreground, cursor, `color0`–`color15`)
2. **Font** — `~/.termux/font.ttf` (ekta .ttf file)

Ei tool 2 tai banay / bosay. Kono Android app code change lage na, kono extra library lage na (stdlib only).

## Themes (10 ta)

| # | Theme | Background | Font | Vibe |
|---|---|---|---|---|
| 1 | `neon-modern` ⭐ | `#0F172A` deep navy | JetBrains Mono | Purple `#A78BFA` + cyan `#22D3EE` neon — Design #3 |
| 2 | `minimal-dark` | `#1A1A1A` charcoal | Fira Code | Clean dark, soft white |
| 3 | `hacker-green` | `#000000` pure black | Hack | Neon green `#00FF41`, classic hacker |
| 4 | `dracula` | `#282A36` dark purple | Cascadia Code ⚠️ | Pink `#FF79C6` + green `#50FA7B` |
| 5 | `ocean-blue` | `#0A192F` deep sea | Source Code Pro | Aqua `#64FFDA`, calm professional |
| 6 | `sunset` | `#2D1B1E` dark brown | Ubuntu Mono ⚠️ | Orange `#FF6B35` + amber, warm dusk |
| 7 | `forest` | `#0D1B0E` deep green | Noto Sans Mono | Lime `#7CFC00`, night forest |
| 8 | `lavender` | `#1E1B2E` purple night | Victor Mono | Pastel purple, dreamy |
| 9 | `sakura` | `#2B1A22` dark plum | Inconsolata | Cherry pink `#FF8FAB`, gentle |
| 10 | `ios-modern` 🍎 | `#F2F2F7` iOS light grey | SF Mono* | iOS-style clean light theme, blue `#007AFF` |

\* **SF Mono Apple-er font, free download nei** — tai `ios-modern`-e SF Mono style-er closest free stand-in hishebe JetBrains Mono .ttf use kora hoy.

⚠️ **Dracula (Cascadia Code) ar Sunset (Ubuntu Mono)-er font URL 2026-11-25-e curl check-e 404 diyechilo** — download korar age link check koro; na hole repo release / font site theke .ttf namiye `~/.termux/font.ttf`-e bosau. Baki 8 tar URL verified (HTTP 200).

## Termux-e chalao (phone-e)

```bash
pkg install python git curl -y
git clone https://github.com/rtashadullah/termux-theme-studio
cd termux-theme-studio

python termux_theme.py list          # 10 ta theme dekho
python termux_theme.py fonts         # font + download URL dekho
python termux_theme.py preview dracula
python termux_theme.py apply neon-modern
```

Ek command-e:

```bash
bash install.sh neon-modern
```

## Font change koro

Color apply korlei font bodlay na — font alada kore bosate hoy:

```bash
# Ek command-e (theme-er font download + install):
python termux_theme.py install-font neon-modern

# Ba nije haate:
curl -L "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf" -o ~/.termux/font.ttf
termux-reload-settings
```

Font bodle gele Termux restart korte hote pare. `apply` korle font install-er instruction auto dekhay.

## Demo (terminal preview)

Prottek theme-er terminal preview dekhte:

```bash
python termux_theme.py preview neon-modern
python termux_theme.py preview ios-modern
python termux_theme.py preview dracula
```

Preview-e 16 ta color-er swatch + sample terminal line (`$ whoami`) dekhay — iPhone UI na, asol Termux terminal-er look.

## Nijer theme banau

```bash
python termux_theme.py create --name amar-theme --bg "#0F172A" --fg "#E2E8F0" --accent "#22D3EE"
cp themes/amar-theme.properties ~/.termux/colors.properties
termux-reload-settings
```

## Files

- `termux_theme.py` — main tool, kono extra library lage na (stdlib only)
- `themes/*.properties` — ready-made Termux color files (10 ta)
- `install.sh` — one-command installer

## Kivabe kaj kore

Termux `~/.termux/colors.properties` pore: `background`, `foreground`, `cursor`, `color0`–`color15`. Ei tool sei file-ta banay. Font-er jonno `~/.termux/font.ttf` file-ta bosay. Android UI (button, menu) bodlay na — terminal-er color + font, etai Termux theme.

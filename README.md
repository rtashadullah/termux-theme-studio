# Termux Theme Studio

Python diye Termux theme banano / apply kora tool.

**3 number design — Neon Modern — 100% possible.** Termux theme asole ekta `colors.properties` file, Python diye seta generate kore `~/.termux/`-e bosalei hoy. Kono Android app code change lage na.

## Themes

| Theme | Vibe |
|---|---|
| `neon-modern` ⭐ | Deep navy `#0F172A` + purple `#A78BFA` + cyan `#22D3EE` — Design #3 |
| `minimal-dark` | Clean charcoal dark, soft white |
| `hacker-green` | Pure black + neon green `#00FF41` |

## Termux-e chalao (phone-e)

```bash
pkg install python git -y
git clone https://github.com/rtashadullah/termux-theme-studio
cd termux-theme-studio

python termux_theme.py list
python termux_theme.py preview neon-modern
python termux_theme.py apply neon-modern
```

Ek command-e:

```bash
bash install.sh neon-modern
```

Apply korlei theme bodle jabe — `termux-reload-settings` auto chalano hoy.

## Nijer theme banau

```bash
python termux_theme.py create --name amar-theme --bg "#0F172A" --fg "#E2E8F0" --accent "#22D3EE"
cp themes/amar-theme.properties ~/.termux/colors.properties
termux-reload-settings
```

## Files

- `termux_theme.py` — main tool, kono extra library lage na (stdlib only)
- `themes/*.properties` — ready-made Termux color files
- `install.sh` — one-command installer

## Kivabe kaj kore

Termux `~/.termux/colors.properties` pore: `background`, `foreground`, `cursor`, `color0`–`color15`. Ei tool sei file-ta banay. Android UI (button, menu) bodlay na — terminal-er color, etai Termux theme.

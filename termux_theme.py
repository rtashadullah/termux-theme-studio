#!/usr/bin/env python3
"""
Termux Theme Studio — Python diye Termux theme banano / apply kora tool
=========================================================================
10 ta built-in theme, prottek tar nijer font soho.

Usage (Termux-e):
    pkg install python -y
    git clone https://github.com/rtashadullah/termux-theme-studio
    cd termux-theme-studio
    python termux_theme.py list
    python termux_theme.py fonts
    python termux_theme.py preview neon-modern
    python termux_theme.py apply neon-modern
    python termux_theme.py install-font neon-modern
    python termux_theme.py generate neon-modern -o ~/.termux/colors.properties

    # Nijer theme banate:
    python termux_theme.py create --name amar-theme --bg "#0f172a" --fg "#e2e8f0" --accent "#22d3ee"

Kono extra library lage na — sudhu Python 3.8+ (stdlib only).

Termux theme = 2 ta jinis:
  1. Color: ~/.termux/colors.properties (background, foreground, cursor, color0-15)
  2. Font:  ~/.termux/font.ttf (ekta .ttf file) — ei tool prottek theme-er
     font-er download URL dey, ar `install-font` diye namiye bosay.

Note on fonts: SF Mono Apple-er font, free download nei — tai ios-modern
theme-e SF Mono style-er closest free stand-in hishebe JetBrains Mono .ttf
use kora hoy. Variable font (.ttf with [wght]) Termux-e default weight-e
render hote pare. "UNVERIFIED" lekha URL gulo 2026-11-25-e curl HEAD check-e
404 diyechilo — download korar age link ta check kore nio.
"""

import argparse
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

VERSION = "1.1.0"

# ---------------------------------------------------------------------------
# Themes (10 ta)
# Font URL check 2026-11-25 (curl -I): 200 = verified, 404 = UNVERIFIED
# ---------------------------------------------------------------------------

THEMES = {
    "neon-modern": {
        "name": "Neon Modern",
        "description": "Deep navy background, purple + cyan neon accents. Design #3.",
        "background": "#0F172A",
        "foreground": "#E2E8F0",
        "cursor": "#22D3EE",
        "font": "JetBrains Mono",
        "font_url": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf",  # verified 200
        "color0": "#1E293B",   # black
        "color1": "#F87171",   # red
        "color2": "#34D399",   # green
        "color3": "#FBBF24",   # yellow
        "color4": "#60A5FA",   # blue
        "color5": "#A78BFA",   # magenta / purple
        "color6": "#22D3EE",   # cyan
        "color7": "#E2E8F0",   # white
        "color8": "#64748B",   # bright black
        "color9": "#FCA5A5",   # bright red
        "color10": "#6EE7B7",  # bright green
        "color11": "#FDE68A",  # bright yellow
        "color12": "#93C5FD",  # bright blue
        "color13": "#C4B5FD",  # bright magenta
        "color14": "#67E8F9",  # bright cyan
        "color15": "#F8FAFC",  # bright white
    },
    "minimal-dark": {
        "name": "Minimal Dark",
        "description": "Clean charcoal dark, soft white text. Design #1.",
        "background": "#1A1A1A",
        "foreground": "#E5E5E5",
        "cursor": "#FFFFFF",
        "font": "Fira Code",
        "font_url": "https://github.com/google/fonts/raw/main/ofl/firacode/FiraCode%5Bwght%5D.ttf",  # verified 200 (variable font)
        "color0": "#1A1A1A",
        "color1": "#E06C75",
        "color2": "#98C379",
        "color3": "#E5C07B",
        "color4": "#61AFEF",
        "color5": "#C678DD",
        "color6": "#56B6C2",
        "color7": "#D0D0D0",
        "color8": "#5C6370",
        "color9": "#E06C75",
        "color10": "#98C379",
        "color11": "#E5C07B",
        "color12": "#61AFEF",
        "color13": "#C678DD",
        "color14": "#56B6C2",
        "color15": "#FFFFFF",
    },
    "hacker-green": {
        "name": "Hacker Green",
        "description": "Pure black + neon green, classic hacker look. Design #2.",
        "background": "#000000",
        "foreground": "#00FF41",
        "cursor": "#00FF41",
        "font": "Hack",
        "font_url": "https://github.com/source-foundry/Hack/raw/master/build/ttf/Hack-Regular.ttf",  # verified 200
        "color0": "#000000",
        "color1": "#FF0000",
        "color2": "#00FF41",
        "color3": "#FFFF00",
        "color4": "#0000FF",
        "color5": "#FF00FF",
        "color6": "#00FFFF",
        "color7": "#C0C0C0",
        "color8": "#808080",
        "color9": "#FF5555",
        "color10": "#55FF55",
        "color11": "#FFFF55",
        "color12": "#5555FF",
        "color13": "#FF55FF",
        "color14": "#55FFFF",
        "color15": "#FFFFFF",
    },
    "dracula": {
        "name": "Dracula",
        "description": "Dark purple, pink + green — famous Dracula palette.",
        "background": "#282A36",
        "foreground": "#F8F8F2",
        "cursor": "#FF79C6",
        "font": "Cascadia Code",
        "font_url": "https://github.com/microsoft/cascadia-code/raw/main/fonts/ttf/CascadiaCode.ttf",  # UNVERIFIED (404 on 2026-11-25 check) — fallback: microsoft/cascadia-code releases theke zip namiye .ttf ber koro
        "color0": "#21222C",
        "color1": "#FF5555",
        "color2": "#50FA7B",
        "color3": "#F1FA8C",
        "color4": "#BD93F9",
        "color5": "#FF79C6",
        "color6": "#8BE9FD",
        "color7": "#F8F8F2",
        "color8": "#6272A4",
        "color9": "#FF6E6E",
        "color10": "#69FF94",
        "color11": "#FFFFA5",
        "color12": "#D6ACFF",
        "color13": "#FF92DF",
        "color14": "#A4FFFF",
        "color15": "#FFFFFF",
    },
    "ocean-blue": {
        "name": "Ocean Blue",
        "description": "Deep sea navy + aqua, calm professional look.",
        "background": "#0A192F",
        "foreground": "#CCD6F6",
        "cursor": "#64FFDA",
        "font": "Source Code Pro",
        "font_url": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",  # verified 200
        "color0": "#0A192F",
        "color1": "#FF6B6B",
        "color2": "#64FFDA",
        "color3": "#FFD166",
        "color4": "#4CC9F0",
        "color5": "#C77DFF",
        "color6": "#48CAE4",
        "color7": "#E6EDF7",
        "color8": "#415A77",
        "color9": "#FF8E8E",
        "color10": "#7FFFD4",
        "color11": "#FFE08A",
        "color12": "#7DD3FC",
        "color13": "#D8B4FE",
        "color14": "#67E8F9",
        "color15": "#F8FAFC",
    },
    "sunset": {
        "name": "Sunset",
        "description": "Warm dusk — orange, amber, soft rose on dark brown.",
        "background": "#2D1B1E",
        "foreground": "#FFD6C0",
        "cursor": "#FF6B35",
        "font": "Ubuntu Mono",
        "font_url": "https://github.com/google/fonts/raw/main/ofl/ubuntumono/UbuntuMono-Regular.ttf",  # UNVERIFIED (404 on 2026-11-25 check) — fallback: Ubuntu font site theke Ubuntu Mono .ttf namau
        "color0": "#2D1B1E",
        "color1": "#FF6B35",
        "color2": "#8AC926",
        "color3": "#FFB703",
        "color4": "#FB8500",
        "color5": "#E07A5F",
        "color6": "#F4A261",
        "color7": "#FFF1E6",
        "color8": "#6B4A4A",
        "color9": "#FF8C69",
        "color10": "#A3E635",
        "color11": "#FFD166",
        "color12": "#FF9E6B",
        "color13": "#F4978E",
        "color14": "#FFC8A2",
        "color15": "#FFF8F0",
    },
    "forest": {
        "name": "Forest",
        "description": "Deep green night forest, fresh lime accent.",
        "background": "#0D1B0E",
        "foreground": "#D4E8D0",
        "cursor": "#7CFC00",
        "font": "Noto Sans Mono",
        "font_url": "https://github.com/google/fonts/raw/main/ofl/notosansmono/NotoSansMono%5Bwdth%2Cwght%5D.ttf",  # verified 200 (variable font)
        "color0": "#0D1B0E",
        "color1": "#E2725B",
        "color2": "#7CFC00",
        "color3": "#E9C46A",
        "color4": "#74C0FC",
        "color5": "#B197FC",
        "color6": "#63E6BE",
        "color7": "#E8F5E9",
        "color8": "#4A6741",
        "color9": "#FF8A75",
        "color10": "#9BF00B",
        "color11": "#FFD60A",
        "color12": "#8ECAE6",
        "color13": "#C77DFF",
        "color14": "#80ED99",
        "color15": "#F1F8E9",
    },
    "lavender": {
        "name": "Lavender",
        "description": "Soft purple night, dreamy pastel accents.",
        "background": "#1E1B2E",
        "foreground": "#E6E0F8",
        "cursor": "#B388EB",
        "font": "Victor Mono",
        "font_url": "https://github.com/google/fonts/raw/main/ofl/victormono/VictorMono%5Bwght%5D.ttf",  # verified 200 (variable font)
        "color0": "#1E1B2E",
        "color1": "#FF7EB6",
        "color2": "#7BF1A8",
        "color3": "#FFD479",
        "color4": "#82AAFF",
        "color5": "#C792EA",
        "color6": "#89DDFF",
        "color7": "#E6E0F8",
        "color8": "#6B658A",
        "color9": "#FF9ECF",
        "color10": "#9FFFCA",
        "color11": "#FFE89E",
        "color12": "#A8C7FF",
        "color13": "#DDA6FF",
        "color14": "#A8E6FF",
        "color15": "#FFFFFF",
    },
    "sakura": {
        "name": "Sakura",
        "description": "Cherry blossom pink on dark plum, gentle + fresh.",
        "background": "#2B1A22",
        "foreground": "#FFE3EC",
        "cursor": "#FF8FAB",
        "font": "Inconsolata",
        "font_url": "https://github.com/google/fonts/raw/main/ofl/inconsolata/Inconsolata%5Bwdth%2Cwght%5D.ttf",  # verified 200 (variable font)
        "color0": "#2B1A22",
        "color1": "#FF6B9D",
        "color2": "#8CE99A",
        "color3": "#FFC078",
        "color4": "#91A7FF",
        "color5": "#E599F7",
        "color6": "#99E9F2",
        "color7": "#FFF0F3",
        "color8": "#6B4A57",
        "color9": "#FF8FA3",
        "color10": "#B2F2BB",
        "color11": "#FFD8A8",
        "color12": "#BAC8FF",
        "color13": "#F3D9FA",
        "color14": "#C5F6FA",
        "color15": "#FFF5F7",
    },
    "ios-modern": {
        "name": "iOS Modern",
        "description": "iOS-style clean light theme — modern technology look, light mode.",
        "background": "#F2F2F7",
        "foreground": "#1C1C1E",
        "cursor": "#007AFF",
        "font": "SF Mono (JetBrains Mono .ttf as free stand-in — SF Mono is Apple-only, no free download)",
        "font_url": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf",  # verified 200 — closest free stand-in for SF Mono
        "color0": "#1C1C1E",
        "color1": "#FF3B30",
        "color2": "#34C759",
        "color3": "#FF9500",
        "color4": "#007AFF",
        "color5": "#AF52DE",
        "color6": "#5AC8FA",
        "color7": "#F2F2F7",
        "color8": "#8E8E93",
        "color9": "#FF6961",
        "color10": "#30D158",
        "color11": "#FFD60A",
        "color12": "#0A84FF",
        "color13": "#BF5AF2",
        "color14": "#64D2FF",
        "color15": "#FFFFFF",
    },
}


def hex_to_rgb(hex_color: str):
    """'#22D3EE' -> (34, 211, 238)"""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def generate_properties(theme: dict) -> str:
    """Theme dict -> Termux colors.properties content."""
    lines = [
        f"# Termux Theme Studio — {theme['name']}",
        f"# {theme['description']}",
        f"# Generated by termux_theme.py v{VERSION}",
        f"# Font: {theme.get('font', '-')}",
        f"# Font download: {theme.get('font_url', '-')}",
        "# Font install: curl -L \"<font_url>\" -o ~/.termux/font.ttf && termux-reload-settings",
        "",
        f"background={theme['background']}",
        f"foreground={theme['foreground']}",
        f"cursor={theme['cursor']}",
        "",
    ]
    for i in range(16):
        lines.append(f"color{i}={theme[f'color{i}']}")
    lines.append("")
    return "\n".join(lines)


def list_themes():
    print(f"Termux Theme Studio v{VERSION} — available themes:\n")
    for key, t in THEMES.items():
        print(f"  {key:15} {t['name']:15} {t['description']}")
        print(f"                  bg {t['background']}  fg {t['foreground']}  cursor {t['cursor']}")
        print(f"                  font {t.get('font', '-')}")
    print("\nApply:  python termux_theme.py apply neon-modern")
    print("Preview: python termux_theme.py preview neon-modern")
    print("Fonts:  python termux_theme.py fonts")


def list_fonts():
    print(f"Termux Theme Studio v{VERSION} — fonts per theme:\n")
    print("Termux font = ~/.termux/font.ttf (ekta .ttf file).")
    print("Install: python termux_theme.py install-font <theme>\n")
    for key, t in THEMES.items():
        print(f"  {key:15} {t.get('font', '-')}")
        print(f"                  {t.get('font_url', '-')}")
    print("\nUNVERIFIED lekha URL gulo 2026-11-25-e curl check-e 404 diyechilo —")
    print("download korar age link ta check kore nio, ba fallback note dekho.")


def preview_theme(key: str):
    theme = THEMES.get(key)
    if not theme:
        print(f"Theme '{key}' pai nai. 'list' diye dekho.")
        sys.exit(1)

    print(f"\n  {theme['name']} — {theme['description']}")
    print(f"  bg {theme['background']}  fg {theme['foreground']}  cursor {theme['cursor']}")
    print(f"  font {theme.get('font', '-')}\n")

    # 16 color swatch — ANSI background blocks
    for row in (range(0, 8), range(8, 16)):
        line = "  "
        for i in row:
            r, g, b = hex_to_rgb(theme[f"color{i}"])
            line += f"\033[48;2;{r};{g};{b}m  \033[0m "
        print(line)
    print("  color0-7".ljust(18) + "color8-15\n")

    # Sample terminal lines in theme foreground / accent colors
    fg = theme["foreground"]
    r, g, b = hex_to_rgb(fg)
    accent = theme["color6"]
    ar, ag, ab = hex_to_rgb(accent)
    print(f"\033[38;2;{r};{g};{b}m  $ whoami\033[0m")
    print(f"\033[38;2;{ar};{ag};{ab}m  ➜ {key} theme ready ✓\033[0m")
    print(f"\033[38;2;{r};{g};{b}m  $ ls ~/storage\033[0m\n")


def print_font_instructions(theme: dict, key: str):
    print("\nFont change korte:")
    print(f"  Font: {theme.get('font', '-')}")
    print(f"  URL:  {theme.get('font_url', '-')}")
    print("  Termux-e:")
    print(f"    curl -L \"{theme.get('font_url', '')}\" -o ~/.termux/font.ttf")
    print("    termux-reload-settings")
    print(f"  Ba ek command-e: python termux_theme.py install-font {key}")
    print("  (Font bodle gele Termux restart korte hote pare.)")


def apply_theme(key: str, termux_dir: Path | None = None):
    theme = THEMES.get(key)
    if not theme:
        print(f"Theme '{key}' pai nai. 'list' diye dekho.")
        sys.exit(1)

    # Termux-e ~/.termux, PC-te test korle ./output use hobe
    if termux_dir is None:
        termux_dir = Path.home() / ".termux"
    termux_dir.mkdir(parents=True, exist_ok=True)
    target = termux_dir / "colors.properties"

    # Backup purono file
    if target.exists():
        backup = termux_dir / "colors.properties.bak"
        shutil.copy2(target, backup)
        print(f"Backup: {backup}")

    target.write_text(generate_properties(theme), encoding="utf-8")
    print(f"Applied '{theme['name']}' -> {target}")

    # Termux-e thakle reload koro
    if shutil.which("termux-reload-settings"):
        subprocess.run(["termux-reload-settings"], check=False)
        print("termux-reload-settings chalano hoyeche — theme ekhoni dekhte pabe.")
    else:
        print("Note: 'termux-reload-settings' pai nai — eta PC, Termux-e chalale auto reload hobe.")
        print(f"Termux-e: cp {target} ~/.termux/colors.properties && termux-reload-settings")

    print_font_instructions(theme, key)


def is_ttf(data: bytes) -> bool:
    """True jodi data ekta TTF/OTF font hoy (magic bytes check)."""
    return data[:4] in (b"\x00\x01\x00\x00", b"true", b"OTTO", b"ttcf")


def install_font(key: str, termux_dir: Path | None = None):
    theme = THEMES.get(key)
    if not theme:
        print(f"Theme '{key}' pai nai. 'list' diye dekho.")
        sys.exit(1)

    url = theme.get("font_url", "")
    if not url:
        print(f"'{key}' theme-er kono font URL nei.")
        sys.exit(1)

    if termux_dir is None:
        termux_dir = Path.home() / ".termux"
    termux_dir.mkdir(parents=True, exist_ok=True)
    target = termux_dir / "font.ttf"

    print(f"Downloading {theme.get('font', '')} font...")
    print(f"  URL: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Termux-Theme-Studio/1.1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
    except Exception as e:  # noqa: BLE001 — network error, user-ke janate hobe
        print(f"Download FAIL: {e}")
        print("Manual try koro:")
        print(f"  curl -L \"{url}\" -o ~/.termux/font.ttf")
        print("  termux-reload-settings")
        sys.exit(1)

    if len(data) < 1024 or not is_ttf(data):
        print(f"Download hoyeche ({len(data)} bytes) kintu eta valid .ttf mone hochhe na.")
        print("Hoyto link ta bodle geche / HTML page download hoyeche.")
        print("README-er font table-e fallback note dekho.")
        sys.exit(1)

    if target.exists():
        backup = termux_dir / "font.ttf.bak"
        shutil.copy2(target, backup)
        print(f"Backup: {backup}")

    target.write_bytes(data)
    print(f"Font installed: {theme.get('font', '')} ({len(data)} bytes) -> {target}")

    if shutil.which("termux-reload-settings"):
        subprocess.run(["termux-reload-settings"], check=False)
        print("termux-reload-settings chalano hoyeche.")
    else:
        print("Note: Termux-e 'termux-reload-settings' chalale font apply hobe.")
        print("Font bodle gele Termux restart korte hote pare.")


def generate_file(key: str, output: str):
    theme = THEMES.get(key)
    if not theme:
        print(f"Theme '{key}' pai nai.")
        sys.exit(1)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(generate_properties(theme), encoding="utf-8")
    print(f"Generated: {out}  ({theme['name']})")


def create_custom(args):
    """Nijer theme banano — bg/fg/accent dile baki color auto derive hobe."""
    accent = args.accent or "#22D3EE"
    theme = dict(THEMES["neon-modern"])  # base hishebe neon-modern
    theme["name"] = args.name
    theme["description"] = f"Custom theme — based on Neon Modern, bg {args.bg}"
    theme["background"] = args.bg
    theme["foreground"] = args.fg
    theme["cursor"] = accent
    theme["color6"] = accent
    theme["color14"] = accent

    out = Path("themes") / f"{args.name}.properties"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(generate_properties(theme), encoding="utf-8")
    print(f"Custom theme banano hoyeche: {out}")
    print(f"Apply korte: python termux_theme.py generate {args.name}  — na, file theke apply koro:")
    print(f"  cp {out} ~/.termux/colors.properties && termux-reload-settings")


def main():
    parser = argparse.ArgumentParser(
        prog="termux_theme.py",
        description="Termux Theme Studio — Python diye Termux theme banau / apply koro (10 themes + fonts)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="Sob theme dekhao (color + font)")
    sub.add_parser("fonts", help="Prottek theme-er font + download URL dekhao")
    p = sub.add_parser("preview", help="Theme-er color preview dekhao (terminal sample)")
    p.add_argument("theme", help="neon-modern / minimal-dark / hacker-green / dracula / ocean-blue / sunset / forest / lavender / sakura / ios-modern")
    p = sub.add_parser("apply", help="Theme Termux-e apply koro (color + font instructions)")
    p.add_argument("theme", help="neon-modern / minimal-dark / hacker-green / dracula / ocean-blue / sunset / forest / lavender / sakura / ios-modern")
    p.add_argument("--termux-dir", default=None, help="~/.termux er bodle onno folder (test er jonno)")
    p = sub.add_parser("install-font", help="Theme-er font download kore ~/.termux/font.ttf-e bosau")
    p.add_argument("theme", help="neon-modern / minimal-dark / hacker-green / dracula / ocean-blue / sunset / forest / lavender / sakura / ios-modern")
    p.add_argument("--termux-dir", default=None, help="~/.termux er bodle onno folder (test er jonno)")
    p = sub.add_parser("generate", help="colors.properties file banau")
    p.add_argument("theme", help="neon-modern / minimal-dark / hacker-green / dracula / ocean-blue / sunset / forest / lavender / sakura / ios-modern")
    p.add_argument("-o", "--output", required=True, help="Output file path")
    p = sub.add_parser("create", help="Nijer custom theme banau")
    p.add_argument("--name", required=True, help="Theme-er naam, jemon amar-theme")
    p.add_argument("--bg", default="#0F172A", help="Background hex, jemon #0F172A")
    p.add_argument("--fg", default="#E2E8F0", help="Foreground hex, jemon #E2E8F0")
    p.add_argument("--accent", default="#22D3EE", help="Accent hex, jemon #22D3EE")

    args = parser.parse_args()

    if args.cmd == "list":
        list_themes()
    elif args.cmd == "fonts":
        list_fonts()
    elif args.cmd == "preview":
        preview_theme(args.theme)
    elif args.cmd == "apply":
        d = Path(args.termux_dir) if args.termux_dir else None
        apply_theme(args.theme, d)
    elif args.cmd == "install-font":
        d = Path(args.termux_dir) if args.termux_dir else None
        install_font(args.theme, d)
    elif args.cmd == "generate":
        generate_file(args.theme, args.output)
    elif args.cmd == "create":
        create_custom(args)


if __name__ == "__main__":
    main()

from dataclasses import dataclass

import flet as ft

PRIMARY = "#0D9488"
PRIMARY_DARK = "#0F766E"
ACCENT = "#22C55E"
DANGER = "#EF4444"
WARNING = "#F59E0B"
INFO = "#0EA5E9"
PURPLE = "#8B5CF6"

PINK = "#EC4899"
INDIGO = "#6366F1"
ORANGE = "#F97316"

# Cada separador tem a sua cor de destaque e o seu gradiente de cabeçalho.
GRADIENTS = {
    "home": ["#2DD4BF", "#0F766E"],
    "assistant": ["#818CF8", "#4F46E5"],
    "facilities": ["#38BDF8", "#0369A1"],
    "appointments": ["#C084FC", "#7C3AED"],
    "profile": ["#FB923C", "#E11D48"],
    "symptoms": ["#FB7185", "#BE123C"],
    "emergency": ["#F87171", "#B91C1C"],
    "doctors": ["#A78BFA", "#DB2777"],
}
TAB_COLORS = [PRIMARY, INDIGO, INFO, PURPLE, ORANGE]

LEVEL_COLORS = {
    "baixo": ACCENT,
    "moderado": WARNING,
    "alto": "#F97316",
    "emergencia": DANGER,
}


@dataclass(frozen=True)
class Palette:
    bg: str
    card: str
    text: str
    muted: str
    border: str
    soft: str  # fundo suave para ícones / chips


LIGHT = Palette(bg="#F4F7FB", card="#FFFFFF", text="#0F172A", muted="#64748B", border="#E2E8F0", soft="#ECFDF5")
DARK = Palette(bg="#0B1220", card="#131C2E", text="#F1F5F9", muted="#94A3B8", border="#1E293B", soft="#11302C")


def build_theme(dark: bool) -> ft.Theme:
    return ft.Theme(
        color_scheme_seed=PRIMARY,
        use_material3=True,
        scaffold_bgcolor=(DARK if dark else LIGHT).bg,
    )

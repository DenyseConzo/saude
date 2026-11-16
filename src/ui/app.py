"""Shell da aplicação: navegação por separadores + pilha de ecrãs."""

import flet as ft

from services.store import Store
from ui import theme
from ui.screens import (
    appointments,
    assistant,
    emergency,
    facilities,
    home,
    onboarding,
    profile,
)

MAX_WIDTH = 520

TABS = [
    ("Início", ft.Icons.HOME_OUTLINED, ft.Icons.HOME_ROUNDED, home.build),
    ("Assistente", ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, ft.Icons.CHAT_BUBBLE_ROUNDED, assistant.build),
    ("Unidades", ft.Icons.LOCATION_ON_OUTLINED, ft.Icons.LOCATION_ON_ROUNDED, facilities.build),
    ("Consultas", ft.Icons.CALENDAR_MONTH_OUTLINED, ft.Icons.CALENDAR_MONTH_ROUNDED, appointments.build),
    ("Perfil", ft.Icons.PERSON_OUTLINE_ROUNDED, ft.Icons.PERSON_ROUNDED, profile.build),
]
TAB_INDEX = {"home": 0, "assistant": 1, "facilities": 2, "appointments": 3, "profile": 4}


class App:
    def __init__(self, page: ft.Page, store: Store | None = None):
        self.page = page
        self.store = store or Store()
        self.tab = 0
        self.stack: list[tuple] = []  # ecrãs empilhados por cima do separador atual
        self.chat: list[dict] = []  # histórico do assistente
        self.body = ft.Container(expand=True)
        self.root = ft.Container(expand=True, width=MAX_WIDTH, alignment=ft.Alignment.TOP_CENTER)

    # ---------- utilitários de estilo ----------
    @property
    def c(self) -> theme.Palette:
        return theme.DARK if self.store.dark_mode else theme.LIGHT

    def fs(self, size: float) -> float:
        return round(size * (1.2 if self.store.large_text else 1.0), 1)

    # ---------- arranque ----------
    def start(self):
        p = self.page
        p.title = "Saúde Fácil"
        p.padding = 0
        p.spacing = 0
        p.on_resize = lambda e: self._fit_width()
        self.apply_theme()
        p.add(ft.Row([self.root], alignment=ft.MainAxisAlignment.CENTER, expand=True, vertical_alignment=ft.CrossAxisAlignment.START))
        self._fit_width()
        self.render()

    def _fit_width(self):
        w = self.page.width
        self.root.width = min(w, MAX_WIDTH) if w else MAX_WIDTH
        self.page.update()

    def apply_theme(self):
        self.page.theme_mode = ft.ThemeMode.DARK if self.store.dark_mode else ft.ThemeMode.LIGHT
        self.page.theme = theme.build_theme(False)
        self.page.dark_theme = theme.build_theme(True)
        self.page.bgcolor = self.c.bg

    # ---------- navegação ----------
    def go_tab(self, name_or_index):
        self.tab = TAB_INDEX.get(name_or_index, name_or_index) if isinstance(name_or_index, str) else name_or_index
        self.stack.clear()
        self.render()

    def push(self, builder, *args):
        self.stack.append((builder, args))
        self.render()

    def back(self):
        if self.stack:
            self.stack.pop()
        self.render()

    def open_emergency(self):
        self.push(emergency.build)

    def render(self):
        self.page.bgcolor = self.c.bg
        if not self.store.onboarded:
            self.root.content = ft.SafeArea(onboarding.build(self), expand=True)
        else:
            if self.stack:
                builder, args = self.stack[-1]
                self.body.content = builder(self, *args)
            else:
                self.body.content = TABS[self.tab][3](self)
            self.root.content = ft.SafeArea(
                ft.Column([self.body, self._nav_bar()], spacing=0, expand=True),
                expand=True,
            )
        self.page.update()

    def _nav_bar(self) -> ft.NavigationBar:
        # A cor do indicador acompanha a cor de destaque de cada separador.
        return ft.NavigationBar(
            selected_index=self.tab,
            bgcolor=self.c.card,
            indicator_color=ft.Colors.with_opacity(0.18, theme.TAB_COLORS[self.tab]),
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=70,
            destinations=[
                ft.NavigationBarDestination(
                    label=label,
                    icon=ft.Icon(ic, color=theme.TAB_COLORS[i], opacity=0.7),
                    selected_icon=ft.Icon(sel, color=theme.TAB_COLORS[i]),
                )
                for i, (label, ic, sel, _) in enumerate(TABS)
            ],
            on_change=lambda e: self.go_tab(e.control.selected_index),
        )

    # ---------- feedback ----------
    def toast(self, message: str, color=None):
        self.page.show_dialog(
            ft.SnackBar(
                ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=color or theme.PRIMARY_DARK,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=14),
                duration=2500,
            )
        )

    def call(self, number: str):
        self.toast(f"A ligar para {number}…")
        try:
            self.page.launch_url(f"tel:{number.replace(' ', '')}")
        except Exception:
            pass

    def reset_demo(self):
        dark = self.store.dark_mode
        self.store = Store()
        self.store.dark_mode = dark
        self.chat.clear()
        self.tab = 0
        self.stack.clear()
        self.render()

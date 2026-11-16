import flet as ft

from data.mock_data import LANGUAGES
from ui import components as ui
from ui import theme

LANG_COLORS = [theme.PRIMARY, theme.ORANGE, theme.PINK, theme.INDIGO, theme.INFO]

ABOUT = (
    "A Saúde Fácil nasceu para aproximar a população moçambicana da informação em saúde, "
    "usando a inteligência artificial como apoio à tomada de decisão.\n\n"
    "Missão: utilizar a tecnologia para tornar a saúde mais acessível, preventiva e próxima das pessoas.\n\n"
    "Esta versão de demonstração usa apenas dados fictícios."
)


def build(app) -> ft.Control:
    s = app.store
    u = s.user

    def set_flag(key, value):
        setattr(s, key, value)
        if key == "dark_mode":
            app.apply_theme()
        app.render()

    def set_lang(lang):
        s.language = lang
        app.toast(f"Idioma: {lang}" + ("" if lang == "Português" else " (tradução parcial — em breve)"))
        app.render()

    def show_about(e):
        app.page.show_dialog(
            ft.AlertDialog(
                icon=ft.Image(src="logo.png", height=110, fit=ft.BoxFit.CONTAIN),
                title=ft.Text("Saúde Fácil · Easy Health"),
                content=ft.Text(ABOUT),
                actions=[ft.TextButton("Fechar", on_click=lambda e: app.page.pop_dialog())],
                shape=ft.RoundedRectangleBorder(radius=24),
            )
        )

    def health_stat(icon_name, label, value, color):
        return ft.Container(
            col={"xs": 6},
            padding=14,
            border_radius=18,
            bgcolor=ui.tint(color, 0.1),
            content=ft.Column([ft.Icon(ui.icon(icon_name), color=color, size=22), ui.muted(app, label, 12), ui.txt(app, value, 15, ft.FontWeight.BOLD)], spacing=4),
        )

    def setting(icon_name, title, subtitle, control, color=theme.PRIMARY, on_click=None):
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=8),
            on_click=on_click,
            content=ft.Row(
                [
                    ui.icon_badge(icon_name, color, size=40, icon_size=20, radius=12),
                    ft.Column([ui.txt(app, title, 14, ft.FontWeight.W_600), ui.muted(app, subtitle, 12)], spacing=0, expand=True),
                    control,
                ],
                spacing=12,
            ),
        )

    profile_card = ft.Container(
        padding=20,
        border_radius=24,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=theme.GRADIENTS["appointments"]),
        shadow=ft.BoxShadow(blur_radius=20, color=ui.tint(theme.PURPLE, 0.35), offset=ft.Offset(0, 8)),
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Text("".join(p[0] for p in u["name"].split()[:2]), size=24, weight=ft.FontWeight.BOLD, color=theme.PRIMARY),
                    width=68, height=68, border_radius=34, bgcolor=ft.Colors.WHITE, alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(u["name"], size=app.fs(19), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(f"{u['age']} anos · {u['city']}", size=app.fs(13), color=ft.Colors.WHITE, opacity=0.88),
                        ft.Text(u["phone"], size=app.fs(12), color=ft.Colors.WHITE, opacity=0.88),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.IconButton(ft.Icons.EDIT_ROUNDED, icon_color=ft.Colors.WHITE, on_click=lambda e: app.toast("Edição de perfil — em breve")),
            ],
            spacing=14,
        ),
    )

    stats = ft.ResponsiveRow(
        [
            health_stat("BLOODTYPE", "Tipo sanguíneo", u["blood_type"], theme.DANGER),
            health_stat("CAKE", "Idade", f"{u['age']} anos", theme.INFO),
            health_stat("NO_FOOD", "Alergias", ", ".join(u["allergies"]) or "Nenhuma", theme.WARNING),
            health_stat("FAVORITE", "Condições", ", ".join(u["conditions"]) or "Nenhuma", theme.PURPLE),
        ],
        spacing=10,
        run_spacing=10,
    )

    languages = ft.Row(
        [
            ui.pill(app, lang, selected=s.language == lang, color=LANG_COLORS[i % len(LANG_COLORS)], on_click=lambda e, lang=lang: set_lang(lang))
            for i, lang in enumerate(LANGUAGES)
        ],
        wrap=True,
        spacing=8,
        run_spacing=8,
    )

    settings = ui.card(
        app,
        ft.Column(
            [
                setting("TEXT_INCREASE", "Texto grande", "Facilita a leitura", ft.Switch(value=s.large_text, active_color=theme.PRIMARY, on_change=lambda e: set_flag("large_text", e.control.value))),
                setting("DARK_MODE", "Modo escuro", "Poupa bateria à noite", ft.Switch(value=s.dark_mode, active_color=theme.PURPLE, on_change=lambda e: set_flag("dark_mode", e.control.value)), theme.PURPLE),
                setting("NOTIFICATIONS_ACTIVE", "Lembretes", "Consultas e medicação", ft.Switch(value=True, active_color=theme.WARNING), theme.WARNING),
                setting("SOS", "Emergência", "Números e primeiros socorros", ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=app.c.muted), theme.DANGER, lambda e: app.open_emergency()),
                setting("INFO_OUTLINE", "Sobre a Saúde Fácil", "Missão e visão do projeto", ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=app.c.muted), theme.INFO, show_about),
                setting("RESTART_ALT", "Reiniciar demonstração", "Repõe os dados mock e o onboarding", ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=app.c.muted), app.c.muted, lambda e: app.reset_demo()),
            ],
            spacing=2,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
    )

    return ft.Column(
        [
            ui.hero(app, "Perfil", "A sua ficha e preferências", key="profile", back=False),
            ui.scroll_body(
                [
                    profile_card,
                    ui.section(app, "Ficha de saúde"),
                    stats,
                    ui.section(app, "Idioma"),
                    languages,
                    ui.section(app, "Definições"),
                    settings,
                    ft.Container(ui.muted(app, "Saúde Fácil v0.1 · Dados fictícios para demonstração", 11, text_align=ft.TextAlign.CENTER), alignment=ft.Alignment.CENTER),
                ],
                spacing=14,
            ),
        ],
        spacing=0,
        expand=True,
    )

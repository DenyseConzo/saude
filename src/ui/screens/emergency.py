import flet as ft

from data.mock_data import EMERGENCY_CONTACTS
from ui import components as ui
from ui import theme

CONTACT_GRADIENTS = [["#F87171", "#DC2626"], ["#34D399", "#0F766E"], ["#60A5FA", "#1D4ED8"]]

FIRST_AID = [
    ("Desmaio", "Deite a pessoa de costas e eleve-lhe as pernas. Afrouxe roupas apertadas."),
    ("Queimadura", "Arrefeça com água corrente durante 10 minutos. Não aplique pasta de dentes nem óleo."),
    ("Hemorragia", "Pressione a ferida com um pano limpo e mantenha a pressão até chegar ajuda."),
    ("Convulsão", "Afaste objetos perigosos, não coloque nada na boca e vire a pessoa de lado no fim."),
]


def build(app) -> ft.Control:
    big = ft.Container(
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.symmetric(vertical=10),
        content=ft.Container(
            width=170,
            height=170,
            border_radius=85,
            bgcolor=ui.tint(theme.DANGER, 0.12),
            alignment=ft.Alignment.CENTER,
            content=ft.Container(
                width=130,
                height=130,
                border_radius=65,
                gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=["#F87171", "#DC2626"]),
                shadow=ft.BoxShadow(blur_radius=30, color=ui.tint(theme.DANGER, 0.5), offset=ft.Offset(0, 10)),
                alignment=ft.Alignment.CENTER,
                on_click=lambda e: app.call("112"),
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.CALL_ROUNDED, color=ft.Colors.WHITE, size=36),
                        ft.Text("112", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
            ),
        ),
    )

    contacts = [
        ui.card(
            app,
            ft.Row(
                [
                    ui.gradient_tile(c["icon"], g, size=50, icon_size=24, radius=16),
                    ft.Column([ui.txt(app, c["name"], 15, ft.FontWeight.BOLD), ui.muted(app, c["desc"], 12)], spacing=0, expand=True),
                    ft.Container(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.CALL_ROUNDED, color=ft.Colors.WHITE, size=18),
                             ft.Text(c["number"], color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=app.fs(16))],
                            spacing=6, tight=True,
                        ),
                        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                        border_radius=24,
                        gradient=ft.LinearGradient(colors=g),
                    ),
                ],
                spacing=12,
            ),
            on_click=lambda e, n=c["number"]: app.call(n),
            accent=g[1],
        )
        for c, g in zip(EMERGENCY_CONTACTS, CONTACT_GRADIENTS)
    ]

    aid = [
        ft.ExpansionTile(
            title=ui.txt(app, title, 15, ft.FontWeight.W_600),
            leading=ft.Icon(ft.Icons.MEDICAL_INFORMATION_ROUNDED, color=theme.DANGER),
            controls=[ft.Container(ui.muted(app, body, 13), padding=ft.Padding.only(left=16, right=16, bottom=12))],
            bgcolor=app.c.card,
            collapsed_bgcolor=app.c.card,
            shape=ft.RoundedRectangleBorder(radius=16),
            collapsed_shape=ft.RoundedRectangleBorder(radius=16),
        )
        for title, body in FIRST_AID
    ]

    return ft.Column(
        [
            ui.hero(app, "Emergência", "Toque num número para ligar", key="emergency"),
            ui.scroll_body(
                [
                    big,
                    ui.muted(app, "112 · Emergência geral — partilhe a sua localização com quem atender.", 13, text_align=ft.TextAlign.CENTER),
                    ui.section(app, "Números úteis"),
                    *contacts,
                    ui.section(app, "Primeiros socorros"),
                    *aid,
                ],
                spacing=12,
            ),
        ],
        spacing=0,
        expand=True,
    )

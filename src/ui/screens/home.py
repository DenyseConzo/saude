import flet as ft

from data.mock_data import GREETINGS, HEALTH_TIPS
from ui import components as ui
from ui import theme
from ui.screens import doctors, facilities, symptoms


def build(app) -> ft.Control:
    s = app.store
    greeting = GREETINGS.get(s.language, "Olá")

    hero = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=["#2DD4BF", "#0D9488", "#1E40AF"]
        ),
        border_radius=ft.BorderRadius.only(bottom_left=32, bottom_right=32),
        padding=ft.Padding.only(left=20, right=20, top=16, bottom=28),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ui.logo(white=True, height=30),
                            padding=8,
                            border_radius=16,
                            bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
                        ),
                        ft.Column(
                            [
                                ft.Text(f"{greeting}, {s.user['first_name']} 👋", size=app.fs(22), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text("Como se sente hoje?", size=app.fs(14), color=ft.Colors.WHITE, opacity=0.85),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                            icon_color=ft.Colors.WHITE,
                            badge=ft.Badge(small_size=8, bgcolor="#F87171"),
                            on_click=lambda e: app.toast("Lembrete: consulta confirmada para segunda-feira às 09:30."),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
                        ),
                    ]
                ),
                ft.Container(height=8),
                # "Barra de pesquisa" que abre o assistente
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=16,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                    on_click=lambda e: app.go_tab("assistant"),
                    ink=True,
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=theme.PRIMARY, size=20),
                            ft.Text("Descreva o que sente…", color="#94A3B8", size=app.fs(14), expand=True),
                            ft.Icon(ft.Icons.MIC_NONE_ROUNDED, color=theme.PRIMARY, size=20),
                        ],
                        spacing=10,
                    ),
                ),
            ]
        ),
    )

    def quick(label, icon_name, key, on_click):
        tile = ft.Container(
            col={"xs": 3},
            on_click=on_click,
            border_radius=16,
            ink=True,
            padding=ft.Padding.symmetric(vertical=6),
            animate_scale=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
            content=ft.Column(
                [ui.gradient_tile(icon_name, theme.GRADIENTS[key]), ui.txt(app, label, 12, ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
        )

        def hover(e):
            tile.scale = 1.08 if e.data in (True, "true") else 1
            tile.update()

        tile.on_hover = hover
        return tile

    quick_actions = ft.ResponsiveRow(
        [
            quick("Sintomas", "MONITOR_HEART", "symptoms", lambda e: app.push(symptoms.build)),
            quick("Assistente", "SMART_TOY", "assistant", lambda e: app.go_tab("assistant")),
            quick("Unidades", "LOCAL_HOSPITAL", "facilities", lambda e: app.go_tab("facilities")),
            quick("Médicos", "MEDICAL_SERVICES", "doctors", lambda e: app.push(doctors.build)),
        ],
        spacing=8,
    )

    sos = ft.Container(
        border_radius=20,
        padding=16,
        gradient=ft.LinearGradient(begin=ft.Alignment.CENTER_LEFT, end=ft.Alignment.CENTER_RIGHT, colors=["#F87171", theme.DANGER]),
        on_click=lambda e: app.open_emergency(),
        ink=True,
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Text("SOS", color=theme.DANGER, weight=ft.FontWeight.BOLD, size=app.fs(14)),
                    bgcolor=ft.Colors.WHITE, width=52, height=52, border_radius=26, alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text("Emergência?", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=app.fs(16)),
                        ft.Text("Toque para ligar 112 ou ver primeiros socorros", color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE), size=app.fs(12)),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=ft.Colors.WHITE),
            ],
            spacing=14,
        ),
    )

    controls = [hero, ft.Container(content=quick_actions, padding=ft.Padding.symmetric(horizontal=12)), _padded(sos)]

    upcoming = s.upcoming()
    if upcoming:
        a = upcoming[0]
        d = s.get_doctor(a["doctor_id"])
        controls += [
            _padded(ui.section(app, "Próxima consulta", "Ver todas", lambda e: app.go_tab("appointments"))),
            _padded(
                ui.card(
                    app,
                    ft.Row(
                        [
                            ui.avatar(d["initials"]),
                            ft.Column([ui.txt(app, d["name"], 15, ft.FontWeight.BOLD), ui.muted(app, d["specialty"])], spacing=2, expand=True),
                            ft.Column(
                                [ui.tag(app, a["date"], theme.PRIMARY, "EVENT"), ui.tag(app, f"{a['time']} · {a['mode']}", theme.INFO, "VIDEOCAM")],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=4,
                            ),
                        ],
                        spacing=12,
                    ),
                    on_click=lambda e: app.go_tab("appointments"),
                    accent=theme.PURPLE,
                )
            ),
        ]

    tips = ft.Row(
        [
            ft.Container(
                width=230,
                padding=16,
                border_radius=20,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[ft.Colors.with_opacity(0.75, t["color"]), t["color"]],
                ),
                shadow=ft.BoxShadow(blur_radius=16, color=ui.tint(t["color"], 0.35), offset=ft.Offset(0, 6)),
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ui.icon(t["icon"]), color=ft.Colors.WHITE, size=20),
                            width=40, height=40, border_radius=14, alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.with_opacity(0.22, ft.Colors.WHITE),
                        ),
                        ft.Text(t["title"], size=app.fs(15), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(t["body"], size=app.fs(12), color=ft.Colors.WHITE, opacity=0.92),
                    ],
                    spacing=8,
                ),
            )
            for t in HEALTH_TIPS
        ],
        scroll=ft.ScrollMode.HIDDEN,
        spacing=12,
    )
    controls += [_padded(ui.section(app, "Dicas de saúde")), ft.Container(content=tips, padding=ft.Padding.only(left=16))]

    near = s.nearest()
    if near:
        controls += [
            _padded(ui.section(app, "Mais perto de si", "Ver mapa", lambda e: app.go_tab("facilities"))),
            _padded(facilities.facility_card(app, near)),
        ]

    controls.append(ft.Container(height=12))
    return ft.Column(controls, spacing=16, scroll=ft.ScrollMode.AUTO, expand=True)


def _padded(control):
    return ft.Container(content=control, padding=ft.Padding.symmetric(horizontal=16))

import urllib.parse

import flet as ft

from services.store import FACILITY_TYPES
from ui import components as ui
from ui import theme

TYPE_STYLE = {
    "Hospital": ("LOCAL_HOSPITAL", theme.DANGER),
    "Centro de Saúde": ("HEALTH_AND_SAFETY", theme.PRIMARY),
    "Farmácia": ("MEDICATION", theme.PURPLE),
}


def facility_card(app, f) -> ft.Control:
    icon_name, color = TYPE_STYLE.get(f["type"], ("LOCAL_HOSPITAL", theme.PRIMARY))
    fav = f["id"] in app.store.favorites
    return ui.card(
        app,
        ft.Column(
            [
                ft.Row(
                    [
                        ui.icon_badge(icon_name, color, size=50, icon_size=26, radius=16),
                        ft.Column(
                            [
                                ui.txt(app, f["name"], 15, ft.FontWeight.BOLD, max_lines=2),
                                ui.muted(app, f["address"], 12, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.FAVORITE_ROUNDED if fav else ft.Icons.FAVORITE_BORDER_ROUNDED, color=theme.DANGER if fav else app.c.muted, size=20),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ui.tag(app, f"{f['distance_km']:.1f} km", theme.INFO, "NEAR_ME"),
                        ui.tag(app, "24h" if f["open_24h"] else f["hours"], theme.ACCENT if f["open_24h"] else theme.WARNING, "SCHEDULE"),
                        ui.tag(app, f"~{f['wait_min']} min", app.c.muted, "HOURGLASS_BOTTOM"),
                    ],
                    spacing=6,
                    wrap=True,
                ),
            ],
            spacing=12,
        ),
        on_click=lambda e: app.push(detail, f["id"]),
        accent=color,
    )


def build(app) -> ft.Control:
    state = {"type": "Todos", "query": "", "open": False}
    results = ft.Column(spacing=12)
    filters = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=8)

    def refresh(update=True):
        items = app.store.search_facilities(state["query"], state["type"], state["open"])
        filters.controls = [
            ui.pill(
                app, t, selected=state["type"] == t, on_click=lambda e, t=t: set_type(t),
                color=TYPE_STYLE.get(t, (None, theme.INFO))[1], leading=TYPE_STYLE.get(t, ("APPS",))[0],
            )
            for t in FACILITY_TYPES
        ] + [ui.pill(app, "Aberto 24h", selected=state["open"], color=theme.ACCENT, leading="SCHEDULE", on_click=lambda e: toggle_open())]
        results.controls = [facility_card(app, f) for f in items] or [
            ft.Container(
                padding=40,
                content=ft.Column(
                    [ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=48, color=app.c.muted), ui.muted(app, "Nenhuma unidade encontrada.", 14)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
            )
        ]
        if update:
            app.page.update()

    def set_type(t):
        state["type"] = t
        refresh()

    def toggle_open():
        state["open"] = not state["open"]
        refresh()

    def on_search(e):
        state["query"] = e.control.value
        refresh()

    search = ft.TextField(
        hint_text="Pesquisar unidade ou serviço (ex.: vacinação)",
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        border_radius=16,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.WHITE,
        text_size=app.fs(14),
        color="#0F172A",
        hint_style=ft.TextStyle(color="#94A3B8"),
        on_change=on_search,
    )

    # Mapa ilustrativo (mock) com marcadores posicionados manualmente.
    def pin(left, top, color):
        return ft.Container(
            content=ft.Icon(ft.Icons.LOCATION_ON_ROUNDED, color=color, size=30), left=left, top=top
        )

    fake_map = ft.Container(
        height=150,
        border_radius=20,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=["#CCFBF1", "#BAE6FD"]),
        content=ft.Stack(
            [
                ft.Container(left=-40, top=60, width=600, height=14, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), rotate=-0.12),
                ft.Container(left=140, top=-20, width=14, height=220, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), rotate=0.3),
                pin(60, 30, theme.DANGER),
                pin(200, 80, theme.PRIMARY),
                pin(300, 25, theme.PURPLE),
                ft.Container(
                    left=150, top=58, width=22, height=22, border_radius=11, bgcolor=theme.INFO,
                    border=ft.Border.all(4, ft.Colors.WHITE),
                    shadow=ft.BoxShadow(blur_radius=12, color=ui.tint(theme.INFO, 0.6)),
                ),
                ft.Container(
                    right=10, bottom=10, padding=ft.Padding.symmetric(horizontal=10, vertical=6), border_radius=12, bgcolor=ft.Colors.WHITE,
                    content=ft.Row([ft.Icon(ft.Icons.MY_LOCATION_ROUNDED, size=14, color=theme.INFO), ft.Text("Maputo", size=12, color="#0F172A")], spacing=4, tight=True),
                ),
            ],
            expand=True,
        ),
    )

    refresh(update=False)
    return ft.Column(
        [
            ui.hero(app, "Unidades sanitárias", "Ordenadas pela distância", key="facilities", back=False, extra=search),
            ui.scroll_body([filters, fake_map, results], spacing=14),
        ],
        spacing=0,
        expand=True,
    )


def detail(app, fid) -> ft.Control:
    f = app.store.get_facility(fid)
    icon_name, color = TYPE_STYLE.get(f["type"], ("LOCAL_HOSPITAL", theme.PRIMARY))
    fav = f["id"] in app.store.favorites

    def toggle_fav(e):
        added = app.store.toggle_favorite(fid)
        app.toast("Adicionado aos favoritos ❤️" if added else "Removido dos favoritos")
        app.render()

    def directions(e):
        app.page.launch_url("https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(f"{f['name']}, {f['address']}"))

    hero = ft.Container(
        padding=20,
        border_radius=24,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=[color, theme.PRIMARY_DARK]),
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ui.icon(icon_name), color=color, size=30),
                    bgcolor=ft.Colors.WHITE, width=56, height=56, border_radius=18, alignment=ft.Alignment.CENTER,
                ),
                ft.Text(f["name"], size=app.fs(21), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Row(
                    [
                        ft.Text(f["type"], size=app.fs(13), color=ft.Colors.WHITE, opacity=0.9),
                        ft.Text("•", color=ft.Colors.WHITE),
                        ft.Icon(ft.Icons.STAR_ROUNDED, size=16, color="#FDE68A"),
                        ft.Text(f"{f['rating']:.1f}", size=app.fs(13), color=ft.Colors.WHITE),
                    ],
                    spacing=6,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Column(
        [
            ui.header(
                app,
                "Detalhes",
                actions=[
                    ft.IconButton(
                        ft.Icons.FAVORITE_ROUNDED if fav else ft.Icons.FAVORITE_BORDER_ROUNDED,
                        icon_color=theme.DANGER,
                        on_click=toggle_fav,
                        tooltip="Favorito",
                    )
                ],
            ),
            ui.scroll_body(
                [
                    hero,
                    ui.card(
                        app,
                        ft.Column(
                            [
                                ui.info_row(app, "PLACE", "Endereço", f["address"]),
                                ui.info_row(app, "NEAR_ME", "Distância", f"{f['distance_km']:.1f} km · ~{int(f['distance_km'] * 3) + 2} min de carro"),
                                ui.info_row(app, "SCHEDULE", "Horário", f["hours"]),
                                ui.info_row(app, "HOURGLASS_BOTTOM", "Tempo de espera estimado", f"~{f['wait_min']} minutos"),
                                ui.info_row(app, "PHONE", "Telefone", f["phone"]),
                            ],
                            spacing=14,
                        ),
                    ),
                    ui.txt(app, "Serviços disponíveis", 16, ft.FontWeight.BOLD),
                    ft.Row([ui.tag(app, s, theme.PRIMARY, "CHECK_CIRCLE") for s in f["services"]], wrap=True, spacing=8, run_spacing=8),
                    ft.Row(
                        [
                            ui.secondary_button(app, "Ligar", lambda e: app.call(f["phone"]), "CALL"),
                            ui.primary_button(app, "Direções", directions, "DIRECTIONS"),
                        ],
                        spacing=12,
                    ),
                ]
            ),
        ],
        spacing=0,
        expand=True,
    )

import datetime as dt

import flet as ft

from data.mock_data import TIME_SLOTS
from ui import components as ui
from ui import theme

WEEKDAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MONTHS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
MODES = [("Vídeo", "VIDEOCAM"), ("Chamada", "CALL"), ("Presencial", "PERSON_PIN_CIRCLE")]
AVATAR_COLORS = [theme.PRIMARY, theme.PURPLE, theme.PINK, theme.ORANGE]


def next_days(n=7, start: dt.date | None = None):
    start = start or dt.date.today()
    days = [start + dt.timedelta(days=i + 1) for i in range(n)]
    return [(WEEKDAYS[d.weekday()], d.day, f"{WEEKDAYS[d.weekday()]}, {d.day} {MONTHS[d.month - 1]}") for d in days]


def doctor_card(app, d, index=0) -> ft.Control:
    return ui.card(
        app,
        ft.Row(
            [
                ft.Stack(
                    [
                        ui.avatar(d["initials"], AVATAR_COLORS[index % len(AVATAR_COLORS)], size=56),
                        ft.Container(
                            width=14, height=14, border_radius=7, right=0, bottom=2,
                            bgcolor=theme.ACCENT if d["online"] else app.c.muted, border=ft.Border.all(2, app.c.card),
                        ),
                    ],
                    width=56,
                    height=56,
                ),
                ft.Column(
                    [
                        ui.txt(app, d["name"], 15, ft.FontWeight.BOLD),
                        ui.muted(app, f"{d['specialty']} · {d['years']} anos exp.", 12),
                        ft.Row([ui.rating(app, d["rating"], d["reviews"]), ui.tag(app, d["price"], theme.PRIMARY)], spacing=8),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=app.c.muted),
            ],
            spacing=12,
        ),
        on_click=lambda e: app.push(booking, d["id"]),
        accent=AVATAR_COLORS[index % len(AVATAR_COLORS)],
    )


def build(app) -> ft.Control:
    return ft.Column(
        [
            ui.hero(app, "Médicos disponíveis", "Teleconsulta por vídeo ou chamada", key="doctors"),
            ui.scroll_body([doctor_card(app, d, i) for i, d in enumerate(app.store.doctors)], spacing=12),
        ],
        spacing=0,
        expand=True,
    )


def booking(app, doctor_id) -> ft.Control:
    d = app.store.get_doctor(doctor_id)
    idx = app.store.doctors.index(d)
    days = next_days()
    state = {"date": days[0][2], "time": None, "mode": "Vídeo"}
    dates_row = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=10)
    times_row = ft.Row(wrap=True, spacing=8, run_spacing=8)
    modes_row = ft.Row(spacing=8, wrap=True)

    def date_tile(wd, day, label):
        on = state["date"] == label
        return ft.Container(
            width=62,
            padding=ft.Padding.symmetric(vertical=12),
            border_radius=18,
            bgcolor=None if on else ui.tint(theme.PURPLE, 0.07),
            gradient=ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=theme.GRADIENTS["doctors"]) if on else None,
            border=ft.Border.all(1, theme.PURPLE if on else ui.tint(theme.PURPLE, 0.3)),
            shadow=ft.BoxShadow(blur_radius=14, color=ui.tint(theme.PURPLE, 0.4), offset=ft.Offset(0, 5)) if on else None,
            on_click=lambda e: set_state("date", label),
            content=ft.Column(
                [
                    ft.Text(wd, size=app.fs(12), color=ft.Colors.WHITE if on else app.c.muted),
                    ft.Text(str(day), size=app.fs(20), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if on else app.c.text),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
        )

    def taken(t):
        return any(
            a["doctor_id"] == doctor_id and a["date"] == state["date"] and a["time"] == t and a["status"] != "Cancelada"
            for a in app.store.appointments
        )

    def fill():
        dates_row.controls = [date_tile(*x) for x in days]
        times_row.controls = [
            ui.pill(app, t, selected=state["time"] == t, color=theme.PINK, leading="SCHEDULE", on_click=lambda e, t=t: set_state("time", t))
            if not taken(t)
            else ft.Container(
                content=ft.Text(t, size=app.fs(13), color=app.c.muted, style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10), border_radius=30, bgcolor=app.c.border,
            )
            for t in TIME_SLOTS
        ]
        modes_row.controls = [
            ui.pill(app, m, selected=state["mode"] == m, leading=ic, color=theme.PURPLE, on_click=lambda e, m=m: set_state("mode", m))
            for m, ic in MODES
        ]

    def set_state(k, v):
        state[k] = v
        if k == "date":
            state["time"] = None
        fill()
        app.page.update()

    def confirm(e):
        if not state["time"]:
            app.toast("Escolha um horário.", theme.WARNING)
            return
        try:
            app.store.book(doctor_id, state["date"], state["time"], state["mode"])
        except ValueError as err:
            app.toast(str(err), theme.DANGER)
            return

        def close(e):
            app.page.pop_dialog()
            app.go_tab("appointments")

        app.page.show_dialog(
            ft.AlertDialog(
                icon=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=theme.ACCENT, size=56),
                title=ft.Text("Consulta marcada!", text_align=ft.TextAlign.CENTER),
                content=ft.Text(
                    f"{d['name']}\n{state['date']} às {state['time']} · {state['mode']}",
                    text_align=ft.TextAlign.CENTER,
                ),
                actions=[ft.FilledButton("Ver as minhas consultas", on_click=close, style=ft.ButtonStyle(bgcolor=theme.PRIMARY))],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                shape=ft.RoundedRectangleBorder(radius=24),
            )
        )

    fill()
    return ft.Column(
        [
            ui.hero(app, "Marcar consulta", "Escolha o tipo, o dia e a hora", key="doctors"),
            ui.scroll_body(
                [
                    ui.card(
                        app,
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ui.avatar(d["initials"], AVATAR_COLORS[idx % len(AVATAR_COLORS)], size=64),
                                        ft.Column(
                                            [
                                                ui.txt(app, d["name"], 17, ft.FontWeight.BOLD),
                                                ui.muted(app, d["specialty"]),
                                                ui.rating(app, d["rating"], d["reviews"]),
                                            ],
                                            spacing=3,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=14,
                                ),
                                ft.Row(
                                    [
                                        _stat(app, f"{d['years']}+", "anos"),
                                        _stat(app, str(d["reviews"]), "avaliações"),
                                        _stat(app, d["price"], "consulta"),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                ft.Row([ui.tag(app, lang, theme.INFO, "TRANSLATE") for lang in d["languages"]], spacing=6),
                            ],
                            spacing=14,
                        ),
                    ),
                    ui.txt(app, "Tipo de consulta", 16, ft.FontWeight.BOLD),
                    modes_row,
                    ui.txt(app, "Escolha o dia", 16, ft.FontWeight.BOLD),
                    dates_row,
                    ui.txt(app, "Horários disponíveis", 16, ft.FontWeight.BOLD),
                    times_row,
                    ft.Row([ui.primary_button(app, "Confirmar marcação", confirm, "EVENT_AVAILABLE", color=theme.PURPLE)]),
                ]
            ),
        ],
        spacing=0,
        expand=True,
    )


def _stat(app, value, label):
    return ft.Column(
        [ui.txt(app, value, 16, ft.FontWeight.BOLD, color=theme.PRIMARY), ui.muted(app, label, 11)],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

import flet as ft

from data.mock_data import SYMPTOMS
from services import triage
from ui import components as ui
from ui import theme

DURATIONS = [(1, "Hoje"), (2, "1–2 dias"), (3, "3+ dias")]


def build(app) -> ft.Control:
    selected: set[str] = set()
    state = {"days": 1}
    result_box = ft.Container()
    counter = ui.muted(app, "0 selecionados", 12)

    def chip(s):
        on = s["id"] in selected
        color = theme.DANGER if s["red_flag"] else theme.PRIMARY
        return ui.pill(app, s["label"], selected=on, color=color, leading=s["icon"], on_click=lambda e, sid=s["id"]: toggle(sid))

    chips = ft.Row(wrap=True, spacing=8, run_spacing=8)
    days_row = ft.Row(spacing=8)

    def fill():
        chips.controls = [chip(s) for s in SYMPTOMS]
        days_row.controls = [
            ui.pill(app, label, selected=state["days"] == d, color=theme.ORANGE, leading="SCHEDULE", on_click=lambda e, d=d: set_days(d))
            for d, label in DURATIONS
        ]
        counter.value = f"{len(selected)} selecionado(s)"

    def refresh():
        fill()
        app.page.update()

    def toggle(sid):
        selected.symmetric_difference_update({sid})
        result_box.content = None
        refresh()

    def set_days(d):
        state["days"] = d
        refresh()

    def evaluate(e):
        if not selected:
            app.toast("Selecione pelo menos um sintoma.", theme.WARNING)
            return
        r = triage.evaluate(list(selected), age=app.store.user["age"], days=state["days"])
        result_box.content = result_card(app, r)
        app.page.update()

    fill()

    return ft.Column(
        [
            ui.hero(app, "Verificar sintomas", "Responda em menos de 1 minuto", key="symptoms"),
            ui.scroll_body(
                [
                    ui.card(
                        app,
                        ft.Row(
                            [
                                ui.icon_badge("TIPS_AND_UPDATES", theme.INFO, size=40, icon_size=20),
                                ui.muted(app, "Os sintomas a vermelho são sinais de alarme. Se tiver algum, procure ajuda imediatamente.", 12, expand=True),
                            ],
                            spacing=12,
                        ),
                        bgcolor=ui.tint(theme.INFO, 0.08),
                    ),
                    ft.Row([ui.txt(app, "1. O que está a sentir?", 16, ft.FontWeight.BOLD), counter], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    chips,
                    ui.txt(app, "2. Há quanto tempo?", 16, ft.FontWeight.BOLD),
                    days_row,
                    ft.Row([ui.primary_button(app, "Avaliar sintomas", evaluate, "MONITOR_HEART", color="#E11D48")]),
                    result_box,
                ]
            ),
        ],
        spacing=0,
        expand=True,
    )


def result_card(app, r: triage.TriageResult) -> ft.Control:
    from ui.screens import doctors, facilities  # evita import circular

    color = theme.LEVEL_COLORS[r.level]
    level_label = {"baixo": "Risco baixo", "moderado": "Risco moderado", "alto": "Risco alto", "emergencia": "Emergência"}[r.level]
    target = app.store.nearest(r.facility_type)

    actions = []
    if r.level == triage.EMERGENCY:
        actions.append(ft.Row([ui.primary_button(app, "Ligar 112 agora", lambda e: app.call("112"), "CALL", theme.DANGER)]))
    if target:
        actions.append(ft.Row([ui.secondary_button(app, f"Ir a: {target['name']}", lambda e: app.push(facilities.detail, target["id"]), "NEAR_ME", color)]))
    if r.level in (triage.MEDIUM, triage.HIGH):
        actions.append(ft.Row([ui.secondary_button(app, "Falar com um médico", lambda e: app.push(doctors.build), "VIDEOCAM", theme.PURPLE)]))

    body = [
        ft.Row(
            [
                ui.icon_badge("WARNING_ROUNDED" if r.level in ("alto", "emergencia") else "VERIFIED_USER", color, size=52, icon_size=28),
                ft.Column([ui.tag(app, level_label, color), ui.txt(app, r.title, 18, ft.FontWeight.BOLD)], spacing=4, expand=True),
            ],
            spacing=12,
        ),
        ui.muted(app, r.advice, 14),
    ]
    if r.conditions:
        body.append(ui.txt(app, "Possíveis causas a considerar", 14, ft.FontWeight.BOLD))
        body += [
            ft.Row([ft.Icon(ft.Icons.CIRCLE, size=8, color=color), ui.txt(app, c, 13, expand=True)], spacing=8)
            for c in r.conditions
        ]
    body += actions
    body.append(ui.muted(app, "Esta avaliação é apenas orientativa e não substitui um diagnóstico médico.", 11, italic=True))

    return ft.Container(
        content=ft.Column(body, spacing=12),
        padding=18,
        border_radius=22,
        bgcolor=app.c.card,
        border=ft.Border.all(2, color),
        animate_opacity=300,
    )

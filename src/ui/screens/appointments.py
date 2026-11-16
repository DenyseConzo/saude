import asyncio

import flet as ft

from ui import components as ui
from ui import theme
from ui.screens import doctors

STATUS_COLORS = {"Confirmada": theme.ACCENT, "Cancelada": theme.DANGER}


def build(app) -> ft.Control:
    s = app.store
    upcoming = s.upcoming()
    past = [a for a in s.appointments if a["status"] != "Confirmada"]

    def cancel(appt_id):
        def do(e):
            app.page.pop_dialog()
            s.cancel(appt_id)
            app.toast("Consulta cancelada.", theme.DANGER)
            app.render()

        app.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Cancelar consulta?"),
                content=ft.Text("Pode voltar a marcar a qualquer momento."),
                actions=[
                    ft.TextButton("Manter", on_click=lambda e: app.page.pop_dialog()),
                    ft.FilledButton("Cancelar consulta", on_click=do, style=ft.ButtonStyle(bgcolor=theme.DANGER)),
                ],
                shape=ft.RoundedRectangleBorder(radius=24),
            )
        )

    def appt_card(a):
        d = s.get_doctor(a["doctor_id"])
        active = a["status"] == "Confirmada"
        buttons = []
        if active:
            buttons = [
                ft.Row(
                    [
                        ui.secondary_button(app, "Cancelar", lambda e, i=a["id"]: cancel(i), color=theme.DANGER, height=44),
                        ui.primary_button(
                            app,
                            "Entrar" if a["mode"] != "Presencial" else "Detalhes",
                            lambda e, a=a: app.push(call_screen, a["id"]) if a["mode"] != "Presencial" else app.toast("Apresente-se 15 min antes."),
                            "VIDEOCAM" if a["mode"] == "Vídeo" else "CALL",
                            height=44,
                        ),
                    ],
                    spacing=10,
                )
            ]
        return ui.card(
            app,
            ft.Column(
                [
                    ft.Row(
                        [
                            ui.avatar(d["initials"], size=48),
                            ft.Column([ui.txt(app, d["name"], 15, ft.FontWeight.BOLD), ui.muted(app, d["specialty"], 12)], spacing=2, expand=True),
                            ui.tag(app, a["status"], STATUS_COLORS.get(a["status"], theme.INFO)),
                        ],
                        spacing=12,
                    ),
                    ft.Container(
                        padding=12,
                        border_radius=14,
                        bgcolor=ui.tint(theme.PURPLE, 0.08),
                        content=ft.Row(
                            [
                                ft.Row([ft.Icon(ft.Icons.EVENT_ROUNDED, size=16, color=theme.PURPLE), ui.txt(app, a["date"], 13, ft.FontWeight.W_600)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color=theme.PINK), ui.txt(app, a["time"], 13, ft.FontWeight.W_600)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, size=16, color=theme.INDIGO), ui.txt(app, a["mode"], 13, ft.FontWeight.W_600)], spacing=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                    *buttons,
                ],
                spacing=12,
            ),
            opacity=1 if active else 0.65,
        )

    controls = [ui.section(app, f"Próximas ({len(upcoming)})")]
    if upcoming:
        controls += [appt_card(a) for a in upcoming]
    else:
        controls.append(
            ui.card(
                app,
                ft.Column(
                    [
                        ui.gradient_tile("EVENT_BUSY", theme.GRADIENTS["appointments"]),
                        ui.txt(app, "Sem consultas marcadas", 15, ft.FontWeight.BOLD),
                        ui.muted(app, "Fale com um médico sem sair de casa.", 13),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=24,
            )
        )
    controls.append(ft.Row([ui.primary_button(app, "Marcar nova consulta", lambda e: app.push(doctors.build), "ADD_ROUNDED", color=theme.PURPLE)]))
    controls.append(ui.section(app, "Médicos em destaque", "Ver todos", lambda e: app.push(doctors.build)))
    controls += [doctors.doctor_card(app, d, i) for i, d in enumerate(s.doctors[:2])]
    if past:
        controls.append(ui.section(app, "Histórico"))
        controls += [appt_card(a) for a in past]

    return ft.Column(
        [ui.hero(app, "Consultas", "Telemedicina e acompanhamento", key="appointments", back=False), ui.scroll_body(controls, spacing=12)],
        spacing=0,
        expand=True,
    )


def call_screen(app, appt_id) -> ft.Control:
    """Simulação de uma teleconsulta (sem vídeo real)."""
    a = next(x for x in app.store.appointments if x["id"] == appt_id)
    d = app.store.get_doctor(a["doctor_id"])
    status = ft.Text("A ligar…", color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), size=app.fs(14))
    muted = {"mic": False, "cam": False}

    async def connect():
        await asyncio.sleep(2)
        status.value = "Ligado · 00:01"
        try:
            status.update()
        except Exception:
            pass

    app.page.run_task(connect)

    def round_btn(icon, color, on_click, tooltip):
        return ft.IconButton(
            icon, icon_color=ft.Colors.WHITE, icon_size=26, tooltip=tooltip, on_click=on_click,
            style=ft.ButtonStyle(bgcolor=color, padding=18, shape=ft.CircleBorder()),
        )

    def toggle(e, key, on_icon, off_icon):
        muted[key] = not muted[key]
        e.control.icon = off_icon if muted[key] else on_icon
        e.control.update()

    def hang_up(e):
        app.toast("Chamada terminada. Obrigado por usar a Saúde Fácil!")
        app.back()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER, colors=["#134E4A", "#0B1220"]),
        padding=24,
        content=ft.Column(
            [
                ft.Container(height=40),
                ft.Container(
                    content=ui.avatar(d["initials"], size=130),
                    border_radius=80,
                    border=ft.Border.all(6, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
                    shadow=ft.BoxShadow(blur_radius=50, color=ft.Colors.with_opacity(0.4, theme.PRIMARY)),
                ),
                ft.Text(d["name"], size=app.fs(24), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(d["specialty"], color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=app.fs(14)),
                status,
                ft.Container(expand=True),
                ft.Row(
                    [
                        round_btn(ft.Icons.MIC_ROUNDED, ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                                  lambda e: toggle(e, "mic", ft.Icons.MIC_ROUNDED, ft.Icons.MIC_OFF_ROUNDED), "Microfone"),
                        round_btn(ft.Icons.CALL_END_ROUNDED, theme.DANGER, hang_up, "Desligar"),
                        round_btn(ft.Icons.VIDEOCAM_ROUNDED, ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                                  lambda e: toggle(e, "cam", ft.Icons.VIDEOCAM_ROUNDED, ft.Icons.VIDEOCAM_OFF_ROUNDED), "Câmara"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

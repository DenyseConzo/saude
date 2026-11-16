import flet as ft

from data.mock_data import ONBOARDING
from ui import components as ui
from ui import theme


SLIDE_GRADIENTS = [theme.GRADIENTS["home"], theme.GRADIENTS["assistant"], theme.GRADIENTS["doctors"]]


def build(app) -> ft.Control:
    step = getattr(app, "onboarding_step", 0)
    slide = ONBOARDING[step]
    last = step == len(ONBOARDING) - 1
    colors = SLIDE_GRADIENTS[step % len(SLIDE_GRADIENTS)]

    def go(i):
        app.onboarding_step = i
        app.render()

    def finish(e=None):
        app.store.onboarded = True
        app.onboarding_step = 0
        app.render()

    dots = ft.Row(
        [
            ft.Container(
                width=26 if i == step else 8,
                height=8,
                border_radius=4,
                bgcolor=colors[-1] if i == step else app.c.border,
                animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
            )
            for i in range(len(ONBOARDING))
        ],
        spacing=6,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    illustration = ft.Container(
        content=ft.Stack(
            [
                ft.Container(width=240, height=240, border_radius=120, bgcolor=ui.tint(colors[-1], 0.1)),
                ft.Container(
                    width=170, height=170, border_radius=85, left=35, top=35,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                        colors=colors,
                    ),
                    shadow=ft.BoxShadow(blur_radius=40, color=ui.tint(colors[-1], 0.45), offset=ft.Offset(0, 14)),
                    content=ui.logo(white=True, height=96) if step == 0 else ft.Icon(ui.icon(slide["icon"]), size=80, color=ft.Colors.WHITE),
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            width=240,
            height=240,
        ),
        alignment=ft.Alignment.CENTER,
    )

    return ft.Container(
        padding=24,
        bgcolor=app.c.bg,
        expand=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row([ui.logo(height=34), ui.txt(app, "Saúde Fácil", 16, ft.FontWeight.BOLD)], spacing=8),
                        ft.TextButton(content=ui.muted(app, "Saltar", 14), on_click=finish, visible=not last),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(expand=True),
                illustration,
                ft.Container(height=32),
                ui.txt(app, slide["title"], 26, ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ui.muted(app, slide["body"], 15, text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                dots,
                ft.Container(expand=True),
                ft.Row(
                    [
                        ui.primary_button(
                            app,
                            "Começar" if last else "Continuar",
                            on_click=finish if last else (lambda e: go(step + 1)),
                            icon_name="ARROW_FORWARD_ROUNDED",
                            color=colors[-1],
                        )
                    ]
                ),
                ft.TextButton(
                    content=ui.muted(app, "Voltar", 13),
                    on_click=lambda e: go(step - 1),
                    visible=step > 0,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

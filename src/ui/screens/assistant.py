import asyncio

import flet as ft

from services import assistant as bot
from ui import components as ui
from ui import theme
from ui.screens import doctors, symptoms

CHIP_COLORS = [theme.INDIGO, theme.PINK, theme.INFO, theme.ORANGE, theme.PRIMARY]

# Sugestões que levam diretamente a outro ecrã em vez de gerar resposta.
SHORTCUTS = {
    "Avaliar sintomas": lambda app: app.push(symptoms.build),
    "Ver unidades": lambda app: app.go_tab("facilities"),
    "Ver hospitais perto": lambda app: app.go_tab("facilities"),
    "Ver médicos": lambda app: app.push(doctors.build),
    "Marcar consulta": lambda app: app.push(doctors.build),
    "Ligar 112": lambda app: app.call("112"),
}


def build(app) -> ft.Control:
    if not app.chat:
        app.chat.append({"role": "bot", "text": bot.WELCOME.text, "suggestions": bot.WELCOME.suggestions})

    messages = ft.ListView(expand=True, spacing=10, padding=16, auto_scroll=True)
    suggestions = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=8)
    field = ft.TextField(
        hint_text="Escreva a sua mensagem…",
        border_radius=24,
        filled=True,
        fill_color=app.c.card,
        border_color=app.c.border,
        focused_border_color=theme.INDIGO,
        content_padding=ft.Padding.symmetric(horizontal=18, vertical=12),
        text_size=app.fs(14),
        color=app.c.text,
        expand=True,
        shift_enter=True,
    )

    def bubble(m):
        is_user = m["role"] == "user"
        content = ft.Container(
            content=ft.Text(m["text"], size=app.fs(14), color=ft.Colors.WHITE if is_user else app.c.text, selectable=True),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            bgcolor=None if is_user else app.c.card,
            gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=theme.GRADIENTS["assistant"]) if is_user else None,
            border=None if is_user else ft.Border.all(1, app.c.border),
            border_radius=ft.BorderRadius.only(
                top_left=18, top_right=18, bottom_left=4 if not is_user else 18, bottom_right=4 if is_user else 18
            ),
        )
        # A Column dá largura "solta" ao balão: o texto quebra linha e o balão encolhe ao conteúdo.
        column = ft.Column(
            [content],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.END if is_user else ft.CrossAxisAlignment.START,
        )
        side = ft.Container(width=40) if is_user else ui.gradient_tile("SMART_TOY", theme.GRADIENTS["home"], size=32, icon_size=18, radius=16)
        return ft.Row([side, column], spacing=8, vertical_alignment=ft.CrossAxisAlignment.END)

    def show_suggestions(items):
        suggestions.controls = [
            ui.pill(app, s, on_click=lambda e, s=s: on_suggestion(s), color=CHIP_COLORS[i % len(CHIP_COLORS)],
                    leading="AUTO_AWESOME" if s in SHORTCUTS else None)
            for i, s in enumerate(items)
        ]

    def typing():
        return ft.Row(
            [
                ui.icon_badge("SMART_TOY", theme.PRIMARY, size=32, icon_size=18, radius=16),
                ft.Container(
                    content=ft.Row([ft.ProgressRing(width=14, height=14, stroke_width=2, color=theme.PRIMARY), ui.muted(app, "A escrever…", 13)], spacing=8, tight=True),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    bgcolor=app.c.card,
                    border_radius=18,
                ),
            ],
            spacing=8,
        )

    async def send(text):
        text = (text or "").strip()
        if not text:
            return
        msg = {"role": "user", "text": text}
        app.chat.append(msg)
        messages.controls.append(bubble(msg))
        field.value = ""
        suggestions.controls = []
        indicator = typing()
        messages.controls.append(indicator)
        app.page.update()

        await asyncio.sleep(0.9)
        r = bot.reply(text)
        answer = {"role": "bot", "text": r.text, "suggestions": r.suggestions}
        app.chat.append(answer)
        messages.controls.remove(indicator)
        messages.controls.append(bubble(answer))
        show_suggestions(r.suggestions)
        app.page.update()

    def on_suggestion(s):
        if s in SHORTCUTS:
            SHORTCUTS[s](app)
        else:
            app.page.run_task(send, s)

    async def on_send(e):
        await send(field.value)

    field.on_submit = on_send
    messages.controls = [bubble(m) for m in app.chat]
    show_suggestions(app.chat[-1].get("suggestions", []))

    def clear(e):
        app.chat.clear()
        app.render()

    top = ft.Container(
        padding=ft.Padding.only(left=16, right=12, top=14, bottom=14),
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=theme.GRADIENTS["assistant"]),
        border_radius=ft.BorderRadius.only(bottom_left=24, bottom_right=24),
        content=ft.Row(
            [
                ft.Stack(
                    [
                        ft.Container(ui.logo(white=True, height=30), width=48, height=48, border_radius=24, alignment=ft.Alignment.CENTER,
                                     bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                        ft.Container(width=13, height=13, border_radius=7, bgcolor=theme.ACCENT, right=0, bottom=0, border=ft.Border.all(2, ft.Colors.WHITE)),
                    ],
                    width=48,
                    height=48,
                ),
                ft.Column(
                    [
                        ft.Text("Fácil · Assistente", size=app.fs(18), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("● Online · responde na hora", size=app.fs(12), color="#BBF7D0"),
                    ],
                    spacing=0,
                    expand=True,
                ),
                ft.IconButton(ft.Icons.REFRESH_ROUNDED, icon_color=ft.Colors.WHITE, tooltip="Nova conversa", on_click=clear,
                              style=ft.ButtonStyle(bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE))),
            ],
            spacing=12,
        ),
    )

    disclaimer = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=14, color=app.c.muted), ui.muted(app, "Orientação informativa. Não substitui consulta médica.", 11)],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(bottom=4),
    )

    composer = ft.Container(
        padding=ft.Padding.only(left=12, right=12, bottom=10, top=6),
        content=ft.Row(
            [
                ft.IconButton(
                    ft.Icons.MIC_ROUNDED,
                    icon_color=theme.PINK,
                    tooltip="Falar (em breve)",
                    on_click=lambda e: app.toast("🎙️ Assistente por voz e línguas nacionais — em breve!"),
                    style=ft.ButtonStyle(bgcolor=ui.tint(theme.PINK)),
                ),
                field,
                ft.IconButton(
                    ft.Icons.SEND_ROUNDED,
                    icon_color=ft.Colors.WHITE,
                    on_click=on_send,
                    tooltip="Enviar",
                    style=ft.ButtonStyle(bgcolor=theme.INDIGO),
                ),
            ],
            spacing=8,
        ),
    )

    return ft.Column(
        [
            top,
            messages,
            ft.Container(suggestions, padding=ft.Padding.symmetric(horizontal=12)),
            composer,
            disclaimer,
        ],
        spacing=0,
        expand=True,
    )

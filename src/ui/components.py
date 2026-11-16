"""Componentes reutilizáveis com o estilo visual da Saúde Fácil."""

import flet as ft

from ui import theme


def icon(name: str) -> ft.IconData:
    """Converte o nome guardado nos dados mock (ex.: "WATER_DROP") num ícone."""
    return getattr(ft.Icons, name, ft.Icons.HEALTH_AND_SAFETY)


def tint(color: str, opacity: float = 0.12) -> str:
    return ft.Colors.with_opacity(opacity, color)


def txt(app, value, size=14, weight=None, color=None, **kw) -> ft.Text:
    return ft.Text(value, size=app.fs(size), weight=weight, color=color or app.c.text, **kw)


def muted(app, value, size=13, **kw) -> ft.Text:
    return ft.Text(value, size=app.fs(size), color=app.c.muted, **kw)


def _hovering(e) -> bool:
    return e.data in (True, "true")


def card(app, content, on_click=None, padding=16, bgcolor=None, accent=theme.PRIMARY, **kw) -> ft.Container:
    """Cartão; quando é clicável, cresce ligeiramente e ganha a cor de destaque ao passar o rato/tocar."""
    c = ft.Container(
        content=content,
        padding=padding,
        bgcolor=bgcolor or app.c.card,
        border_radius=20,
        border=ft.Border.all(1, app.c.border),
        on_click=on_click,
        ink=on_click is not None,
        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
        **kw,
    )
    if on_click:
        c.animate_scale = ft.Animation(180, ft.AnimationCurve.EASE_OUT)

        def hover(e):
            on = _hovering(e)
            c.scale = 1.02 if on else 1
            c.border = ft.Border.all(1.5 if on else 1, accent if on else app.c.border)
            c.shadow = ft.BoxShadow(
                blur_radius=24 if on else 14,
                color=ft.Colors.with_opacity(0.25 if on else 0.06, accent if on else ft.Colors.BLACK),
                offset=ft.Offset(0, 8 if on else 4),
            )
            c.update()

        c.on_hover = hover
    return c


def hero(app, title, subtitle=None, key="home", back=True, actions=None, extra=None) -> ft.Container:
    """Cabeçalho colorido em gradiente com círculos decorativos."""
    colors = theme.GRADIENTS.get(key, theme.GRADIENTS["home"])
    row = []
    if back:
        row.append(
            ft.IconButton(
                ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.Colors.WHITE,
                icon_size=18,
                on_click=lambda e: app.back(),
                tooltip="Voltar",
                style=ft.ButtonStyle(bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), shape=ft.CircleBorder()),
            )
        )
    col = [ft.Text(title, size=app.fs(22), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)]
    if subtitle:
        col.append(ft.Text(subtitle, size=app.fs(13), color=ft.Colors.WHITE, opacity=0.88))
    row.append(ft.Column(col, spacing=0, expand=True))
    row += actions or []
    body = [ft.Row(row, vertical_alignment=ft.CrossAxisAlignment.CENTER)]
    if extra:
        body.append(extra)
    return ft.Container(
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=colors),
        border_radius=ft.BorderRadius.only(bottom_left=28, bottom_right=28),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        margin=ft.Margin.only(bottom=12),
        content=ft.Stack(
            [
                ft.Container(width=160, height=160, border_radius=80, right=-50, top=-60, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                ft.Container(width=90, height=90, border_radius=45, right=70, bottom=-50, bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                ft.Container(
                    content=ft.Column(body, spacing=14),
                    padding=ft.Padding.only(left=12 if back else 20, right=16, top=16, bottom=22),
                ),
            ]
        ),
    )


def gradient_tile(icon_name, colors, size=58, icon_size=28, radius=18) -> ft.Container:
    return ft.Container(
        content=ft.Icon(icon(icon_name), color=ft.Colors.WHITE, size=icon_size),
        width=size,
        height=size,
        border_radius=radius,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=colors),
        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.35, colors[-1]), offset=ft.Offset(0, 6)),
        alignment=ft.Alignment.CENTER,
    )


def logo(white=False, height=36) -> ft.Image:
    return ft.Image(src="logo_mark_white.png" if white else "logo_mark.png", height=height, fit=ft.BoxFit.CONTAIN)


def icon_badge(name, color, size=44, icon_size=22, radius=14) -> ft.Container:
    return ft.Container(
        content=ft.Icon(icon(name) if isinstance(name, str) else name, color=color, size=icon_size),
        width=size,
        height=size,
        border_radius=radius,
        bgcolor=tint(color),
        alignment=ft.Alignment.CENTER,
    )


def avatar(initials: str, color=theme.PRIMARY, size=48) -> ft.Container:
    return ft.Container(
        content=ft.Text(initials, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=size * 0.36),
        width=size,
        height=size,
        border_radius=size / 2,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=[color, theme.PRIMARY_DARK]
        ),
        alignment=ft.Alignment.CENTER,
    )


def section(app, title, action=None, on_action=None) -> ft.Row:
    controls = [txt(app, title, 17, ft.FontWeight.BOLD)]
    if action:
        controls.append(
            ft.TextButton(
                content=ft.Text(action, size=app.fs(13), color=theme.PRIMARY, weight=ft.FontWeight.W_600),
                on_click=on_action,
            )
        )
    return ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


def pill(app, label, selected=False, on_click=None, color=theme.PRIMARY, leading=None, data=None) -> ft.Container:
    row = [ft.Text(label, size=app.fs(13), weight=ft.FontWeight.W_600, color=ft.Colors.WHITE if selected else app.c.text)]
    if leading:
        row.insert(0, ft.Icon(icon(leading), size=16, color=ft.Colors.WHITE if selected else color))
    p = ft.Container(
        content=ft.Row(row, spacing=6, tight=True),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=30,
        bgcolor=None if selected else tint(color, 0.08),
        gradient=ft.LinearGradient(colors=[color, ft.Colors.with_opacity(0.8, color)]) if selected else None,
        border=ft.Border.all(1, color if selected else tint(color, 0.35)),
        shadow=ft.BoxShadow(blur_radius=10, color=tint(color, 0.35), offset=ft.Offset(0, 3)) if selected else None,
        on_click=on_click,
        data=data,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )
    if on_click:
        def hover(e):
            p.scale = 1.05 if _hovering(e) else 1
            p.update()

        p.on_hover = hover
    return p


def primary_button(app, text, on_click=None, icon_name=None, color=theme.PRIMARY, expand=True, height=54):
    return ft.FilledButton(
        content=ft.Text(text, size=app.fs(15), weight=ft.FontWeight.W_600),
        icon=icon(icon_name) if icon_name else None,
        on_click=on_click,
        expand=expand,
        height=height,
        style=ft.ButtonStyle(
            bgcolor=color,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        ),
    )


def secondary_button(app, text, on_click=None, icon_name=None, color=theme.PRIMARY, expand=True, height=54):
    return ft.OutlinedButton(
        content=ft.Text(text, size=app.fs(15), weight=ft.FontWeight.W_600, color=color),
        icon=icon(icon_name) if icon_name else None,
        icon_color=color,
        on_click=on_click,
        expand=expand,
        height=height,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=16),
            side=ft.BorderSide(1.5, color),
        ),
    )


def tag(app, label, color=theme.PRIMARY, icon_name=None) -> ft.Container:
    row = [ft.Text(label, size=app.fs(11), weight=ft.FontWeight.W_600, color=color)]
    if icon_name:
        row.insert(0, ft.Icon(icon(icon_name), size=13, color=color))
    return ft.Container(
        content=ft.Row(row, spacing=4, tight=True),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        bgcolor=tint(color),
    )


def header(app, title, subtitle=None, back=True, actions=None) -> ft.Container:
    left = []
    if back:
        left.append(
            ft.IconButton(
                ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=app.c.text,
                icon_size=20,
                on_click=lambda e: app.back(),
                tooltip="Voltar",
                style=ft.ButtonStyle(bgcolor=app.c.card, shape=ft.CircleBorder()),
            )
        )
    col = [txt(app, title, 20, ft.FontWeight.BOLD)]
    if subtitle:
        col.append(muted(app, subtitle, 13))
    left.append(ft.Column(col, spacing=0, expand=True))
    return ft.Container(
        content=ft.Row(left + (actions or []), vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.only(left=12 if back else 16, right=12, top=12, bottom=6),
    )


def scroll_body(controls, padding=16, spacing=16) -> ft.Container:
    return ft.Container(
        content=ft.Column(controls, spacing=spacing, scroll=ft.ScrollMode.AUTO),
        padding=ft.Padding.only(left=padding, right=padding, bottom=padding),
        expand=True,
    )


def rating(app, value, reviews=None) -> ft.Row:
    items = [ft.Icon(ft.Icons.STAR_ROUNDED, color=theme.WARNING, size=16), txt(app, f"{value:.1f}", 12, ft.FontWeight.W_600)]
    if reviews:
        items.append(muted(app, f"({reviews})", 12))
    return ft.Row(items, spacing=3, tight=True)


def info_row(app, icon_name, label, value) -> ft.Row:
    return ft.Row(
        [
            icon_badge(icon_name, theme.PRIMARY, size=38, icon_size=18, radius=12),
            ft.Column([muted(app, label, 12), txt(app, value, 14, ft.FontWeight.W_600)], spacing=0, expand=True),
        ],
        spacing=12,
    )

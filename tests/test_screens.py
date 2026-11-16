"""Testes de fumo: todos os ecrãs constroem-se sem erros com os dados mock."""

import flet as ft
import pytest

from ui.app import TABS
from ui.screens import appointments, doctors, emergency, facilities, onboarding, symptoms
from services import triage


@pytest.mark.parametrize("index", range(len(TABS)))
def test_tabs_render(app, index):
    app.go_tab(index)
    assert isinstance(app.body.content, ft.Control)


@pytest.mark.parametrize("dark, large", [(False, False), (True, True)])
def test_render_with_settings(app, dark, large):
    app.store.dark_mode, app.store.large_text = dark, large
    for i in range(len(TABS)):
        app.go_tab(i)


def test_sub_screens_render(app):
    for builder, args in [
        (symptoms.build, ()),
        (facilities.detail, ("hcm",)),
        (doctors.build, ()),
        (doctors.booking, ("d1",)),
        (emergency.build, ()),
        (appointments.call_screen, ("a1",)),
    ]:
        app.push(builder, *args)
        assert app.body.content is not None
    app.back()
    assert len(app.stack) == 5


def test_onboarding_steps(app):
    app.store.onboarded = False
    for step in range(3):
        app.onboarding_step = step
        assert isinstance(onboarding.build(app), ft.Control)


@pytest.mark.parametrize("ids", [["dor_garganta"], ["febre", "diarreia", "vomitos"], ["dor_peito"]])
def test_result_card(app, ids):
    assert isinstance(symptoms.result_card(app, triage.evaluate(ids)), ft.Control)


def test_next_days_labels():
    import datetime as dt

    days = doctors.next_days(3, start=dt.date(2026, 11, 5))  # quinta-feira
    assert [d[2] for d in days] == ["Sex, 6 Nov", "Sáb, 7 Nov", "Dom, 8 Nov"]


def test_reset_demo(app):
    app.store.book("d2", "Ter, 11 Nov", "11:00")
    app.reset_demo()
    assert len(app.store.appointments) == 1
    assert app.store.onboarded is False

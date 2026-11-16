import pytest

from services import triage


def test_red_flag_is_emergency():
    r = triage.evaluate(["febre", "falta_ar"])
    assert r.level == triage.EMERGENCY
    assert "112" in r.advice


def test_mild_symptom_is_low():
    r = triage.evaluate(["dor_garganta"], age=30, days=1)
    assert r.level == triage.LOW
    assert r.facility_type == "Farmácia"


def test_malaria_suggested_for_fever_and_chills():
    r = triage.evaluate(["febre", "calafrios"], age=30)
    assert any("Malária" in c for c in r.conditions)
    assert r.level == triage.LOW


def test_duration_and_age_raise_level():
    base = triage.evaluate(["febre", "calafrios"], age=30, days=1)
    worse = triage.evaluate(["febre", "calafrios"], age=2, days=3)
    assert worse.score == base.score + 4
    assert worse.level == triage.HIGH


def test_unknown_or_empty_symptoms_raise():
    with pytest.raises(ValueError):
        triage.evaluate([])
    with pytest.raises(ValueError):
        triage.evaluate(["nao_existe"])

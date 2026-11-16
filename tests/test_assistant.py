import pytest

from services import assistant


@pytest.mark.parametrize(
    "message, action",
    [
        ("Tenho FEBRE desde ontem", "triage"),
        ("estou com diarreia", "triage"),
        ("Sinto dor no peito", "emergency"),
        ("onde fica o hospital?", "facilities"),
        ("quero marcar consulta com médico", "doctors"),
    ],
)
def test_intents(message, action):
    assert assistant.reply(message).action == action


def test_accents_are_ignored():
    assert assistant.reply("malária").text == assistant.reply("malaria").text


def test_empty_message_returns_welcome():
    assert assistant.reply("   ") is assistant.WELCOME


def test_unknown_message_falls_back():
    r = assistant.reply("xyzzy")
    assert r is assistant.FALLBACK
    assert r.suggestions

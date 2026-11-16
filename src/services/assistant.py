"""Assistente virtual simulado: respostas por palavras-chave (sem IA real).

A interface é a mesma que um backend de IA usaria (`reply(texto) -> Reply`),
por isso pode ser trocado por um serviço real mais tarde.
"""

import unicodedata
from dataclasses import dataclass, field


@dataclass
class Reply:
    text: str
    suggestions: list[str] = field(default_factory=list)
    action: str | None = None  # "triage", "facilities", "doctors", "emergency"


WELCOME = Reply(
    "Olá! Sou a Fácil, a sua assistente de saúde. 💚\n"
    "Diga-me como se sente ou escolha uma das opções abaixo.",
    ["Tenho febre", "Dor de barriga", "Onde fica o hospital?", "Falar com médico"],
)

_INTENTS = [
    (
        ("dor no peito", "falta de ar", "desmaio", "convuls", "inconsciente", "sangr"),
        Reply(
            "⚠️ Isso pode ser uma emergência. Ligue já para o 112 (emergência) "
            "ou vá à urgência mais próxima. Não espere que os sintomas passem.",
            ["Ver hospitais perto", "Ligar 112"],
            "emergency",
        ),
    ),
    (
        ("febre", "calafrio", "malaria", "paludismo"),
        Reply(
            "A febre é muito comum em casos de malária em Moçambique. 🦟\n"
            "• Faça o teste rápido de malária — é gratuito no centro de saúde.\n"
            "• Beba muitos líquidos e descanse.\n"
            "• Se a febre durar mais de 2 dias, ou for numa criança, procure atendimento hoje.",
            ["Avaliar sintomas", "Centro de saúde perto"],
            "triage",
        ),
    ),
    (
        ("diarreia", "barriga", "vomit", "colera"),
        Reply(
            "Para diarreia ou vómitos, o mais importante é evitar a desidratação. 💧\n"
            "• Tome soro de reidratação oral (SRO) aos poucos.\n"
            "• Beba apenas água fervida ou tratada.\n"
            "• Sangue nas fezes ou sinais de desidratação: vá à unidade sanitária.",
            ["Avaliar sintomas", "Como preparar soro caseiro?"],
            "triage",
        ),
    ),
    (
        ("soro caseiro", "preparar soro"),
        Reply(
            "Soro caseiro: 1 litro de água fervida e arrefecida + 6 colheres de chá "
            "rasas de açúcar + ½ colher de chá de sal. Mexa bem e beba aos goles.",
            ["Obrigado", "Centro de saúde perto"],
        ),
    ),
    (
        ("tosse", "gripe", "constipa", "garganta"),
        Reply(
            "Tosse e dor de garganta costumam ser infeções respiratórias. 😷\n"
            "• Beba líquidos quentes e descanse.\n"
            "• Tosse há mais de 2 semanas, suores à noite ou perda de peso: faça rastreio de tuberculose.",
            ["Avaliar sintomas", "Falar com médico"],
            "triage",
        ),
    ),
    (
        ("hiv", "sida", "preservativo", "teste"),
        Reply(
            "O teste de HIV é gratuito e confidencial em todas as unidades sanitárias públicas. ❤️\n"
            "Se o resultado for positivo, o tratamento antirretroviral também é gratuito.",
            ["Centro de saúde perto"],
            "facilities",
        ),
    ),
    (
        ("gravid", "gestante", "bebe", "prenatal", "pre-natal"),
        Reply(
            "Durante a gravidez faça pelo menos 4 consultas pré-natais. 🤰\n"
            "Sinais de alarme: sangramento, dor de cabeça forte, inchaço súbito ou o bebé deixar de mexer.",
            ["Marcar consulta", "Hospital com maternidade"],
            "doctors",
        ),
    ),
    (
        ("hospital", "centro de saude", "unidade", "perto", "farmacia", "onde fica"),
        Reply(
            "Posso mostrar-lhe as unidades sanitárias mais próximas, com horários e serviços. 📍",
            ["Ver unidades"],
            "facilities",
        ),
    ),
    (
        ("medico", "consulta", "marcar", "doutor", "teleconsulta", "video"),
        Reply(
            "Pode falar com um profissional de saúde por vídeo ou chamada. 👩🏾‍⚕️\n"
            "Veja os médicos disponíveis e marque em poucos toques.",
            ["Ver médicos"],
            "doctors",
        ),
    ),
    (
        ("cabeca", "enxaqueca"),
        Reply(
            "Para dor de cabeça ligeira: descanse num local calmo, beba água e evite ecrãs. 🧠\n"
            "Se vier com febre, procure fazer o teste de malária. "
            "Dor muito forte e súbita ou rigidez no pescoço: vá à urgência.",
            ["Avaliar sintomas", "Tenho febre"],
            "triage",
        ),
    ),
    (
        ("obrigad", "valeu", "estou bem", "certo"),
        Reply("De nada! Estou aqui sempre que precisar. Cuide-se! 💚", ["Tenho outra dúvida"]),
    ),
    (
        ("ola", "bom dia", "boa tarde", "boa noite", "avuxeni", "salama"),
        Reply("Olá! Como se sente hoje?", ["Tenho febre", "Dor de cabeça", "Estou bem"]),
    ),
]

FALLBACK = Reply(
    "Ainda estou a aprender e não percebi bem. 🤔\n"
    "Pode descrever o que sente com outras palavras, ou usar o verificador de sintomas.",
    ["Avaliar sintomas", "Falar com médico"],
    "triage",
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def reply(message: str) -> Reply:
    msg = normalize(message.strip())
    if not msg:
        return WELCOME
    for keywords, answer in _INTENTS:
        if any(k in msg for k in keywords):
            return answer
    return FALLBACK

"""Motor de triagem simplificado (regras locais, sem rede).

Não substitui avaliação médica: serve para orientar o utilizador sobre a
urgência com que deve procurar uma unidade sanitária.
"""

from dataclasses import dataclass, field

from data.mock_data import SYMPTOMS

SYMPTOMS_BY_ID = {s["id"]: s for s in SYMPTOMS}

LOW, MEDIUM, HIGH, EMERGENCY = "baixo", "moderado", "alto", "emergencia"


@dataclass
class TriageResult:
    level: str
    title: str
    advice: str
    facility_type: str
    score: int
    conditions: list[str] = field(default_factory=list)


def _possible_conditions(ids: set[str]) -> list[str]:
    conditions = []
    if "febre" in ids and ({"calafrios", "dor_cabeca", "dor_corpo"} & ids):
        conditions.append("Malária (faça o teste rápido)")
    if "diarreia" in ids and "vomitos" in ids:
        conditions.append("Gastroenterite / risco de cólera")
    elif "diarreia" in ids:
        conditions.append("Infeção intestinal")
    if "tosse" in ids and ("febre" in ids or "dor_garganta" in ids):
        conditions.append("Infeção respiratória")
    if "tosse" in ids and "cansaco" in ids:
        conditions.append("Considere rastreio de tuberculose")
    return conditions


def evaluate(symptom_ids: list[str], age: int | None = None, days: int = 1) -> TriageResult:
    """Avalia a lista de sintomas e devolve o nível de urgência."""
    ids = {s for s in symptom_ids if s in SYMPTOMS_BY_ID}
    if not ids:
        raise ValueError("Selecione pelo menos um sintoma.")

    score = sum(SYMPTOMS_BY_ID[s]["weight"] for s in ids)
    if days >= 3:
        score += 2
    if age is not None and (age < 5 or age >= 65):
        score += 2

    conditions = _possible_conditions(ids)

    if any(SYMPTOMS_BY_ID[s]["red_flag"] for s in ids):
        return TriageResult(
            EMERGENCY,
            "Procure atendimento urgente",
            "Tem sinais de alarme. Ligue 112 ou dirija-se imediatamente à urgência mais próxima.",
            "Hospital",
            score,
            conditions,
        )
    if score >= 7:
        return TriageResult(
            HIGH,
            "Consulte um profissional hoje",
            "Os seus sintomas precisam de avaliação ainda hoje. Vá a um centro de saúde ou marque teleconsulta.",
            "Hospital",
            score,
            conditions,
        )
    if score >= 4:
        return TriageResult(
            MEDIUM,
            "Marque uma consulta",
            "Descanse, beba muitos líquidos e procure um centro de saúde nas próximas 24–48 horas.",
            "Centro de Saúde",
            score,
            conditions,
        )
    return TriageResult(
        LOW,
        "Cuidados em casa",
        "Os sintomas parecem ligeiros. Descanse, hidrate-se e volte a avaliar se piorar.",
        "Farmácia",
        score,
        conditions,
    )

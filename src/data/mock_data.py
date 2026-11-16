"""Dados fictícios (mock) usados pela app Saúde Fácil.

Nenhum destes dados é real: nomes, distâncias, horários e médicos servem
apenas para demonstração e testes da interface.
"""

USER = {
    "name": "Ana Muthemba",
    "first_name": "Ana",
    "age": 29,
    "gender": "Feminino",
    "city": "Maputo",
    "blood_type": "O+",
    "phone": "+258 84 123 4567",
    "allergies": ["Penicilina"],
    "conditions": ["Asma ligeira"],
}

LANGUAGES = ["Português", "Changana", "Macua", "Sena", "Ndau"]

GREETINGS = {
    "Português": "Olá",
    "Changana": "Avuxeni",
    "Macua": "Salama",
    "Sena": "Moni",
    "Ndau": "Mhoro",
}

EMERGENCY_CONTACTS = [
    {"name": "Emergência geral", "number": "112", "icon": "EMERGENCY", "desc": "Ambulância e socorro"},
    {"name": "Alô Vida", "number": "110", "icon": "SUPPORT_AGENT", "desc": "Linha de apoio e aconselhamento"},
    {"name": "Polícia", "number": "119", "icon": "LOCAL_POLICE", "desc": "Segurança pública"},
]

FACILITIES = [
    {
        "id": "hcm",
        "name": "Hospital Central de Maputo",
        "type": "Hospital",
        "address": "Av. Agostinho Neto, Maputo",
        "distance_km": 2.4,
        "open_24h": True,
        "hours": "Aberto 24 horas",
        "phone": "+258 21 000 001",
        "rating": 4.3,
        "wait_min": 55,
        "services": ["Urgência", "Maternidade", "Pediatria", "Cirurgia", "Laboratório"],
    },
    {
        "id": "mavalane",
        "name": "Hospital Geral de Mavalane",
        "type": "Hospital",
        "address": "Bairro de Mavalane, Maputo",
        "distance_km": 5.1,
        "open_24h": True,
        "hours": "Aberto 24 horas",
        "phone": "+258 21 000 002",
        "rating": 4.0,
        "wait_min": 40,
        "services": ["Urgência", "Maternidade", "Laboratório", "Raio-X"],
    },
    {
        "id": "polana",
        "name": "Centro de Saúde da Polana Caniço",
        "type": "Centro de Saúde",
        "address": "Polana Caniço A, Maputo",
        "distance_km": 1.2,
        "open_24h": False,
        "hours": "07:30 – 15:30",
        "phone": "+258 21 000 003",
        "rating": 4.1,
        "wait_min": 25,
        "services": ["Consulta geral", "Vacinação", "Planeamento familiar", "Teste HIV"],
    },
    {
        "id": "altomae",
        "name": "Centro de Saúde do Alto Maé",
        "type": "Centro de Saúde",
        "address": "Av. Eduardo Mondlane, Alto Maé",
        "distance_km": 3.0,
        "open_24h": False,
        "hours": "07:30 – 15:30",
        "phone": "+258 21 000 004",
        "rating": 3.9,
        "wait_min": 30,
        "services": ["Consulta geral", "Vacinação", "Teste de malária", "Nutrição"],
    },
    {
        "id": "matola",
        "name": "Hospital Provincial da Matola",
        "type": "Hospital",
        "address": "Matola Cidade, Matola",
        "distance_km": 12.7,
        "open_24h": True,
        "hours": "Aberto 24 horas",
        "phone": "+258 21 000 005",
        "rating": 4.2,
        "wait_min": 45,
        "services": ["Urgência", "Pediatria", "Maternidade", "Laboratório"],
    },
    {
        "id": "farmacia",
        "name": "Farmácia Saúde Viva",
        "type": "Farmácia",
        "address": "Av. Julius Nyerere, Maputo",
        "distance_km": 0.8,
        "open_24h": False,
        "hours": "08:00 – 21:00",
        "phone": "+258 21 000 006",
        "rating": 4.6,
        "wait_min": 5,
        "services": ["Medicamentos", "Medição de tensão", "Aconselhamento"],
    },
]

DOCTORS = [
    {
        "id": "d1",
        "name": "Dra. Célia Nhantumbo",
        "specialty": "Clínica Geral",
        "rating": 4.9,
        "reviews": 212,
        "years": 11,
        "price": "Gratuito",
        "online": True,
        "languages": ["Português", "Changana"],
        "initials": "CN",
    },
    {
        "id": "d2",
        "name": "Dr. Abel Cossa",
        "specialty": "Pediatria",
        "rating": 4.8,
        "reviews": 158,
        "years": 9,
        "price": "350 MT",
        "online": True,
        "languages": ["Português", "Sena"],
        "initials": "AC",
    },
    {
        "id": "d3",
        "name": "Dra. Fátima Issufo",
        "specialty": "Ginecologia e Obstetrícia",
        "rating": 4.7,
        "reviews": 97,
        "years": 14,
        "price": "500 MT",
        "online": False,
        "languages": ["Português", "Macua"],
        "initials": "FI",
    },
    {
        "id": "d4",
        "name": "Dr. Hélder Macuácua",
        "specialty": "Medicina Interna",
        "rating": 4.6,
        "reviews": 74,
        "years": 7,
        "price": "400 MT",
        "online": True,
        "languages": ["Português"],
        "initials": "HM",
    },
]

TIME_SLOTS = ["08:00", "09:30", "11:00", "13:30", "15:00", "16:30"]

HEALTH_TIPS = [
    {
        "title": "Previna a malária",
        "body": "Durma sempre debaixo de rede mosquiteira tratada e elimine águas paradas perto de casa.",
        "icon": "BUG_REPORT",
        "color": "#0EA5E9",
    },
    {
        "title": "Água segura",
        "body": "Ferva ou trate a água com Certeza antes de beber para evitar cólera e diarreias.",
        "icon": "WATER_DROP",
        "color": "#14B8A6",
    },
    {
        "title": "Vacinas em dia",
        "body": "Confirme o cartão de vacinação das crianças no centro de saúde mais próximo.",
        "icon": "VACCINES",
        "color": "#8B5CF6",
    },
    {
        "title": "Conheça o seu estado",
        "body": "O teste de HIV é gratuito e confidencial em todas as unidades sanitárias públicas.",
        "icon": "FAVORITE",
        "color": "#F43F5E",
    },
]

# Sintomas disponíveis no verificador. "weight" indica a gravidade relativa e
# "red_flag" marca sinais de alarme que exigem atendimento imediato.
SYMPTOMS = [
    {"id": "febre", "label": "Febre", "weight": 2, "red_flag": False, "icon": "THERMOSTAT"},
    {"id": "dor_cabeca", "label": "Dor de cabeça", "weight": 1, "red_flag": False, "icon": "PSYCHOLOGY"},
    {"id": "tosse", "label": "Tosse", "weight": 1, "red_flag": False, "icon": "AIR"},
    {"id": "diarreia", "label": "Diarreia", "weight": 2, "red_flag": False, "icon": "WATER_DROP"},
    {"id": "vomitos", "label": "Vómitos", "weight": 2, "red_flag": False, "icon": "SICK"},
    {"id": "calafrios", "label": "Calafrios", "weight": 1, "red_flag": False, "icon": "AC_UNIT"},
    {"id": "dor_corpo", "label": "Dores no corpo", "weight": 1, "red_flag": False, "icon": "ACCESSIBILITY_NEW"},
    {"id": "cansaco", "label": "Cansaço", "weight": 1, "red_flag": False, "icon": "BEDTIME"},
    {"id": "dor_garganta", "label": "Dor de garganta", "weight": 1, "red_flag": False, "icon": "RECORD_VOICE_OVER"},
    {"id": "falta_ar", "label": "Falta de ar", "weight": 4, "red_flag": True, "icon": "MONITOR_HEART"},
    {"id": "dor_peito", "label": "Dor no peito", "weight": 4, "red_flag": True, "icon": "HEART_BROKEN"},
    {"id": "convulsoes", "label": "Convulsões", "weight": 5, "red_flag": True, "icon": "WARNING"},
    {"id": "confusao", "label": "Confusão mental", "weight": 5, "red_flag": True, "icon": "BLUR_ON"},
    {"id": "sangramento", "label": "Sangramento", "weight": 4, "red_flag": True, "icon": "BLOODTYPE"},
]

INITIAL_APPOINTMENTS = [
    {
        "id": "a1",
        "doctor_id": "d1",
        "date": "Seg, 10 Nov",
        "time": "09:30",
        "mode": "Vídeo",
        "status": "Confirmada",
    },
]

ONBOARDING = [
    {
        "title": "A sua saúde, mais perto de si",
        "body": "Informação médica confiável, em português simples, sempre que precisar.",
        "icon": "HEALTH_AND_SAFETY",
    },
    {
        "title": "Assistente virtual inteligente",
        "body": "Descreva os seus sintomas e receba orientação sobre quando e onde procurar ajuda.",
        "icon": "SMART_TOY",
    },
    {
        "title": "Unidades e médicos perto de si",
        "body": "Encontre a unidade sanitária mais próxima ou fale com um profissional por vídeo.",
        "icon": "LOCAL_HOSPITAL",
    },
]

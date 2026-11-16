from data.mock_data import EMERGENCY_CONTACTS


def test_emergency_numbers():
    numbers = {c["name"]: c["number"] for c in EMERGENCY_CONTACTS}
    assert numbers == {"Emergência geral": "112", "Alô Vida": "110", "Polícia": "119"}

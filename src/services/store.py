"""Estado da aplicação em memória, alimentado pelos dados mock."""

import copy
import itertools

from data import mock_data

FACILITY_TYPES = ["Todos", "Hospital", "Centro de Saúde", "Farmácia"]


class Store:
    def __init__(self):
        self.user = copy.deepcopy(mock_data.USER)
        self.facilities = copy.deepcopy(mock_data.FACILITIES)
        self.doctors = copy.deepcopy(mock_data.DOCTORS)
        self.appointments = copy.deepcopy(mock_data.INITIAL_APPOINTMENTS)
        self.favorites: set[str] = {"polana"}
        self.language = "Português"
        self.large_text = False
        self.dark_mode = False
        self.onboarded = False
        self._ids = itertools.count(len(self.appointments) + 1)

    # ---------- unidades sanitárias ----------
    def search_facilities(self, query: str = "", ftype: str = "Todos", open_now_only: bool = False):
        q = query.strip().lower()
        result = [
            f
            for f in self.facilities
            if (ftype == "Todos" or f["type"] == ftype)
            and (not q or q in f["name"].lower() or any(q in s.lower() for s in f["services"]))
            and (not open_now_only or f["open_24h"])
        ]
        return sorted(result, key=lambda f: f["distance_km"])

    def nearest(self, ftype: str | None = None):
        items = self.search_facilities(ftype=ftype or "Todos")
        return items[0] if items else None

    def get_facility(self, fid: str):
        return next((f for f in self.facilities if f["id"] == fid), None)

    def toggle_favorite(self, fid: str) -> bool:
        if fid in self.favorites:
            self.favorites.remove(fid)
            return False
        self.favorites.add(fid)
        return True

    # ---------- médicos e consultas ----------
    def get_doctor(self, did: str):
        return next((d for d in self.doctors if d["id"] == did), None)

    def book(self, doctor_id: str, date: str, time: str, mode: str = "Vídeo") -> dict:
        if not self.get_doctor(doctor_id):
            raise ValueError("Médico não encontrado.")
        if any(
            a["doctor_id"] == doctor_id and a["date"] == date and a["time"] == time and a["status"] != "Cancelada"
            for a in self.appointments
        ):
            raise ValueError("Esse horário já está ocupado.")
        appt = {
            "id": f"a{next(self._ids)}",
            "doctor_id": doctor_id,
            "date": date,
            "time": time,
            "mode": mode,
            "status": "Confirmada",
        }
        self.appointments.append(appt)
        return appt

    def cancel(self, appt_id: str):
        for a in self.appointments:
            if a["id"] == appt_id:
                a["status"] = "Cancelada"
                return a
        raise ValueError("Consulta não encontrada.")

    def upcoming(self):
        return [a for a in self.appointments if a["status"] == "Confirmada"]

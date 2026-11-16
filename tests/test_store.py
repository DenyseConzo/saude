import pytest

from services.store import Store


def test_facilities_sorted_by_distance():
    items = Store().search_facilities()
    assert [f["distance_km"] for f in items] == sorted(f["distance_km"] for f in items)


def test_facility_filters():
    s = Store()
    assert all(f["type"] == "Hospital" for f in s.search_facilities(ftype="Hospital"))
    assert all(f["open_24h"] for f in s.search_facilities(open_now_only=True))
    assert [f["id"] for f in s.search_facilities("vacina")] == ["polana", "altomae"]
    assert s.search_facilities("nada-disto") == []


def test_nearest_by_type():
    assert Store().nearest("Hospital")["id"] == "hcm"


def test_toggle_favorite():
    s = Store()
    assert s.toggle_favorite("hcm") is True
    assert s.toggle_favorite("hcm") is False


def test_book_and_cancel():
    s = Store()
    before = len(s.upcoming())
    appt = s.book("d2", "Ter, 11 Nov", "11:00", "Chamada")
    assert len(s.upcoming()) == before + 1
    with pytest.raises(ValueError):
        s.book("d2", "Ter, 11 Nov", "11:00")
    s.cancel(appt["id"])
    assert len(s.upcoming()) == before
    # depois de cancelado o horário fica livre outra vez
    s.book("d2", "Ter, 11 Nov", "11:00")


def test_book_unknown_doctor():
    with pytest.raises(ValueError):
        Store().book("zz", "Ter, 11 Nov", "11:00")


def test_stores_are_independent():
    a, b = Store(), Store()
    a.book("d1", "Qua, 12 Nov", "08:00")
    assert len(b.appointments) == 1

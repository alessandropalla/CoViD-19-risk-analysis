from db.utils import Database
import pytest


def db_types():
    return ["confirmed", "deaths", "recovered"]


@pytest.mark.parametrize("db_type", db_types())
def test_files(db_type):
    db = Database(db_type)
    assert db is not None


@pytest.mark.parametrize("db_type", db_types())
def test_country(db_type):
    db = Database(db_type)
    assert len(db.get_countries()) > 0


@pytest.mark.parametrize("db_type", db_types())
def test_patients(db_type):
    db = Database(db_type)
    for country in db.get_countries():
        assert not db.get_patients_by_country(country).empty

from src.models import Perfume


def test_perfume_to_dict():
    perfume = Perfume(
        url="https://test",
        brand="Brand",
        name="Test Perfume",
        price="100",
        rating="4.5",
        description="Aroma",
        instruction="Nanosit na sheyu",
        country="Россия"
    )

    data = perfume.to_dict()

    assert data["url"] == "https://test"
    assert data["brand"] == "Brand"
    assert data["name"] == "Test Perfume"
    assert data["price"] == "100"
    assert data["rating"] == "4.5"
    assert data["description"] == "Aroma"
    assert data["instruction"] == "Nanosit na sheyu"
    assert data["country"] == "Россия"
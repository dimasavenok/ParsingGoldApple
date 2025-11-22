class Perfume:
    def __init__(self, url=None, brand=None, name=None, price=None, rating=None,
                 description=None, instruction=None, country=None):
        self.url = url
        self.brand = brand
        self.name = name
        self.price = price
        self.rating = rating
        self.description = description
        self.instruction = instruction
        self.country = country

    def to_dict(self):
        return {
            "url": self.url,
            "brand": self.brand,
            "name": self.name,
            "price": self.price,
            "rating": self.rating,
            "description": self.description,
            "instruction": self.instruction,
            "country": self.country
        }

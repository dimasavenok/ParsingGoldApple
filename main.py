from src.parser import PerfumeParser
from src.utils import save_to_json, save_to_csv


def main():
    scrolls_input = input("Сколько скроллов выполнять? (Enter для полного скролла): ").strip()
    scrolls = int(scrolls_input) if scrolls_input.isdigit() else None

    parser = PerfumeParser(scrolls=scrolls)
    try:
        parser.open_page("https://goldapple.ru/parfjumerija")
        parser.parse_products()
        save_to_json(parser.products, "goldapple_perfumes.json")
        save_to_csv(parser.products, "goldapple_perfumes.csv")
        print(f"✅ Сохранено {len(parser.products)} товаров")
    finally:
        parser.close()

if __name__ == "__main__":
    main()

import time
import re
import csv
import json

def scroll_to_bottom(driver, pause_time=2, max_scrolls=None):
    last_height = driver.execute_script("return document.body.scrollHeight")
    i = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        if max_scrolls is not None and i >= max_scrolls:
            break

def clean_html_text(html):
    text = re.sub(r'<br\s*/?>', '\n', html)
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

def save_to_json(items, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([item.to_dict() for item in items], f, ensure_ascii=False, indent=2)

def save_to_csv(items, filename):
    if not items:
        return
    keys = items[0].to_dict().keys()
    with open(filename, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for item in items:
            writer.writerow(item.to_dict())

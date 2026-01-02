from pymystem3 import Mystem
import re
from collections import Counter


STOP_WORDS = {
    "и", "в", "на", "с", "для", "по", "что", "это",
    "также", "только", "его", "ее", "к", "у", "о",
    "как", "от", "все", "начало", "каждый", "один",
    "очень", "можно", "ещё", "теперь"
}
mystem = Mystem()

def clean_meta_keywords(keywords: str) -> str:
    if not keywords:
        return ""

    words = keywords.split(",")

    words = [w.strip() for w in words if w.strip()]

    seen = set()
    clean_words = []
    for w in words:
        if w.lower() not in seen:
            clean_words.append(w)
            seen.add(w.lower())

    return ", ".join(clean_words)

def generate_meta_keywords(text: str = "", max_words=10) -> str:
    if not text:
        return ""

    analysis = mystem.analyze(text.lower())
    nouns = []

    for item in analysis:
        if 'analysis' in item and item['analysis']:
            lex = item['analysis'][0]
            lemma = lex['lex']
            gr = lex['gr']

            # Берём только существительные, исключаем стоп-слова и короткие слова
            if 'S' in gr and lemma not in STOP_WORDS and len(lemma) >= 3:
                nouns.append(lemma)

    # Считаем частоту и берём max_words
    counter = Counter(nouns)
    keywords = [w for w, _ in counter.most_common(max_words)]
    return ", ".join(keywords)

def generate_meta_title(title: str) -> str:
    return title or "Без названия"

def generate_meta_description(text: str = "") -> str:
    match = re.search(r"(.+?[.!?])(\s|$)", text)
    description = match.group(1).strip() if match else text.strip()
    return description[:160]
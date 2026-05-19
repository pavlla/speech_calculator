UNITS = {
    "zero": 0,
    "jeden": 1, "jedna": 1, "jedno": 1,
    "dwa": 2, "dwie": 2,
    "trzy": 3,
    "cztery": 4,
    "piec": 5, "pięć": 5,
    "szesc": 6, "sześć": 6,
    "siedem": 7,
    "osiem": 8,
    "dziewiec": 9, "dziewięć": 9,

    "pierwszej": 1, "pierwszego": 1, "pierwszy": 1, "pierwsza": 1,
    "drugiej": 2, "drugiego": 2, "drugi": 2, "druga": 2,
    "trzeciej": 3, "trzeciego": 3, "trzeci": 3, "trzecia": 3,
    "czwartej": 4, "czwartego": 4, "czwarty": 4, "czwarta": 4,
    "piatej": 5, "piatego": 5, "piaty": 5, "piata": 5,
    "piątej": 5, "piątego": 5, "piąty": 5, "piąta": 5,
    "szostej": 6, "szostego": 6, "szosty": 6, "szosta": 6,
    "szóstej": 6, "szóstego": 6, "szósty": 6, "szósta": 6,
    "siodmej": 7, "siodmego": 7, "siodmy": 7, "siodma": 7,
    "siódmej": 7, "siódmego": 7, "siódmy": 7, "siódma": 7,
    "osmej": 8, "osmego": 8, "osmy": 8, "osma": 8,
    "ósmej": 8, "ósmego": 8, "ósmy": 8, "ósma": 8,
    "dziewiatej": 9, "dziewiatego": 9, "dziewiaty": 9, "dziewiata": 9,
    "dziewiątej": 9, "dziewiątego": 9, "dziewiąty": 9, "dziewiąta": 9,
    "dziesiatej": 10, "dziesiatego": 10, "dziesiaty": 10, "dziesiata": 10,
    "dziesiątej": 10, "dziesiątego": 10, "dziesiąty": 10, "dziesiąta": 10,
}

TEENS = {
    "dziesiec": 10, "dziesięć": 10,
    "jedenascie": 11, "jedenaście": 11,
    "dwanascie": 12, "dwanaście": 12,
    "trzynascie": 13, "trzynaście": 13,
    "czternascie": 14, "czternaście": 14,
    "pietnascie": 15, "piętnaście": 15,
    "szesnascie": 16, "szesnaście": 16,
    "siedemnascie": 17, "siedemnaście": 17,
    "osiemnascie": 18, "osiemnaście": 18,
    "dziewietnascie": 19, "dziewiętnaście": 19,
}

TENS = {
    "dwadziescia": 20, "dwadzieścia": 20,
    "trzydziesci": 30, "trzydzieści": 30,
    "czterdziesci": 40, "czterdzieści": 40,
    "piecdziesiat": 50, "pięćdziesiąt": 50,
    "szescdziesiat": 60, "sześćdziesiąt": 60,
    "siedemdziesiat": 70, "siedemdziesiąt": 70,
    "osiemdziesiat": 80, "osiemdziesiąt": 80,
    "dziewiecdziesiat": 90, "dziewięćdziesiąt": 90,
}

HUNDREDS = {
    "sto": 100,
    "dwiescie": 200, "dwieście": 200,
    "trzysta": 300,
    "czterysta": 400,
    "piecset": 500, "pięćset": 500,
    "szescset": 600, "sześćset": 600,
    "siedemset": 700,
    "osiemset": 800,
    "dziewiecset": 900, "dziewięćset": 900,
}

THOUSANDS = {
    "tysiac", "tysiąc",
    "tysiace", "tysiące",
    "tysiecy", "tysięcy",
}


MULTI_TOKENS = [
    (("pierwiastek", "kwadratowy", "z"), "SQRT"),
    (("pierwiastek", "z"), "SQRT"),
    (("do", "potegi"), "POW"),
    (("do", "potęgi"), "POW"),
    (("podzielić", "przez"), "DIV"),
    (("podzielona", "przez"), "DIV"),
    (("podzielone", "przez"), "DIV"),
    (("podzielic", "przez"), "DIV"),
    (("pomnożyć", "przez"), "MUL"),
    (("pomnozyc", "przez"), "MUL"),

    (("otwórz", "nawias"), "LPAREN"),
    (("otworz", "nawias"), "LPAREN"),
    (("zamknij", "nawias"), "RPAREN"),

    (("równa", "się"), "EQUALS"),
    (("rowna", "sie"), "EQUALS"),
    (("silnia", "z"), "FACT"),
    (("pierwiastek",), "SQRT"),
    (("silnia",), "FACT"),
]

SINGLE_TOKENS = {
    "plus": "PLUS",
    "minus": "MINUS",
    "razy": "MUL",
    "x": "MUL",
    "przez": "DIV",
    "pomnozono": "MUL",
    "pomnożone": "MUL",
    "podzielone": "DIV",
    "potega": "POW",
    "potęga": "POW",
    "potegi": "POW",
    "potęgi": "POW",
}

SYMBOL_MAP = {
    "+": "plus",
    "x": "razy",
    "÷": "przez",
    "/": "przez",
    "^": "potega",
    "!": "silnia",
    "(": "otworz nawias",
    ")": "zamknij nawias",
}

TEXT_SUBS = [
    ("do kwadratu", "do potegi 2"),
    ("do sześcianu", "do potegi 3"),
    ("do szescianu", "do potegi 3"),
    ("kwadrat", "do potegi 2"),
    ("sześcian", "do potegi 3"),
    ("szescian", "do potegi 3"),
]


SPEECH = {
    "language": "pl-PL",
    "timeout": 10,
    "phrase_time_limit": 20,
    "pause_threshold": 1.8,
    "non_speaking_duration": 1.0,
    "calibration_duration": 1.5,
    "dynamic_energy": True,
}


EXIT_COMMANDS = {
    "wyjdz",
    "wyjście",
    "wyjscie",
    "koniec",
    "stop",
    "zakoncz",
}

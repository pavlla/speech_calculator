import math
import sys
import speech_recognition as sr
import pyttsx3

from config import (
    UNITS, TEENS, TENS, HUNDREDS, THOUSANDS,   
    MULTI_TOKENS, SINGLE_TOKENS, SYMBOL_MAP, TEXT_SUBS,
    SPEECH, EXIT_COMMANDS,
)


class ParseError(Exception):
    pass


def _init_tts():
    engine = pyttsx3.init()
    engine.setProperty("voice", "com.apple.voice.compact.pl-PL.Zosia")
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    return engine


def _speak(engine, text):
    engine.say(text)
    engine.runAndWait()


def _parse_group(words, pos):
    val, start = 0, pos

    if pos < len(words) and words[pos] in HUNDREDS:
        val += HUNDREDS[words[pos]]
        pos += 1

    if pos < len(words) and words[pos] in TEENS:
        val += TEENS[words[pos]]
        pos += 1
    elif pos < len(words) and words[pos] in TENS:
        val += TENS[words[pos]]
        pos += 1

        if pos < len(words) and words[pos] in UNITS and words[pos] != "zero":
            val += UNITS[words[pos]]
            pos += 1
    elif pos < len(words) and words[pos] in UNITS:
        val += UNITS[words[pos]]
        pos += 1

    if pos > start:
        return val, pos

    return None, pos


def parse_number(words, pos):
    if pos < len(words) and words[pos] == "zero":
        return 0, pos + 1

    g1, p1 = _parse_group(words, pos)

    if g1 is not None:
        if p1 < len(words) and words[p1] in THOUSANDS:
            g2, p2 = _parse_group(words, p1 + 1)
            return g1 * 1000 + (g2 or 0), p2 if g2 is not None else p1 + 1

        return g1, p1

    if pos < len(words) and words[pos] in THOUSANDS:
        g2, p2 = _parse_group(words, pos + 1)
        return 1000 + (g2 or 0), p2 if g2 is not None else pos + 1

    return None, pos

def normalize_expression(text: str) -> str:
    replacements = {
        "otwórz nawias okrągły": "(",
        "zamknij nawias okrągły": ")",
        "otwórz nawias": "(",
        "zamknij nawias": ")",
        "nawias otwarty": "(",
        "nawias zamknięty": ")",

        "silnia": "!",
        "razy": "*",
        "x": "*",
        "plus": "+",
        "minus": "-",
        "podzielić przez": "/",
        "podzielone przez": "/",

        "do potęgi drugiej": "^2",
        "do potęgi trzeciej": "^3",
        "do potęgi czwartej": "^4",
        "do potęgi piątej": "^5",
        "do potęgi szóstej": "^6",
        "do potęgi siódmej": "^7",
        "do potęgi ósmej": "^8",
        "do potęgi dziewiątej": "^9",
        "do potęgi dziesiątej": "^10",
    }

    normalized = text.lower()

    for word, symbol in replacements.items():
        normalized = normalized.replace(word, symbol)

    normalized = normalized.replace(" ", "")
    return normalized

def tokens_to_expression(tokens):
    symbols = {
        "PLUS": "+",
        "MINUS": "-",
        "MUL": "*",
        "DIV": "/",
        "POW": "^",
        "FACT": "!",
        "LPAREN": "(",
        "RPAREN": ")",
    }

    parts = []

    for token in tokens:
        if token == "END":
            continue

        if isinstance(token, tuple) and token[0] == "NUM":
            value = token[1]

            if float(value).is_integer():
                parts.append(str(int(value)))
            else:
                parts.append(str(value))

        elif token in symbols:
            parts.append(symbols[token])

    return "".join(parts)


def tokenize(text):
    import re

    text = text.lower()

    for old, new in TEXT_SUBS:
        text = text.replace(old, new)

    for sym, word in SYMBOL_MAP.items():
        text = text.replace(sym, f" {word} ")

    text = re.sub(r"[,;.:!?]", " ", text)

    words = text.split()
    tokens = []
    i = 0

    while i < len(words):
        matched = False

        for pattern, tok in MULTI_TOKENS:
            n = len(pattern)

            if words[i:i + n] == list(pattern):
                tokens.append(tok)
                i += n
                matched = True
                break

        if matched:
            continue

        word = words[i]

        if word in SINGLE_TOKENS:
            tokens.append(SINGLE_TOKENS[word])
        else:
            try:
                value = int(word)

                if (
                    i + 1 < len(words)
                    and words[i + 1].isdigit()
                    and len(words[i + 1]) == 3
                ):
                    value = value * 1000 + int(words[i + 1])
                    i += 1

                tokens.append(("NUM", value))

            except ValueError:
                val, new_i = parse_number(words, i)

                if val is not None:
                    tokens.append(("NUM", val))
                    i = new_i
                    continue

        i += 1

    tokens.append("END")
    return tokens


def _fact(x):
    if x < 0 or x != int(x):
        raise ParseError("Silnia tylko dla nieujemnych liczb całkowitych!")
    return math.factorial(int(x))


def _sqrt(x):
    if x < 0:
        raise ParseError("Pierwiastek z liczby ujemnej!")
    return math.sqrt(x)


class _Eval:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def _cur(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return "END"

    def _eat(self):
        value = self._cur()
        self.i += 1
        return value

    def run(self):
        value = self._expr()

        return value

    def _expr(self):
        value = self._term()

        while self._cur() in ["PLUS", "MINUS"]:
            operator = self._eat()
            right = self._term()

            if operator == "PLUS":
                value += right
            else:
                value -= right

        return value

    def _term(self):
        value = self._power()

        while self._cur() in ["MUL", "DIV"]:
            operator = self._eat()
            right = self._power()

            if operator == "DIV":
                if right == 0:
                    raise ParseError("Dzielenie przez zero!")
                value /= right
            else:
                value *= right

        return value

    def _power(self):
        value = self._unary()

        if self._cur() == "POW":
            self._eat()
            return value ** self._power()

        return value

    def _unary(self):
        current = self._cur()

        if current == "MINUS":
            self._eat()
            return -self._unary()

        if current == "SQRT":
            self._eat()
            return _sqrt(self._atom())

        if current == "FACT":
            self._eat()
            return _fact(self._atom())

        return self._postfix()

    def _postfix(self):
        value = self._atom()

        if self._cur() == "FACT":
            self._eat()
            return _fact(value)

        return value

    def _atom(self):
        token = self._cur()

        if isinstance(token, tuple):
            self._eat()
            return float(token[1])

        if token == "LPAREN":
            self._eat()

            if self._cur() == "RPAREN":
                raise ParseError("Pusty nawias.")

            value = self._expr()

            if self._cur() != "RPAREN":
                raise ParseError("Brak zamknięcia nawiasu.")

            self._eat()
            return value

        raise ParseError(f"Nie rozpoznano: {token}")


def oblicz(text):
    tokens = []

    try:
        tokens = tokenize(text)

        if tokens[0] == "END":
            return None, "Nie rozpoznano wyrażenia.", tokens

        evaluator = _Eval(tokens)
        result = evaluator.run()

        return result, None, tokens

    except ParseError as error:
        return None, str(error), tokens
    except OverflowError:
        return None, "Wynik zbyt duży.", tokens
    except Exception as error:
        return None, f"Błąd: {error}", tokens


def fmt_wynik(value):
    if isinstance(value, int):
        return str(value)

    if math.isfinite(value) and value == int(value) and abs(value) < 1e15:
        return str(int(value))

    return f"{value:.10g}"


def _rozpoznaj(recognizer, source):
    try:
        print("Słucham...")

        audio = recognizer.listen(
            source,
            timeout=SPEECH["timeout"],
            phrase_time_limit=SPEECH["phrase_time_limit"]
        )

        print("Przetwarzam...")
        return recognizer.recognize_google(audio, language=SPEECH["language"])

    except sr.WaitTimeoutError:
        print("Spróbuj ponownie.")
    except sr.UnknownValueError:
        print("Nie rozumiem - powtórz.")
    except sr.RequestError as error:
        print(f"Błąd Google Speech API: {error}")

    return None


def main():

    try:
        microphone = sr.Microphone()
    except OSError:
        print("Brak mikrofonu!")
        sys.exit(1)

    engine = _init_tts()

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = SPEECH["pause_threshold"]
    recognizer.non_speaking_duration = SPEECH["non_speaking_duration"]
    recognizer.dynamic_energy_threshold = SPEECH["dynamic_energy"]

    with microphone as source:
        recognizer.adjust_for_ambient_noise(
            source,
            duration=SPEECH["calibration_duration"]
        )

    intro = "Cześć, jestem twoim kalkulatorem głosowym. Podaj wyrażenie matematyczne. Powiedz stop, aby zakończyć."
    print(intro)
    _speak(engine, intro)

    with microphone as source:
        while True:
            text = _rozpoznaj(recognizer, source)

            if text is None:
                continue


            text_lower = text.lower().strip()

            if text_lower in EXIT_COMMANDS or any(command in text_lower for command in EXIT_COMMANDS):
                exit_message = "Do widzenia!"
                print("Do widzenia!")
                _speak(engine, exit_message)
                break

            result, error, tokens = oblicz(text_lower)
            math_expression = tokens_to_expression(tokens)
            print(f'Rozpoznano: "{math_expression}"')

            if error:
                print(f"Błąd: {error}")
                _speak(engine, f"Błąd: {error}")
            else:
                result_text = fmt_wynik(result)
                print(f"Wynik: {result_text}")
                _speak(engine, f"Wynik: {result_text}")


import urllib.request
import argparse
import random
import os


def bullscows(guess: str, secret: str) -> (int, int):
    return sum(x == y for x, y in zip(guess, secret)), len(set(guess) & set(secret))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secretWord, cnt = random.choice(words), 1
    print(secretWord)
    while True:
        cnt += 1
        guessedWord = ask("Введите слово: ", words)
        bulls, cows = bullscows(guessedWord, secretWord)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if guessedWord == secretWord:
            return cnt


def ask(prompt: str, valid: list[str] = None) -> str:
    guessedWord = input(prompt)
    return guessedWord


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dict", help="dictionary file path or url")
    parser.add_argument("len", type=int, default=5, help="length of secret word")
    args = parser.parse_args()

    gameDict = args.dict
    length = args.len

    if not os.path.isfile(f"./{gameDict}"):
        urllib.request.urlretrieve(gameDict, 'dict')
        gameDict = "dict"

    with open(gameDict, "r") as f:
        words = [word.strip() for word in f if len(word.strip()) == length]

    print("Количество попыток: ", gameplay(ask, inform, words))


if __name__ == "__main__":
    main()

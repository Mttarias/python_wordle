import pathlib
import random


def main():
    
    word = getWord()

    for guessNum in range(1,7):
        guess = input(f"Guess {guessNum}: ").upper()

        if guess == word:
            print("You guessed correctly!")
            break
        
        showGuess(guess, word)
        
    else:
        gameOver(word)


def getWord():
    WORD_LIST = pathlib.Path("wordlist.txt")

    words = [
        word.upper() for word in WORD_LIST.read_text(encoding="utf-8").strip().split("\n")
    ]

    return random.choice(words)


def showGuess(guess, word):
    correctLetters = {
            letter for letter, correct in zip(guess, word) if letter == correct
        }
    misplacedLetters = set(guess) & set(word) - correctLetters
    wrongLetters = set(guess) - set(word)

    print("Correct letters: ", ", ".join(sorted(correctLetters)))
    print("Misplaced letters: ", ", ".join(sorted(misplacedLetters)))
    print("Wrong letters: ", ", ".join(sorted(wrongLetters)))


def gameOver(word):
    print(f"The word was {word}")

if __name__ == "__main__":
    main()
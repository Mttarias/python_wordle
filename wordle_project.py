import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

#Rich console
console = Console(width=40, theme=Theme({"warning": "red on yellow"}))

LETTERS_NUM = 5
GUESSES_NUM = 6
WORD_LIST = pathlib.Path(__file__).parent / "wordlist.txt"


def main():
    #Pre process
    word = getWord(WORD_LIST.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * LETTERS_NUM] * GUESSES_NUM
    correct = False

    #Main process
    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(GUESSES_NUM):
            refreshPage(headline=f"Guess {idx + 1}")
            showGuesses(guesses, word)

            guesses[idx] = guessWord(previousGuesses=guesses)
            if guesses[idx] == word:
                correct = True
                break
    
    #Post process
    gameOver(guesses, word, correct)

#Random word generator, function takes a word list and sets the words to uppercase.
#It only adds words that are the appropriate length and only contain english characters.
#If no words meet criteria console prints error and calls SystemExit()
def getWord(wordList):

    if words := [
        word.upper()
        for word in wordList
        if len(word) == LETTERS_NUM and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print(f"No words of length {LETTERS_NUM} in the word list", style="warning")
        raise SystemExit()

#Player input validation, takes player input and validates:
#-if the user already guess the word
#-if the word is smaller or larger than the set amount
#-if there are invalid characters
def guessWord(previousGuesses):
    guess = console.input("\nGuess word: ").upper()

    if guess in previousGuesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        return guessWord(previousGuesses)
    
    if len(guess) != LETTERS_NUM:
        console.print(f"Your guess must be {LETTERS_NUM} letters.", style="warning")
        return guessWord(previousGuesses)
    
    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f"Invalid letter: '{invalid}'. Please use English letters."
                      , style="warning")
        return guessWord(previousGuesses)
    return guess

#Guesses, displays previous guesses as well as the english alphabet letters
#Color coded to display correct guesses, misplaced guesses and incorrect guesses
def showGuesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styledGuess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styledGuess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"
    
        console.print("".join(styledGuess), justify="center")
    console.print("\n" + "".join(letter_status.values()), justify="center")

#End game, function announces game over and displays the correct word whether the player
#was correct or incorrect.
def gameOver(guesses, word, guessedCorrectly):
    refreshPage(headline="Game Over")
    showGuesses(guesses, word)

    if guessedCorrectly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

#Game header, function clears view and prints new header to track guess numbers and gameover
def refreshPage(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


if __name__ == "__main__":
    main()
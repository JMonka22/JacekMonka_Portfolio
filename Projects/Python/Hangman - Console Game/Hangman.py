import random
import sys, os
import time
import re
from colorama import init, Fore, Back, Style

HANGMAN = [
    '________',
    '|       |',
    '|       O',
    '|       |',
    '|      /|\ ',
    '|       |',
    '|      / \         OOF'
]

WORDS = [
    'OBJECT','ORIENTED', 'PROGRAMMING', 'EXERCISE', 'WORD', 'PYTHON', 'CLASS', 'METHOD', 'PROJECT', 'PORTFOLIO',
    'HANGMAN', 'CONSOLE', 'CHARACTER', 'BUG', 'TEST', 
]

class Hangman():

    def __init__(self, chosen_word):
        self.failed_attempts = 0
        self.points = 0
        self.chosen_word = chosen_word
        self.guessed_letters = []

    def get_user_input(self):
        user_input = input("Input letter you'd like to reveal!")[0].upper()
        while user_input in self.guessed_letters:
            print('You already guesed that letter!')
            user_input = input('')[0].upper()
        self.guessed_letters.append(user_input)
        return user_input
    
    def check_letter(self, user_input):
        if user_input in self.chosen_word:
            return len(re.findall(user_input, self.chosen_word))
        return False

    def print_hangman(self):
        print(Fore.RED)
        for i in range(self.failed_attempts):
            print(HANGMAN[i])
        print(Fore.RESET)

    def hangman_game(self):

        while self.failed_attempts != len(HANGMAN) and self.points != len(self.chosen_word):

            os.system('cls')

            print(Fore.YELLOW + '\t\t\tHANGMAN' + Fore.RESET)       
            for char in self.chosen_word:
                if char not in self.guessed_letters:
                    print('_ ', end="")
                else:
                    print(char + " ", end="")
            print()

            self.print_hangman()

            input = self.get_user_input()

            if not self.check_letter(input):
                self.failed_attempts += 1
            else:
                self.points += self.check_letter(input)

        if self.failed_attempts == len(HANGMAN):
            os.system('cls')
            print(Fore.RED + "\nYOU LOSE!\nWord: " + self.chosen_word + Fore.RESET)
            self.print_hangman()    
        if self.points == len(self.chosen_word):
            print(Fore.GREEN + "\nYOU WIN!\nWord: " + self.chosen_word + Fore.RESET)
        print()


if __name__ == '__main__':
    again = 'Y'
    while again.upper() == 'Y':
        word_to_guess = random.choice(WORDS)
        hangman = Hangman(word_to_guess)
        hangman.hangman_game() 
        again = input(Fore.YELLOW + 'Input Y if you want to play again :)' + Fore.RESET) 
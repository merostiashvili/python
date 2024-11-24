import random
import hangman_library

print(hangman_library.main_picture)
picked_word = random.choice(hangman_library.list_of_words)
print(picked_word)
length_of_word = len(picked_word)
continue_game = True
users_progress = []
remaining_lives = 6
for letter in range(length_of_word):
    if letter == " ":
        users_progress += " "
    else:
        users_progress += "_"
print(''.join(users_progress))
while continue_game:
    guessed_letter = input("Guess a letter: ")
    if len(guessed_letter) == 1:
        guessed_letter = guessed_letter.lower()
        if guessed_letter in picked_word:
            print(f"Well done, letter {guessed_letter} is in the word")
            for position_of_guessed_letter in range(length_of_word):
                if picked_word[position_of_guessed_letter] == guessed_letter:
                    users_progress[position_of_guessed_letter] = guessed_letter
            print(''.join(users_progress))
        else:
            remaining_lives -= 1
            print("wrong choice")
            print(hangman_library.lives[remaining_lives])
            if remaining_lives == 0:
                continue_game = False;
                print("game over 😔 ")
        if "_" not in users_progress:
            continue_game = False
            print("You won !!! Congrats ❤️ ")
    else:
        print("only one word at once")

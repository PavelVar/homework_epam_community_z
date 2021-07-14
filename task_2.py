import random

lives = 10  # начальное количество жизней
words_variants = ['dog', 'cat', 'hamster']  # список возможных слов
word_right = random.choice(words_variants)  # выбор слова
word_in_game = '_' * len(word_right)  # шаблон слова из подчеркиваний

# игра продолжается пока есть неугаданные буквы и не использованы все попытки
while ('_' in word_in_game) and (lives > 0):
    print('Lives count:', lives)  # вывод количества оставшихся попыток (жизней)
    print(word_in_game)  # вывод слова в игре с учетом отгаданного
    letter = input('Input character (1) or the full word: ')  # ввод буквы или слова

    # проверка правильности попытки
    if letter == word_right:  # если сделана попытка назвать все слово целиком
        word_in_game = letter
    elif letter in word_right and len(letter) == 1:  # есть ли выбранная буква в слове
        print('You ar right! We have this letter in word.')
        index = -1

        #  замена символа на игровом поле на правильную букву
        while word_in_game.count(letter) != word_right.count(letter):
            index = word_right.find(letter, index + 1)
            word_in_game = word_in_game[:index] + letter + word_in_game[index+1:]

    else:  # если попытка неудачная
        lives -= 1
        print('Bad try :(')

    print('*' * 10)  # печать разделителя между попытками

# подведение итогов
print('Right word:', word_right)
if lives > 0:
    print('You win!')
else:
    print('You loose. Game over')

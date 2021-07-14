import requests
import random

words_variants = ['dog', 'pig', 'bird', 'spider']  # list of words in use

# base data for bot
my_token = '1867768916:AAEbplTkKzgNyoQfwiELWe4y8F1acMpijAU'
root_url = 'https://api.telegram.org/bot'
bot_updates = '/getUpdates'
send_message_endpoint = '/sendMessage'


# update info about user messages
def get_updates(token):
    updates_url = f'{root_url}{token}{bot_updates}'
    res = requests.get(updates_url)
    status = res.status_code
    if 200 <= status < 300:
        updates = res.json()
        return updates
    else:
        print(f"Request failed with code {res.status_code}")


# initiations of the game
def game_start():
    lives = 10  # start lives amount
    word_right = random.choice(words_variants)  # word choosing
    word_in_game = '*' * len(word_right)  # shape of word
    return lives, word_right, word_in_game


# sending initial message with game rules
def first_message(lives, word_right, word_in_game):
    message = 'Hello. I am your bot. I will play with you in "Guess the word" game.\n' \
              "Below you'll see the word I have conjured up as: * * * * \n" \
              'The amount of "*" is equal to the letters in my word.\n' \
              'Every try you can wright only one letter or the full word.\n' \
              "If the letter is in my word you'll see it's in place.\n" \
              'Remember, we are playing in English.\n' \
              'You have 10 chances to guess. Good luck!'
    send_message(my_token, chat_id, message)  # start function sending messages to user
    message = f'Lives count: {lives}'
    send_message(my_token, chat_id, message)  # send amount of lives rest
    message = f'There are {len(word_right)} letters in my word'
    send_message(my_token, chat_id, message)  # send the word lengths
    message = word_in_game
    send_message(my_token, chat_id, message)  # send the word in game


# sending messages to user
def send_message(token, chat_id, message_text):
    send_message_url = f'{root_url}{token}{send_message_endpoint}'
    res = requests.post(send_message_url, {'chat_id': chat_id, 'text': message_text})
    status = res.status_code
    if 200 <= status < 300:
        return True
    else:
        print(f"Request failed with code {res.status_code}")


# check the try
def check():
    if last_message_text == word_right or word_in_game == word_right:  # if the full word was wright
        return 'Victory'
    elif len(last_message_text.split()) > 1 or len(last_message_text) > 1:  # if more than1 word or letter are typed
        return 'Error'
    elif last_message_text in word_right:  # if the letter is ok
        return "Ok"


# action when win
def victory():
    send_message(my_token, chat_id, f"You win! Congratulations!\nOur word was '{word_right}'")
    send_message(my_token, chat_id, "Type 'start' if you want to play again")
    game_end()


# action when mistake
def mistake(flag):
    global lives
    lives -= 1
    message_1 = f"Check input, you wrote more than 1 word or more than 1 letter.\nLives count: {lives}"
    message_2 = f"Sorry, there is a false word or no this letter in our word. Try again..\nLives count: {lives}"
    if lives == 0:
        send_message(my_token, chat_id, f"You loose( \nOur word was '{word_right}'")
        send_message(my_token, chat_id, "Type 'start' if you want to play again")
        game_end()
    else:
        if flag == 'Error':
            send_message(my_token, chat_id, message_1)
        else:
            send_message(my_token, chat_id, message_2)


# end game
def game_end():
    global word_right
    word_right = ''


lives, word_right, word_in_game = game_start()  # get started game
# reading user messages
last_message_number = 0
while True:
    updates = get_updates(my_token)  # start function to get user message
    last_message = updates['result'][-1]
    message_id = last_message['message']['message_id']  # get message id
    chat_id = last_message['message']['chat']['id']
    last_message_text = last_message['message']['text'].lower()  # get message text
    if message_id > last_message_number:  # check if the message is new
        if last_message_text in ('/start', 'start'):  # check if it is a start of user work
            lives, word_right, word_in_game = game_start()
            first_message(lives, word_right, word_in_game)
        else:
            if word_right == '':  # if the game was ended
                send_message(my_token, chat_id, 'If you want to continue, type start.')
            else:
                if check() == 'Victory':  # if the full word is ok
                    victory()
                elif check() == "Error":  # if mistake in typing
                    mistake("Error")
                elif check() == "Ok":  # if the letter is ok
                    index = -1
                    #  change the symbol by the right letter
                    while word_in_game.count(last_message_text) != word_right.count(last_message_text):
                        index = word_right.find(last_message_text, index + 1)
                        word_in_game = word_in_game[:index] + last_message_text + word_in_game[index + 1:]
                    if check() == 'Victory':  # if the word is ok in result
                        victory()
                    else:  # if just letter is ok
                        send_message(my_token, chat_id, 'You are right! We have this letter in the word.')
                        send_message(my_token, chat_id, word_in_game)
                else:
                    mistake('else')  # if the letter is wrong

        last_message_number = message_id  # update message_id

import json
import random

haiku_dictionary = ""
uncouth_mode = False #whether or not to write foul and uncouth poetry
def retrieve_dictionary():
    if uncouth_mode:
        with open('uncouth_dictionary.json', 'r') as haiku_dictionary_raw_json:
            haiku_dictionary = json.loads(haiku_dictionary_raw_json.read())
    else:
        with open('haiku_dictionary.json', 'r') as haiku_dictionary_raw_json:
            haiku_dictionary = json.loads(haiku_dictionary_raw_json.read())

def generate_haiku():
    haiku = ""
    for i in range(3):
        max_syllables = 5
        if i == 1:
            max_syllables = 7
        syllable_count = 0
        word_count = 0
        while syllable_count < max_syllables:
            next_word = get_word();
            if syllable_count + int(next_word['number_of_syllables']) <= max_syllables:
                haiku += next_word['word'] + " "
                syllable_count += int(next_word['number_of_syllables'])
                word_count += 1
        haiku += "\n"
    return haiku

def get_word():
    return haiku_dictionary['dictionary'][random.randint(0, len(haiku_dictionary['dictionary']) - 1)]

def update_dictionary(word, part_of_speech, number_of_syllables):
    if not uncouth_mode:
        haiku_dictionary_raw_json_temp = open('haiku_dictionary.json', 'r')
        haiku_dictionary_raw_json = haiku_dictionary_raw_json_temp.read()
        haiku_dictionary_raw_json_temp.close()
        haiku_dictionary_dict = json.loads(haiku_dictionary_raw_json)
        haiku_dictionary_dict['dictionary'].append({"word":word,"part_of_speech":part_of_speech,"number_of_syllables":number_of_syllables})
        haiku_dictionary_string = json.dumps(haiku_dictionary_dict, indent=2)
        with open('haiku_dictionary.json', 'w') as haiku_dictionary_temp:
            haiku_dictionary_temp.write(haiku_dictionary_string)
        with open('haiku_dictionary.json', 'r') as haiku_dictionary_temp:
            haiku_dictionary = json.loads(haiku_dictionary_temp.read())
    else:
        haiku_dictionary_raw_json_temp = open('uncouth_dictionary.json', 'r')
        haiku_dictionary_raw_json = haiku_dictionary_raw_json_temp.read()
        haiku_dictionary_raw_json_temp.close()
        haiku_dictionary_dict = json.loads(haiku_dictionary_raw_json)
        haiku_dictionary_dict['dictionary'].append({"word":word,"part_of_speech":part_of_speech,"number_of_syllables":number_of_syllables})
        haiku_dictionary_string = json.dumps(haiku_dictionary_dict, indent=2)
        with open('uncouth_dictionary.json', 'w') as haiku_dictionary_temp:
            haiku_dictionary_temp.write(haiku_dictionary_string)
        with open('uncouth_dictionary.json', 'r') as haiku_dictionary_temp:
            haiku_dictionary = json.loads(haiku_dictionary_temp.read())

def dictionary_duplicate(word):
    for i in haiku_dictionary['dictionary']:
        if i['word'] == word:
            return True
    return False

commands = "Commands: \nhaiku - generates a haiku\nadd word - add word to dictionary\nexit - close program\nhelp - \"remind me what the commands are, I'm a retard who can't remember 3 commands\""

print("Haiku Generator\nThis program generates pseudorandom haikus using its own ever-growing dictionary.")
print(commands)

user_input = ""
while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input == "haiku":
        print(generate_haiku())
        continue
    elif user_input == "uncouth mode":
        uncouth_mode = True
    elif user_input == "add word":
        while True:
            new_word = input("Enter your new word:\n")
            if dictionary_duplicate(new_word):
                print("This word is already in the dictionary :)")
                continue
            part_of_speech = input("What part of speech is your word? \nPossible parts of speech: noun, proper noun, pronoun, verb, adjective, adverb, preposition, conjunction, article\n")
            number_of_syllables = input("How many syllables does your word have? Must be less than 7\n")
            if int(number_of_syllables) > 7:
                print("Too many syllables")
                continue
            update_dictionary(new_word, part_of_speech, number_of_syllables)
            break
        continue
    elif user_input == "help":
        print(commands)
        continue
    else:
        print("Not a valid command, type \"help\" for commands")

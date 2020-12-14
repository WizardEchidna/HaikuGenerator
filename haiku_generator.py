import json
import random
import requests

seed_list = []
with open('random_seed_list.txt', 'r') as file:
    seed_list = file.readlines()

def generate_haiku():
    haiku = ""
    for line in range(3):
        max_syllables = 5
        if line == 1:
            max_syllables = 7
        syllable_count = 0
        word_count = 0
        while syllable_count < max_syllables:
            random_word_list = get_random_word_list()
            bad_entries = []
            possible_word = choice_excluding(random_word_list, bad_entries)
            if word_good(possible_word, max_syllables - syllable_count):
                haiku += possible_word['word'] + " "
                syllable_count += int(possible_word['numSyllables'])
                word_count += 1
            else:
                bad_entries.append(possible_word)
        haiku += "\n"
    return haiku

def word_good(word_dict, max_syl):
    frequency = float(word_dict['tags'][-1][2:])
    is_valid_pos = True
    for i in word_dict['tags']:
        if i == 'prop' or i == 'u':
            is_valid_pos = False
    vowels = 'aeiouy'
    has_vowel = False
    for i in word_dict['word']:
        if i in vowels:
            has_vowel = True
            break
    if word_dict['numSyllables'] > max_syl or frequency < 1.0 or not is_valid_pos or not has_vowel:
        return False
    else:
        return True

def get_random_word_list():
    source = "https://api.datamuse.com/words"
    constraint_list = ['ml', 'sl','rel_ant', 'rel_nry','ml', 'ml', 'ml']
    seed = random.choice(seed_list)
    while True:
        req = requests.get(source + '?' + random.choice(constraint_list) + '=' + seed + '&md=dpsrf').text
        response = json.loads(req)
        if len(response) != 0:
            return response

def choice_excluding(list, exclude):
    revised_list = []
    for item in list:
        if item not in exclude:
            revised_list.append(item);
    return random.choice(revised_list)

commands = "Commands: \nhaiku - generates a haiku\nexit - close program\nhelp - remind me what the commands are\n"

print("Haiku Generator\nThis program generates pseudorandom haikus using the Datamuse API.")
print(commands)

user_input = ""
while True:
    user_input = input(">")
    if user_input == "exit":
        break
    elif user_input == "haiku":
        print(generate_haiku())
        continue
    elif user_input == "help":
        print(commands)
        continue
    else:
        print("Not a valid command, type \"help\" for commands")

import pandas as pd
from pprint import pprint
import numpy as np
from random import sample
import random
random.seed(128)

df = pd.read_csv('food.csv')
words = (set(df['Category']))

words = set(w for w in words if len(w.split()) < 4)


english_numbers = """two
three
four
five
six
seven
eight
nine
ten
eleven
twelve
thirteen
fourteen
fifteen
sixteen
seventeen
eighteen
nineteen
twenty
twenty-one
twenty-two
twenty-three
twenty-four
twenty-five
twenty-six
twenty-seven
twenty-eight
twenty-nine
thirty
thirty-one""".split()

add_sentences = [
    "i want XXX YYY",
    "i want YYY",
    "i desire YYY",
    "i desire XXX YYY",
    "i wish YYY",
    "i wish XXX YYY",
    "i want to buy XXX YYY",
    "i want to buy YYY",
    "i want to add XXX YYY",
    "i want to add some YYY to the list",
    "i want to add some YYY",
    "add YYY to the list",
    "add XXX YYY to the list",
    "add XXX YYY to the shoppint list",
    "insert XXX YYY",
    "insert XXX YYY in the list",
    "insert YYY in the list",
    "insert YYY in the shopping list",
    "remember me to buy some YYY",
    "remember me to buy some XXX YYY",
    "i would like to add XXX YYY to the list",
    "i would like to add some YYY to the list",
    "I would like to order XXX YYY",
    "I would like to order YYY",
    "I would like to get XXX YYY",
    "I would like to get YYY",
    "I would like to include XXX YYY",
    "I would like to include YYY",
    "I would like to have XXX YYY on my list"
    "I would like to have YYY on my list"
    "I need XXX YYY",
    "I need YYY",
    "I want to purchase XXX YYY",
    "I want to purchase YYY",
    "place XXX YYY on my list",
    "place XXX YYY on my shopping list",
    "place YYY on my list",
    "place YYY on my shopping list",
    "place XXX YYY on the list",
    "place XXX YYY on the shopping list",
    "I would like to put XXX YYY on my list",
    "put XXX YYY on my list",
    "set XXX YYY on my list"

]

remove_sentences = [
    "i want to remove XXX YYY",
    "i want to delete XXX YYY",
    "i want to cancel some YYY from the list",
    "i want to cancel some YYY",
    "delete XXX YYY from the list",
    "delete YYY from the list",
    "delete XXX YYY from the shopping list",
    "delete YYY from the shopping list",
    "delete XXX YYY",
    "delete YYY",
    "cancel XXX YYY from the shopping list",
    "cancel YYY from the shopping list",
    "cancel XXX YYY from the list",
    "cancel YYY from the list",
    "cancel XXX YYY",
    "cancel YYY",
    "remove XXX YYY",
    "remove YYY",
    "remove XXX YYY from the list",
    "remove YYY from the list",
    "i would like to remove XXX YYY from the list",
    "i would like to cancel some YYY from the list",
    "i would like to delete some YYY from the list",
    "cross out XXX YYY",
    "cross out YYY",
    "eliminate XXX YYY",
    "eliminate YYY",
    "eliminate XXX YYY from the list",
    "eliminate YYY from the list",
    "eliminate XXX YYY from the shopping list",
    "eliminate YYY from the shopping list",
    "exclude XXX YYY",
    "exclude YYY",
    "exclude XXX YYY from the list",
    "exclude YYY from the list",
    "exclude XXX YYY from the shopping list",
    "exclude YYY from the shopping list",
    "black out XXX YYY",
    "black out YYY",
    "undo XXX YYY",
    "undo YYY",
    "erase XXX YYY",
    "erase YYY",
    "erase XXX YYY from the list",
    "erase YYY from the list",
    "erase XXX YYY from the shopping list",
    "erase YYY from the shopping list"
]

numbers = [
    lambda : '[one]{"entity": "number", "value": 1}',
    lambda : '[a]{"entity": "number", "value": 1}',
    lambda : '[an]{"entity": "number", "value": 1}',
]
numbers += [lambda: f'[{np.random.random_integers(0, 100)}](number)']\
    		+	[lambda:f'[{sample(english_numbers,1)[0]}](number)']

infinite_numbers = [
    lambda : '[all]{"entity": "number", "value": -1} the',
    lambda : '[all]{"entity": "number", "value": -1}',
    lambda : '[any]{"entity": "number", "value": -1}',
    lambda : '[every]{"entity": "number", "value": -1}',
    lambda : '[every single]{"entity": "number", "value": -1}',
    lambda : '[completely]{"entity": "number", "value": -1} the',
    lambda : '[entirely]{"entity": "number", "value": -1} the',
    lambda : '[totally]{"entity": "number", "value": -1} the',
    lambda : '[wholly]{"entity": "number", "value": -1} the',
    lambda : '[fully]{"entity": "number", "value": -1} the',
    lambda : '[each and every]{"entity": "number", "value": -1}',
    lambda : '[the whole lot]{"entity": "number", "value": -1} of',
    lambda : '[each]{"entity": "number", "value": -1}',
]

inform_sentences = ['XXX', 'YYY', 'XXX YYY', 'YYY XXX']

show_list_sentences = [
    'how many YYY are there on the list?',
    'show me the number of YYY',
    'how many YYY are there?',
    'how many YYY do i need to buy?',
    'let me see the number of YYY',
    'let me see how many YYY are there',
    'What was it I wanted to buy?',
    'show my list',
    'show my shopping list',
    'show me my list',
    'show me my shopping list',
    'show my articles',
    'show my things',
    'I want to see my list',
    'I want to see my shopping list',
    'I would like to see my list',
    'I would like to see my shopping list',
    'list my things',
    'list my articles',
    'display my list',
    'display my shopping list',
    'display my articles',
    'display my things',
    'present me my list',
    'present me my shopping list',
    'open my list',
    'open my shopping list',
    
]

set_item=set()
for w in sample(words, len(words)//3):
    for num in sample(numbers, np.random.random_integers(2, 3)):
        sentence = sample(add_sentences, 1)[0]
        sentence = sentence.replace('XXX', num())\
            .replace('YYY', f'[{w.lower()}](item)')
        if (np.random.uniform() < 0.2):
            sentence = sentence.replace(
                'list', sample(['lis', 'lits', 'ist'], 1)[0])
        set_item.add('- '+str(sentence))
print( '\n'.join(set_item) ,file= open('add_item.txt', 'w') )

set_remove=set()
remove_numbers = numbers+infinite_numbers
for w in sample(words, len(words)//3):
    for num in sample(remove_numbers, np.random.random_integers(2, 3)):
        sentence = sample(remove_sentences, 1)[0]
        sentence = sentence.replace('XXX', num())\
            .replace('YYY', f'[{w.lower()}](item)')
        if (np.random.uniform() < 0.2):
            sentence = sentence.replace(
                'list', sample(['lis', 'lits', 'ist'], 1)[0])
        set_remove.add('- '+str(sentence) )
print( '\n'.join(set_remove) ,file= open('remove_item.txt', 'w') )
    
set_inform=set()
remove_numbers = numbers+infinite_numbers
for w in sample(words, len(words)//3):
    for num in sample(remove_numbers, np.random.random_integers(2, 3)):
        sentence = sample(inform_sentences, 1)[0]
        sentence = sentence.replace('XXX', num())\
            .replace('YYY', f'[{w.lower()}](item)')

        set_inform.add('- '+str(sentence) )
print( '\n'.join(set_inform) ,file= open('inform.txt', 'w') )

set_list=set()
with open('show_list.txt', 'w') as f:
    for w in sample(words, len(words)//3):
        for _ in range(np.random.random_integers(2, 3)):
            sentence = sample(show_list_sentences, 1)[0]
            sentence = sentence.replace('YYY', f'[{w.lower()}](item)')
            set_list.add('- '+str(sentence) )
print( '\n'.join(set_list) ,file= open('show_list.txt', 'w') )

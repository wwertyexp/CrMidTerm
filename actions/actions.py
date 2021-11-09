# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import spacy
from spellchecker import SpellChecker

shopping_list = {}
nlp = spacy.load("en_core_web_md")
spell = SpellChecker()


def get_word_lemma(word, debug=False):
    '''
    Correct and extract lemma from the given word.
    '''
    if (debug):print('original:',word,end='|')
    #misspelled = spell.unknown([word])

    correct = spell.correction(word)
    if (debug):print('correction:',correct,end='|')

    processed_text = nlp(correct)
    lemma_tags = {"NNS", "NNPS",'NNP','NN'}
    for token in processed_text:
        lemma = token.text
        if token.tag_ in lemma_tags:
            lemma = token.lemma_
    if (debug):print('LEMMA:',lemma)
    return correct, lemma

def extract_number(number_slot):
    '''
    Extract duckling number from the given slot
    '''

    # workaround for pipeline conflicts

    try:
        quantity = int(number_slot)
    except:
        for quantity in number_slot:
            try:
                quantity=int(quantity)
                break
            except:
                pass
    return quantity

class ActionAdd(Action):

    def name(self) -> Text:
        return "action_add"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        item = tracker.get_slot('item_to_add')
        items = item.split()
        corrects_lemmas = [get_word_lemma(item,debug=True) for item in items]

        lemma = ' '.join(lemma for correct, lemma in corrects_lemmas)

        number_slot = tracker.get_slot('number')
        quantity = extract_number(number_slot)
        
        shopping_list[lemma] = shopping_list.get(lemma, 0) + (quantity)

        correct_spelling = ' '.join(correct for correct, lemma in corrects_lemmas)
        dispatcher.utter_message(
            text=f"I've just added {quantity} {correct_spelling} to the shopping list!")

        return [AllSlotsReset()]

class ActionList(Action):

    def name(self) -> Text:
        return "action_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=str(shopping_list))

        return []

class ActionRemove(Action):

    def name(self) -> Text:
        return "action_remove"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item = tracker.get_slot('item_to_remove')

        items = item.split()
        corrects_lemmas = [get_word_lemma(item,debug=True) for item in items]

        lemma = ' '.join(lemma for correct, lemma in corrects_lemmas)

        number_slot = tracker.get_slot('number')
        quantity = extract_number(number_slot)
        
        if  lemma in shopping_list:
            if shopping_list.get(lemma, 0) > (quantity):
                shopping_list[lemma] = shopping_list.get(lemma, 0) - (quantity)
            else:
                del(shopping_list[lemma])
                
        correct_spelling = ' '.join(correct for correct, lemma in corrects_lemmas)


        dispatcher.utter_message(text=f"I've just removed {correct_spelling} from the shopping list!")
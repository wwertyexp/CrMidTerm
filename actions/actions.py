# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
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

def get_slot(slot_name, tracker: Tracker):
    """return the slot and prevent multiple slot values"""
    item = tracker.get_slot(slot_name)
    if type(item) is list:
        return item[0]
    return item

class ActionAdd(Action):

    def name(self) -> Text:
        return "action_add"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        item = get_slot('item_to_add',tracker)
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
        
        item = next(tracker.get_latest_entity_values('item'), None)
        if item is not None:
            items = item.split()
            corrects_lemmas = [get_word_lemma(item,debug=True) for item in items]
            lemma = ' '.join(lemma for correct, lemma in corrects_lemmas)
            correction = ' '.join(correct for correct, lemma in corrects_lemmas)
            if lemma not in shopping_list:
                text = 'Shopping list:\n'+'\n'.join(
                    f'{key}: {shopping_list[key]}' for key in sorted(shopping_list))
            else:
                text = f'There are {shopping_list[lemma]} {correction} in the list.'
        else:
            text = 'Shopping list:\n'+'\n'.join(
                f'{key}: {shopping_list[key]}' for key in sorted(shopping_list))

        dispatcher.utter_message(text=text)

        return [AllSlotsReset()]


class ActionRemove(Action):

    def name(self) -> Text:
        return "action_remove"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item = get_slot('item_to_remove', tracker)
        items = item.split()
        corrects_lemmas = [get_word_lemma(item,debug=True) for item in items]

        lemma = ' '.join(lemma for correct, lemma in corrects_lemmas)

        number_slot = tracker.get_slot('number')
        quantity = extract_number(number_slot)
        if quantity <0: quantity = float('inf')
        
        correct_spelling = ' '.join(correct for correct, lemma in corrects_lemmas)

        if  lemma in shopping_list:
            if shopping_list.get(lemma, 0) > (quantity):
                shopping_list[lemma] = shopping_list.get(lemma, 0) - (quantity)
            else:
                del(shopping_list[lemma])
            
            if quantity==float('inf'): quantity = 'every'
            dispatcher.utter_message(text=f"I've just removed {quantity} {correct_spelling} from the shopping list!")
        else:
            dispatcher.utter_message(text=f"There are no {correct_spelling} in the shopping list!")

        return [AllSlotsReset()]

class ValidateAddItemForm(FormValidationAction):

    def name(self):
        return 'validate_item_quantity_form'
    
    def validate_number(
        self,
        slot_value,
        dispatcher,
        tracker,
        domain
    ):
        """Validate the number of items to add in the list"""
        number = extract_number(slot_value)
        if (number < 0):
            dispatcher.utter_message(text="Sorry, I didn't get that.")
            return {'number':None}
        return {'number':slot_value}

class ActionDestoryList(Action):

    def name(self) -> Text:
        return "action_destroy_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            shopping_list.clear()
            dispatcher.utter_message(text="Your list is empty now.")

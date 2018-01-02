import random

class Player(object):

    def __init__(self,name):
        self.cash = 1000
        self.name = name

    def add_cash(self,amount):
        self.cash += amount

    def remove_cash(self,amount):
        self.cash -= amount


class Card(object):

    valid_pips = ('Jack','Queen','King','Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten')
    valid_suits = ('Hearts','Diamonds','Clubs','Spades')
    valid_scores = {'Jack': 10,
                    'Queen': 10,
                    'King': 10,
                    'Ace': [1,10],
                    'Two': 2,
                    'Three': 3,
                    'Four': 4,
                    'Five': 5,
                    'Six': 6,
                    'Seven': 7,
                    'Eight': 8,
                    'Nine': 9,
                    'Ten': 10
    }

    def __init__(self,card_pip,suit_name):


        if card_pip not in Card.valid_pips or suit_name not in Card.valid_suits:
            print("Your entered card values on not correct!")
            print('Valid cards: %s' %Card.valid_pips)
            print('Valid suits: %s' %Card.valid_suits)
            raise ValueError()
        else:
            self.card_pip = card_pip
            self.suit_name = suit_name
            self.card_name = self.card_pip + ' of ' + self.suit_name
            self.card_score = Card.valid_scores[self.card_pip]


class CardPack(Card):

    def __init__(self):
        self.deck = []

        self.reset_pack(6) #It's popular in casinos to use 6 packs for the deck
        self.shuffle_pack()

    def nb_of_cards(self):
        return len(self.deck)

    def display_list_of_cards(self):
        for card in self.deck:
            print(card.card_name)
        
    def reset_pack(self,nb_of_packs = 1):
        '''Recreate the pack with its cards'''
        '''nb_of_packs(optional) will allow you to create multi-pack deck of cards'''

        for pack in range(1,nb_of_packs):

            for suit_nb in range(0,4):
                
                for pip_nb in range(0,13):
                    card = Card(CardPack.valid_pips[pip_nb],CardPack.valid_suits[suit_nb])

                    self.deck.append(card)

    def shuffle_pack(self):
        random.shuffle(self.deck)


    def deal_card(self):
        if self.nb_of_cards() > 0:
            return self.deck.pop()
        else:
            return None




    




    


    
    
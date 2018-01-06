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
                    'Ace': 11, #[1,11] - I'm just too lazy to add the code to decide between 1 & 11 at run-time
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


class Game(object):

    def __init__(self):

        self.round_dealt_cards = []
        self.dealer_points = 0 # - Change to list later on - For each Ace card dealt there will be another possible score (11 or 1) 
        self.player_points = 0
        self.player_turn = 'Player'
        self.bet = 0
        self.game_status = 'Run'

    def reset_round_dealt_cards(self):
        self.round_dealt_cards.clear()

    def change_player_turn(self):
        if self.player_turn == 'Player':
            self.player_turn = 'Dealer'
        else:
            self.player_turn = 'Player'

    def get_player_bet(self,player):
        
        while True:
            entered_amount = int(input('How much would you like to bet (0 to exit)?'))
            if entered_amount == 0:
                self.game_status = 'End'
                break
            else:
                if player.cash >= entered_amount:
                    player.cash -= entered_amount
                    self.bet = entered_amount
                    break
                else:
                    print('%s does not have enough cash for that bet' %player.name)

    def check_score(self):
        '''What's the score of the cards in round_dealt_cards'''
        total_score = 0

        for card in self.round_dealt_cards:
            total_score += card.card_score

        return total_score

    def deal_turn(self, deck, player):
        '''Deal until bust or stay '''
        
        if self.player_turn == 'Dealer':
            name_being_dealt = self.player_turn
        else:
            name_being_dealt = self.player_turn + ' '  + player.name

        print('%s is dealt 2 cards:' %name_being_dealt)

        self.round_dealt_cards.append(deck.deal_card())
        print('\tCard [%i] is %s' %(len(self.round_dealt_cards),self.round_dealt_cards[-1].card_name))
        
        self.round_dealt_cards.append(deck.deal_card())
        print('\tCard [%i] is %s' %(len(self.round_dealt_cards),self.round_dealt_cards[-1].card_name))

        self.player_points = self.check_score()

        player_action = ''

        while not (player_action == 'S' or self.player_points > 21 or self.dealer_points > 21): # deal till bust or stay

            if self.player_turn == 'Dealer':
                if self.dealer_points <= self.player_points:
                    player_action = 'H'
                    print('%s has chosen to Hit' %name_being_dealt)
                    x = input('Press <Enter> to continue....')
                else:
                    player_action = 'S'
                    
            else:
                player_action = input('Hit or Stay? (H or S)') 
            
            if player_action.upper() == 'H':
                self.round_dealt_cards.append(deck.deal_card())
                print('\tCard [%i] is %s' %(len(self.round_dealt_cards),self.round_dealt_cards[-1].card_name))
                if self.player_turn == 'Player':
                    self.player_points = self.check_score()
                else:
                    self.dealer_points = self.check_score()

        if self.player_turn == 'Player':
            if self.player_points > 21:
                print('%s has bust on %s' %(name_being_dealt, self.player_points) )
            else:
                print('%s has stayed on %s' %(name_being_dealt, self.player_points) )
        else:
            if self.dealer_points > 21:
                print('%s has bust on %s' %(name_being_dealt, self.dealer_points) )
            else:
                print('%s has stayed on %s' %(name_being_dealt, self.dealer_points) )


    def play(self):
        
        player = Player(input('Enter player Name:'))
        deck = CardPack()

        print('%s starts with %s dollars' %(player.name, player.cash))

        self.get_player_bet(player)

        if self.game_status == 'End':
            return
        
        #Player's turn
        self.deal_turn(deck, player)
        if self.player_points > 21:
            print("The dealer has won and the house take's all")
        else:    
            #Dealer's turn
            self.change_player_turn() 
            self.reset_round_dealt_cards()
            self.deal_turn(deck, player)
            if self.dealer_points > 21:
                print("The dealer has lost and the player take's all")
                player.add_cash(self.bet*2)
            else:
                print("The dealer has won and the house take's all")
                
        print('Player has $%s cash' %player.cash)

        x = input('Press <Enter> to continue....')


game = Game()
game.play()
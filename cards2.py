import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):

        self.deck = []  # Start with an empty list

        for suit in suits:
            for rank in ranks:
                # Create the Card Object
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# test_deck = Deck()
# test_deck.shuffle()
# print(test_deck)


class Hand:

    def __init__(self):
        self.cards = []  # Start with an empty list as we did in the Deck class
        self.value = 0  # Start with zero value
        self.aces = 0  # Add an attribute to keep track of aces

    def add_card(self, card):
        # Card passed in
        # From Deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # Track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THAN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


# test_deck = Deck()
# test_deck.shuffle()
#
# # PLAYER
# test_player = Hand()
# # Deal 1 card from the deck Card(suit, rank)
# pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.add_card(pulled_card)
# print(test_player.value)
# # Nine of Hearts
# # 9
#
# test_player.add_card(test_deck.deal())
# print(test_player.value)
# # 10


class Chips:

    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! You have: {}'.format(chips.total))
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # To control an upcoming while loop

    while True:
        x = input('Hit or Stand? Enter h or s ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False

        else:
            print("Sorry, I did no understand that, Please enter h or s only!")
            continue
        break


def show_some(player, dealer):
    # dealer.cards[1]
    # Show only ONE of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all (2 cards) of the player's hand/cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    # Show all the dealer's cards
    print("\n Dealer's hand:")
    for card in dealer.cards:
        print(card)

    print("\n Dealer's hand: ", *dealer.cards, sep='\n')
    # Calculate and display value (J+K == 20)
    print(f"Value of Dealer's hand is: {dealer.value}")

    # Show all the players cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")


def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and player tie! PUSH')


while True:
    # Print an opening statement

    print("WELCOME TO BLACKJACK")
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # Recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:  # instead of player_hand.value can be written 17,
            # but it can not change a lot (only if you know BlackJack)
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))
    # Ask to play again
    new_game = input("Would you like to play another hand? y/n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break

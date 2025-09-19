import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        values = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}
        value_name = values.get(self.value, str(self.value))
        return f"{value_name} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        for suit in suits:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]
        for i in range(13):
            for j in range(num_players):
                if self.cards:
                    hands[j].append(self.cards.pop())
        return hands

def select_trump(players_hands):
    dealer = random.randint(0, 3)
    print(f"Player {dealer + 1} is the dealer and chooses trump.")
    
    print(f"Player {dealer + 1}'s first 5 cards:")
    for card in players_hands[dealer][:5]:
        print(" ", card)
    
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    trump_suit = random.choice(suits)
    print(f"Trump suit is: {trump_suit}")
    
    return dealer, trump_suit

def play_round(players_hands, trump_suit, starting_player):
    trick = []
    for i in range(4):
        player_index = (starting_player + i) % 4
        if players_hands[player_index]:
            card = random.choice(players_hands[player_index])
            players_hands[player_index].remove(card)
            trick.append((player_index, card))
            print(f"Player {player_index + 1} plays: {card}")
    
    winner_index = determine_winner(trick, trump_suit)
    print(f"Player {winner_index + 1} wins the trick!\n")
    return winner_index

def determine_winner(trick, trump_suit):
    winning_card = None
    winner_index = None
    for player_index, card in trick:
        if winning_card is None:
            winning_card = card
            winner_index = player_index
        else:
            if card.suit == trump_suit and winning_card.suit != trump_suit:
                winning_card = card
                winner_index = player_index
            elif card.suit == trump_suit and winning_card.suit == trump_suit:
                if card.value > winning_card.value:
                    winning_card = card
                    winner_index = player_index
            elif card.suit == trick[0][1].suit and winning_card.suit != trump_suit:
                if card.value > winning_card.value:
                    winning_card = card
                    winner_index = player_index
    return winner_index

def calculate_score(tricks_won):
    team1_tricks = tricks_won[0] + tricks_won[2]  # Players 1 and 3
    team2_tricks = tricks_won[1] + tricks_won[3]  # Players 2 and 4
    
    print(f"Team 1 (Players 1 & 3) won {team1_tricks} tricks.")
    print(f"Team 2 (Players 2 & 4) won {team2_tricks} tricks.")
    
    if team1_tricks > team2_tricks:
        print("Team 1 wins the game!")
    elif team2_tricks > team1_tricks:
        print("Team 2 wins the game!")
    else:
        print("It's a tie!")

# اجرای اصلی بازی
deck = Deck()
deck.shuffle()
players_hands = deck.deal(4)

dealer, trump_suit = select_trump(players_hands)

print("\n--- Starting the game ---")
current_player = dealer
tricks_won = [0, 0, 0, 0]  # تعداد دست‌های برده شده توسط هر بازیکن

for trick_number in range(13):
    print(f"--- Trick {trick_number + 1} ---")
    winner_index = play_round(players_hands, trump_suit, current_player)
    tricks_won[winner_index] += 1
    current_player = winner_index

print("Game over!")
calculate_score(tricks_won)


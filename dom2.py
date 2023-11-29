import random
from random import shuffle

# Base Card class
class Card:
    def __init__(self, value, cost):
        self.value = value
        self.cost = cost

    def __str__(self):
        return self.__class__.__name__

# Specific Card types
class CopperCard(Card):
    def __init__(self):
        super().__init__(1, 0)

class SilverCard(Card):
    def __init__(self):
        super().__init__(2, 3)

class GoldCard(Card):
    def __init__(self):
        super().__init__(3, 6)

class EstateCard(Card):
    def __init__(self):
        super().__init__(1, 2)

class DuchyCard(Card):
    def __init__(self):
        super().__init__(3, 5)

class ProvinceCard(Card):
    def __init__(self):
        super().__init__(6, 8)

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.coins = 0
        self.buys = 1
        self.hand = []
        self.discard = []
        self.deck = []

    def draw(self, num_cards):
        while num_cards > 0 and (self.deck or self.discard):
            if not self.deck:
                self.deck, self.discard = self.discard, []
                shuffle(self.deck)
            self.hand.append(self.deck.pop())
            num_cards -= 1

    def play(self, card):
        if card in self.hand:
            self.discard.append(card)
            self.hand.remove(card)
            self.coins += card.value
            print(f"{self.name} played {card}")
        else:
            print(f"{card} is not in your hand.")

    def buy(self, card, supply):
        if card in supply and supply[card] > 0 and card.cost <= self.coins and self.buys > 0:
            self.discard.append(card)
            self.coins -= card.cost
            self.buys -= 1
            supply[card] -= 1
            print(f"{self.name} bought {card}")
        else:
            print("You cannot buy that card.")

    def cleanup(self):
        self.discard.extend(self.hand)
        self.hand = []
        self.draw(5)
        self.buys = 1
        self.coins = 0

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

# Game class
class Game:
    def __init__(self):
        self.supply = {}
        self.players = []
        self.card_instances = {
            CopperCard: CopperCard(),
            SilverCard: SilverCard(),
            GoldCard: GoldCard(),
            EstateCard: EstateCard(),
            DuchyCard: DuchyCard(),
            ProvinceCard: ProvinceCard()
        }

    def add_player(self, player):
        self.players.append(player)

    def initialize(self):
        # Initialize supply
        card_quantities = {
            CopperCard: 40,
            SilverCard: 30,
            GoldCard: 30,
            EstateCard: 14,
            DuchyCard: 10,
            ProvinceCard: 10
        }
        for card_class, quantity in card_quantities.items():
            self.supply[self.card_instances[card_class]] = quantity

        # Initialize player decks
        for player in self.players:
            player.deck.extend([self.card_instances[CopperCard] for _ in range(7)])
            player.deck.extend([self.card_instances[EstateCard] for _ in range(3)])
            shuffle(player.deck)

    def show_supply(self):
        return ', '.join(f"{card}: {quantity}" for card, quantity in self.supply.items() if quantity > 0)

    def play(self):
        turn = 0
        province_card = self.card_instances[ProvinceCard]
        while self.supply[province_card] > 0:
            for player in self.players:
                player.draw(5)
                player.coins = sum(card.value for card in player.hand)
                player.buys = 1

                print(f"\n{player.name}'s Turn")
                print(f"Hand: {player.show_hand()}")
                print(f"Coins: {player.coins}, Buys: {player.buys}")
                print(f"Supply: {self.show_supply()}")

                # Player's choice to play cards
                while True:
                    choice = input(f"{player.name}, do you want to play a card from your hand? (yes/no) ")
                    if choice.lower() == 'yes':
                        card_name = input("Enter the name of the card you want to play: ")
                        for card in player.hand:
                            if card.__class__.__name__.lower() == card_name.lower():
                                player.play(card)
                                break
                        else:
                            print("Invalid card name.")
                    elif choice.lower() == 'no':
                        break

                # Player's choice to buy cards
                while player.buys > 0:
                    choice = input(f"{player.name}, do you want to buy a card from the supply? (yes/no) ")
                    if choice.lower() == 'yes':
                        card_name = input("Enter the name of the card you want to buy: ")
                        for card in self.supply:
                            if card.__class__.__name__.lower() == card_name.lower():
                                player.buy(card, self.supply)
                                break
                        else:
                            print("Invalid card name.")
                    elif choice.lower() == 'no':
                        break

                player.cleanup()
                print(f"\nEnd of {player.name}'s turn.")
                input("Press Enter to continue...")

            turn += 1

        # Calculate final scores
        print("\nGame Over! Final Scores:")
        for player in self.players:
            score = sum(card.value for card in player.discard)
            print(f"{player.name}: {score}")

# Setting up the game
random.seed(0)
game = Game()
player1_name = input("Enter name for Player 1: ")
player2_name = input("Enter name for Player 2: ")
game.add_player(Player(player1_name))
game.add_player(Player(player2_name))
game.initialize()
game.play()


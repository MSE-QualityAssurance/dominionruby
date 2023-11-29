import tkinter as tk
from tkinter import simpledialog, messagebox
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
# GUI Class
class DominionGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Dominion Game")
        self.current_player_index = 0

        # Setup the game board
        self.setup_board()
        self.update_board()

    def setup_board(self):
        # Frame for Player Hands
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack()

        self.player_hand_labels = []
        for i in range(len(self.game.players)):
            label = tk.Label(self.player_frame, text="")
            label.pack()
            self.player_hand_labels.append(label)

        # Frame for Supply
        self.supply_frame = tk.Frame(self.root)
        self.supply_frame.pack()

        self.supply_label = tk.Label(self.supply_frame, text="")
        self.supply_label.pack()

        # Control Buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        self.play_card_button = tk.Button(self.control_frame, text="Play Card", command=self.play_card)
        self.play_card_button.pack(side=tk.LEFT)

        self.buy_card_button = tk.Button(self.control_frame, text="Buy Card", command=self.buy_card)
        self.buy_card_button.pack(side=tk.LEFT)

        self.end_turn_button = tk.Button(self.control_frame, text="End Turn", command=self.end_turn)
        self.end_turn_button.pack(side=tk.LEFT)

    def play_card(self):
        player = self.game.players[self.current_player_index]
        card_name = simpledialog.askstring("Play Card", "Enter the name of the card you want to play:", parent=self.root)
        if card_name:
            for card in player.hand:
                if card.__class__.__name__.lower() == card_name.lower():
                    player.play(card)
                    self.update_board()
                    break
            else:
                messagebox.showerror("Error", "Invalid card name.")

    def buy_card(self):
        player = self.game.players[self.current_player_index]
        card_name = simpledialog.askstring("Buy Card", "Enter the name of the card you want to buy:", parent=self.root)
        if card_name:
            for card in self.game.supply:
                if card.__class__.__name__.lower() == card_name.lower() and self.game.supply[card] > 0:
                    player.buy(card, self.game.supply)
                    self.update_board()
                    break
            else:
                messagebox.showerror("Error", "Invalid card name or card not available.")

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.game.players)
        self.game.players[self.current_player_index].cleanup()
        self.update_board()

    def update_board(self):
        for i, player in enumerate(self.game.players):
            self.player_hand_labels[i].config(text=f"{player.name}'s Hand: {player.show_hand()}")
        self.supply_label.config(text=f"Supply: {self.game.show_supply()}")

    def run(self):
        self.root.mainloop()

# Initialize the game
random.seed(0)
game = Game()
player1 = Player("Player 1")
player2 = Player("Player 2")
game.add_player(player1)
game.add_player(player2)
game.initialize()

# Run the GUI
app = DominionGUI(game)
app.run()


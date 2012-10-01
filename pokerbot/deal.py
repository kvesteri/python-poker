from copy import copy
from itertools import combinations

from .action import Action
from .deck import Deck
from .board import Board
from .hand import Hand, HoldEmStartingHand


class Busto(Exception):
    pass


class BetTooMuch(Exception):
    pass


class IllegalAction(Exception):
    pass


class ActOutOfTurn(Exception):
    pass


class Deal(object):
    phases = [None, 'pre-flop', 'flop', 'turn', 'river']

    def __init__(self, table):
        self.table = table
        self.player_dict = copy(table.player_dict)
        self.seats = copy(table.seats)
        self.actions = []
        self.starting_hands = {}
        self.deck = Deck()
        self.phase = None
        self.board = Board()
        self.pot = 0
        self.players_involved = copy(table.seats)
        self.player_to_act_index = 0

        self.betting_rounds = {}
        for phase in self.phases[1:]:
            self.betting_rounds[phase] = {}
            for player in self.seats:
                self.betting_rounds[phase][player.name] = 0

    def add_action(self, player, type, amount=None):
        if player != self.player_to_act:
            raise ActOutOfTurn()

        if player not in self.players_involved:
            raise IllegalAction()

        bets = self.betting_rounds[self.phase]

        if type == 'call':
            amount = max(bets.values()) - bets[player.name]
            if amount == 0:
                raise IllegalAction()  # should check instead of call
            self.put_in_pot(player, amount)
        elif type == 'bet':
            if self.table.balances[player.name] < amount:
                raise BetTooMuch()
            self.put_in_pot(player, amount)
        elif type == 'check':
            if bets[player.name] < max(bets.values()):
                raise IllegalAction()
        elif type == 'fold':
            self.players_involved.remove(player)

        self.actions.append(Action(self, player, type, amount, self.phase))
        self.player_to_act_index += 1
        if self.player_to_act_index > len(self.players_involved) - 1:
            self.player_to_act_index = 0

    @property
    def hands(self):
        hands = []
        for player_name in self.players:
            hand = self.get_hand(player_name)
            hands.append(hand)
        return hands

    @property
    def winner(self):
        hands = sorted(self.hands, key=lambda a: a.score)
        name = hands[0].player_name
        return self.player_dict[name]

    def get_hand(self, player_name):
        starting_hand = self.starting_hands[player_name]
        # find all 5-card combinations and map them into hands
        hands = list(
            map(Hand, combinations(starting_hand.cards + self.board.cards, 5))
        )

        hands = sorted(hands, key=lambda a: a.score)
        hand = hands[0]
        hand.player_name = player_name
        return hand

    def deal_preflop(self, cards={}):
        self.phase = 'pre-flop'
        for name, player in self.player_dict.items():
            if name in cards:
                self.starting_hands[name] = HoldEmStartingHand(cards[name])
            else:
                self.starting_hands[name] = HoldEmStartingHand(
                    self.deck.draw(2)
                )
            if player == self.table.button_player:
                self.put_in_pot(
                    player,
                    self.table.big_blind_size / 2
                )
            else:
                self.put_in_pot(
                    player,
                    self.table.big_blind_size
                )

    def put_in_pot(self, player, amount):
        self.table.balances[player.name] -= amount
        self.pot += amount
        self.betting_rounds[self.phase][player.name] += amount

    def deal_flop(self, cards=[]):
        self.phase = 'flop'
        if cards:
            self.board.cards += cards
        else:
            self.board.cards += self.deck.draw(3)

    def deal_turn(self, cards=[]):
        self.phase = 'turn'
        if cards:
            self.board.cards += cards
        else:
            self.board.cards += self.deck.draw(1)

    def deal_river(self, cards=[]):
        self.phase = 'river'
        if cards:
            self.board.cards += cards
        else:
            self.board.cards += self.deck.draw(1)

    @property
    def player_to_act(self):
        """
        Returns the current player to act (if any).
        """
        return self.players_involved[self.player_to_act_index]

    @property
    def button_player(self):
        """
        Returns the player who is sitting on the button on this deal.
        """
        return self.table.button_player

    @property
    def all_players_acted(self):
        players = set(self.seats)
        acted_players = set([
            action.player for action in self.actions
            if action.phase == self.phase
        ])
        return players == acted_players

    def is_betting_closed(self):
        if self.phase == "pre-flop":
            pass

    def is_dealt(self, phase):
        pass

    def relative_strength(self, starting_hand):
        if self.is_dealt('river'):
            raise Exception('''
                Relative strength only available for flop and turn phases
                ''')

    def absolute_strength(self, starting_hand):
        pass

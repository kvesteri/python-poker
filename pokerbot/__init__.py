from itertools import combinations
from .card import Card
from .hand import Hand
from .range import Range


class CardCollection(object):
    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        return ''.join([str(card) for card in self.cards])


class Board(CardCollection):
    pass


class StartingHand(CardCollection):
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort()
        self.cards.reverse()

    def absolute_strength():
        raise NotImplementedError

    def relative_strength():
        raise NotImplementedError


class HoldEmStartingHand(StartingHand):
    def absolute_strength():
        raise NotImplementedError

    def relative_strength():
        raise NotImplementedError


class Player():
    def __init__(self, name, balance=1000):
        self.name = name
        self.balance = balance

    def bet(self, deal, amount):
        deal.add_action(self, 'bet', amount)

    def check(self, deal):
        deal.add_action(self, 'check')

    def fold(self, deal):
        deal.add_action(self, 'fold')

    def join_table(self, table, buyin):
        table.players[self.name] = (self, buyin)


class RandomAIPlayer(Player):
    pass


class Action(object):
    types = ('bet', 'check', 'fold')
    phases = ('flop', 'turn', 'river')

    def __init__(self, deal, player, type, amount):
        self.deal = deal
        self.player = player
        self.type = type
        self.amount = amount


class Deal(object):
    phases = [None, 'pre-flop', 'flop', 'turn', 'river']

    def __init__(self, players):
        self.players = players
        self.actions = []
        self.starting_hands = {}
        self.deck = Deck()
        self.phase = None
        self.board = Board()

    def add_action(self, player, type, amount):
        self.actions.append(Action(self, player, type, amount))

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
        return self.players[name][0]

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
        for name in self.players:
            if name in cards:
                self.starting_hands[name] = HoldEmStartingHand(cards[name])
            else:
                self.starting_hands[name] = HoldEmStartingHand(
                    self.deck.draw(2)
                )

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

    def is_dealt(self, phase):
        pass

    def relative_strength(self, starting_hand):
        if self.is_dealt('river'):
            raise Exception('''
                Relative strength only available for flop and turn phases
                ''')

    def absolute_strength(self, starting_hand):
        pass


class Table(object):
    def __init__(self):
        self.deals = []
        self.players = {}

    def add_player(self, player, buyin):
        self.players[player.name] = (player, buyin)

    def new_deal(self):
        if not self.players:
            raise Exception("Can't deal new hand. No players at the table")
        if len(self.players.keys()) == 1:
            raise Exception(
                "Can't deal new hand. Only one player present at the table"
            )
        deal = Deal(self.players)
        self.deals.append(deal)
        return deal

    def get_balance(self, player_name):
        return self.players[player_name][1]

    def get_player(self, player_name):
        return self.players[player_name][0]

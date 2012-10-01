from pytest import raises
from pokerbot import Table, Player
from pokerbot.card import Card
from pokerbot.deal import (
    ActOutOfTurn, BetTooMuch, Busto, IllegalAction, PlayersNotActed
)


class DealTestCase(object):
    def setup_method(self, method):
        self.table = Table()
        self.john = Player(name=u'John')
        self.phil = Player(name=u'Phil')
        self.table.add_player(self.john, 100)
        self.table.add_player(self.phil, 100)
        self.deal = self.table.new_deal()


class TestDealPreFlop(DealTestCase):
    def test_all_players_acted(self):
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })
        self.john.call(self.deal)
        assert not self.deal.all_players_acted
        self.phil.check(self.deal)
        assert self.deal.all_players_acted

    def test_puts_blinds_to_pot(self):
        assert self.deal.pot == 0
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })
        assert self.deal.pot == 3

    def test_player_to_act(self):
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })
        assert self.deal.player_to_act == self.john

    def test_raises_error_if_player_acts_out_of_turn(self):
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })
        with raises(ActOutOfTurn):
            self.phil.call(self.deal)


class TestDealFlop(DealTestCase):
    def setup_method(self, method):
        DealTestCase.setup_method(self, method)
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })

    def test_raises_exception_if_all_players_havent_acted(self):
        with raises(PlayersNotActed):
            self.deal.deal_flop([Card('6s'), Card('7s'), Card('Ks')])


class TestDealTurn(DealTestCase):
    def setup_method(self, method):
        DealTestCase.setup_method(self, method)
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })

    def test_raises_exception_if_all_players_havent_acted(self):
        self.john.call(self.deal)
        self.phil.check(self.deal)
        self.deal.deal_flop([Card('6s'), Card('7s'), Card('Ks')])
        with raises(PlayersNotActed):
            self.deal.deal_turn([Card('7d')])


class TestDealRiver(DealTestCase):
    def setup_method(self, method):
        DealTestCase.setup_method(self, method)
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })

    def test_raises_exception_if_all_players_havent_acted(self):
        self.john.call(self.deal)
        self.phil.check(self.deal)
        self.deal.deal_flop([Card('6s'), Card('7s'), Card('Ks')])
        self.john.check(self.deal)
        self.phil.check(self.deal)
        self.deal.deal_turn([Card('Kc')])
        with raises(PlayersNotActed):
            self.deal.deal_river([Card('2s')])


class ActionTestCase(DealTestCase):
    def setup_method(self, method):
        DealTestCase.setup_method(self, method)
        self.deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })


class TestFoldAction(ActionTestCase):
    def test_fold_removes_player_from_involved_players_list(self):
        self.john.fold(self.deal)
        assert self.deal.players_involved == [self.phil]


class TestCheckAction(ActionTestCase):
    def test_check_raises_illegal_action_if_not_enough_money_put_in_pot(self):
        with raises(IllegalAction):
            self.john.check(self.deal)


class TestCallAction(ActionTestCase):
    def test_call_puts_money_in_pot(self):
        self.john.call(self.deal)
        assert self.deal.pot == 4

    def test_raises_exception_if_check_is_sufficient_instead_of_call(self):
        self.john.call(self.deal)
        with raises(IllegalAction):
            self.phil.call(self.deal)


class TestBetAction(ActionTestCase):
    def test_bet_raises_illegal_action_if_not_enough_balance(self):
        with raises(BetTooMuch):
            self.john.bet(self.deal, 100)

    def test_bet_puts_money_in_pot(self):
        self.john.bet(self.deal, 5)
        assert self.deal.pot == 8

    def test_player_is_no_longer_involved_if_he_is_allin(self):
        self.john.bet(self.deal, 99)
        assert self.deal.players_involved == [self.phil]

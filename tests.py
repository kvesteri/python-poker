from pytest import raises
from pokerbot import Card, Deal, Hand, Table, Player, Range
from pokerbot.hand_eval import Two


class TestCard(object):
    def test_rank(self):
        card = Card(9, 1)
        assert card.rank == 9


class TestTwoCardEval(object):
    def test_evaluate_rank(self):
        assert Two.evaluate_rank([Card(14, 1), Card(13, 2)]) == 12
        assert Two.evaluate_rank([Card(14, 1), Card(13, 1)]) == 8
        #print len(range_.hands)

    def test_evaluate_percentile(self):
        assert Two.evaluate_percentile([Card(14, 1), Card(14, 2)]) == 1
        assert Two.evaluate_percentile([Card(14, 1), Card(14, 2)]) == 1


class TestRange(object):
    def test_top_5_percent_range_as_string(self):
        range_ = Range.top(0.05)
        assert str(range_) == '77+, AJs+, AKo+'

    def test_top_10_percent_range_as_string(self):
        range_ = Range.top(0.10)
        assert str(range_) == '66+, A8s+, ATo+'

    def test_top_20_percent_range_as_string(self):
        range_ = Range.top(0.20)
        assert str(range_) == '55+, A3s+, K9o+'

    def test_top_30_percent_range_as_string(self):
        range_ = Range.top(0.30)
        assert str(range_) == '44+, J9s+, Q9o+'

    def test_top_40_percent_range_as_string(self):
        range_ = Range.top(0.40)
        assert str(range_) == '33+, T8s+, K4o+'

    def test_top_50_percent_range_as_string(self):
        range_ = Range.top(0.50)
        assert str(range_) == '22+, J5s+, T8o+'

    def test_paired_range_from_string(self):
        range_ = Range.from_str('66+')
        assert str(range_) == '66+'

    def test_suited_range_from_string(self):
        range_ = Range.from_str('79s+')
        assert str(range_) == '97s+'

    def test_supports_length(self):
        range_ = Range.from_str('97s+')
        assert len(range_) == 176

    def test_all_hands(self):
        range_ = Range.top(1)
        assert len(range_) == 1326

    def test_range_of_AA(self):
        range_ = Range.from_str('AA')
        assert len(range_) == 6

    def test_bottom_10_percent_range_as_string(self):
        range_ = Range.bottom(0.1)


class TestTable(object):
    # def test_new_deal_fails_if_no_players_present(self):
    #     with raises(Exception):
    #         table = Table()
    #         table.new_deal()

    # def test_new_deal_fails_if_only_player_present(self):
    #     with raises(Exception):
    #         table = Table()
    #         table.add_player(Player(name=u'Baller'), 100)
    #         table.new_deal()

    def test_new_deal(self):
        table = Table()
        table.add_player(Player(name=u'Marjo'), 100)
        table.add_player(Player(name=u'Konsta'), 100)
        deal = table.new_deal()
        deal.deal_preflop({
            'Konsta': [Card('Ad'), Card('Kd')],
            'Marjo': [Card('As'), Card('5c')]
        })

        print "--- GAME BEGINS ---"
        for name, hand in deal.starting_hands.items():
            print name, str(hand)

        deal.deal_flop([Card('6s'), Card('7s'), Card('Ks')])
        deal.deal_turn([Card('Kc')])
        deal.deal_river([Card('2s')])

        print 'Final board :', deal.board
        hand1 = deal.get_hand('Konsta')
        hand2 = deal.get_hand('Marjo')

        print 'Marjon käsi :', hand2, hand2.score
        print 'Konsta käsi :', hand1, hand1.score

        print "Winner is: %s" % deal.winner.name


# class TestHand(object):
#     def test_hand_list_sorting(self):
#         list_of_hands = [
#             Hand([
#                 Card(2, 'c'),
#                 Card(3, 'c'),
#                 Card(8, 'd'),
#                 Card(8, 'c'),
#                 Card(10, 's')
#             ]),
#             Hand([
#                 Card(2, 's'),
#                 Card(3, 's'),
#                 Card(4, 's'),
#                 Card(5, 's'),
#                 Card(6, 's')
#             ]),
#             Hand([
#                 Card(2, 's'),
#                 Card(3, 'c'),
#                 Card(4, 's'),
#                 Card(5, 's'),
#                 Card(6, 's')
#             ])
#         ]
#         list_of_hands.sort()
#         #print list_of_hands

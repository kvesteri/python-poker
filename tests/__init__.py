from pytest import raises
from pokerbot import Card, Deal, Hand, Table, Player, Range
from pokerbot.hand_eval import Two


class TestCard(object):
    def test_rank(self):
        card = Card(9, 1)
        assert card.rank == 9


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
        john = Player(name=u'John')
        phil = Player(name=u'Phil')
        table.add_player(john, 100)
        table.add_player(phil, 100)
        deal = table.new_deal()
        deal.deal_preflop({
            'John': [Card('Ad'), Card('Kd')],
            'Phil': [Card('As'), Card('5c')]
        })

        print "--- GAME BEGINS ---"
        for name, hand in deal.starting_hands.items():
            print name, str(hand)

        deal.deal_flop([Card('6s'), Card('7s'), Card('Ks')])
        deal.deal_turn([Card('Kc')])
        deal.deal_river([Card('2s')])

        print 'Final board :', deal.board
        hand1 = deal.get_hand('John')
        hand2 = deal.get_hand('Phil')

        print 'John :', hand2, hand2.score
        print 'Phil :', hand1, hand1.score

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

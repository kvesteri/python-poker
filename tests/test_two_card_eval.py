from pokerbot import Card
from pokerbot.hand_eval import Two


class TestTwoCardEval(object):
    def test_evaluate_rank(self):
        assert Two.evaluate_rank([Card(14, 1), Card(13, 2)]) == 12
        assert Two.evaluate_rank([Card(14, 1), Card(13, 1)]) == 8

    def test_evaluate_percentile(self):
        assert Two.evaluate_percentile([Card(14, 1), Card(14, 2)]) == 1
        assert Two.evaluate_percentile([Card(14, 1), Card(14, 2)]) == 1


class TestBillChenPowerRank(object):
    def test_chen_power_rank_of_AA_is_20(self):
        assert Two.chen_power_rank([Card(14, 1), Card(14, 2)]) == 20

    def test_chen_power_rank_of_KK_is_16(self):
        assert Two.chen_power_rank([Card(13, 1), Card(13, 2)]) == 16

    def test_chen_power_rank_of_QQ_is_14(self):
        assert Two.chen_power_rank([Card(12, 1), Card(12, 2)]) == 14

    def test_chen_power_rank_of_AKs_is_14(self):
        assert Two.chen_power_rank([Card(14, 1), Card(13, 1)]) == 8


class TestRelativeRank(object):
    def test_relative_rank_of_AA_is_1(self):
        assert Two.relative_rank([Card(14, 1), Card(14, 2)]) == 1

    def test_relative_rank_of_KK_is_2(self):
        assert Two.relative_rank([Card(13, 1), Card(13, 2)]) == 2

    def test_relative_rank_of_QQ_is_3(self):
        assert Two.relative_rank([Card(12, 1), Card(12, 2)]) == 3

    def test_relative_rank_of_AKs_is_4(self):
        assert Two.relative_rank([Card(12, 1), Card(12, 2)]) == 4

    def test_relative_rank_of_JJ_is_4(self):
        assert Two.relative_rank([Card(12, 1), Card(12, 2)]) == 4

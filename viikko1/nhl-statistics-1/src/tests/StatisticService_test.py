import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_successful_player_search(self):
        self.assertEqual(self.stats.search("Kurri").name, "Kurri")
    
    def test_unsuccessful_player_search(self):
        player = self.stats.search("Hiltunen")

        self.assertIsNone(player)
    
    def test_team_search(self):
        team = self.stats.team("DET")

        self.assertEqual(team[0].name, "Yzerman")
    
    def test_top_points(self):
        top3 = self.stats.top(3, SortBy.POINTS)
        self.assertEqual(top3[0].name, "Gretzky")

    def test_top_goals(self):
        top3 = self.stats.top(3, SortBy.GOALS)
        self.assertEqual(top3[2].name, "Kurri")

    def test_top_assists(self):
        top3 = self.stats.top(3, SortBy.ASSISTS)       
        self.assertEqual(top3[3].name, "Kurri") 
class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._get_equal_scores()
        elif self.player1_score >= 4 or self.player2_score >= 4:
            return self._get_advantage_or_winner()
        else:
            return self._get_standard_score()

    def _get_equal_scores(self):
        if self.player1_score < 3:
            return f"{self.SCORE_NAMES[self.player1_score]}-All"
        else:
            return "Deuce"

    def _get_advantage_or_winner(self):
        score_difference = self.player1_score - self.player2_score

        if abs(score_difference) == 1:
            leading_player = self.player1_name if score_difference == 1 else self.player2_name
            return f"Advantage {leading_player}"
        else:
            leading_player = self.player1_name if score_difference >= 2 else self.player2_name
            return f"Win for {leading_player}"

    def _get_standard_score(self):
        score = ""
        for i, player_score in enumerate([self.player1_score, self.player2_score]):
            if i > 0:
                score += "-"
            score += self.SCORE_NAMES[player_score]
        return score

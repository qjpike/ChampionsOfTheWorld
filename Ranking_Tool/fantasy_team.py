class FantasyTeam:
    def __init__(self, name, data):
        self.name = name
        if type(data) is str:
            self.owner = data
            self.total_wins = 0
            self.h2h_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.total_h2h_wins = 0
            self.total_points = 0
            self.weekly_points = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.points_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.total_points_wins = 0
            self.ranks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif type(data) is dict:
            self.name = name
            self.owner = data["owner"]
            self.total_wins = data["total_wins"]
            self.h2h_wins = data["h2h_wins"]
            self.total_h2h_wins = data["total_h2h_wins"]
            self.total_points = data["total_points"]
            self.weekly_points = data["weekly_points"]
            self.points_wins = data["points_wins"]
            self.total_points_wins = data["total_points_wins"]
            self.ranks = data["ranks"]
        self.is_done = False

    def record_h2h_win(self, win, week):
        self.h2h_wins[week - 1] = 1 if win else 0
        self.total_h2h_wins = sum(self.h2h_wins)

    def record_points_win(self, week):
        self.points_wins[week - 1] = 1
        self.total_points_wins = sum(self.points_wins)

    def update_score(self, score, week):
        self.weekly_points[week - 1] = score
        self.total_points = sum(self.weekly_points)

    def update_cuml_stats(self):
        self.total_wins = self.total_h2h_wins + self.total_points_wins

    def __lt__(self, other):
        if self.total_wins > other.total_wins:
            return False
        elif self.total_wins < other.total_wins:
            return True
        elif self.total_h2h_wins > other.total_h2h_wins:  # if total wins are equal, compare total H2H Wins
            return False
        elif self.total_h2h_wins < other.total_h2h_wins:
            return True
        elif self.total_points > other.total_points: # if H2H wins are also equal, compare total points
            return False
        elif self.total_points < other.total_points:
            return True

        return False

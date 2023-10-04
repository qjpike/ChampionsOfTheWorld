import os
import json


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


def load_team_data():
    if os.path.exists("teams.json"):
        with open("teams.json", "r") as json_file:
            data = json.load(json_file)
        teams = {team_name: FantasyTeam(team_name, team) for team_name, team in data.items()}
    else:
        teams = {}
    return teams


def input_results_for_week(week, teams):
    print(f"Entering results for Week {week}:\n")
    available_teams = [team for team in teams if not teams[team].is_done]

    while len(available_teams):
        try:
            print(f"Select Team:")
            for i, team in enumerate(available_teams, start=1):
                print(f"{i}. {team} ({teams[team].owner})")

            team_number = input(f"Enter the number or 'q' to quit: ")
            if team_number.lower() == 'q':
                break  # Exit the loop if 'q' is entered

            team_number = int(team_number)
            if team_number < 1 or team_number > len(available_teams):
                print("Invalid team selection. Please choose a valid team.")
                continue

            team1 = available_teams[team_number - 1]
            teams[team1].is_done = True

            available_teams = [team for team in teams if not teams[team].is_done]

            print("Available opponents:")
            for i, team in enumerate(available_teams, start=1):
                print(f"{i}. {team} ({teams[team].owner})")

            team_number = input(f"Enter the number or 'q' to quit: ")
            if team_number.lower() == 'q':
                break  # Exit the loop if 'q' is entered

            team_number = int(team_number)
            if team_number < 1 or team_number > len(available_teams):
                print("Invalid team selection. Please choose a valid team.")
                continue

            team2 = available_teams[team_number - 1]
            teams[team2].is_done = True

            score = float(input(f"{team1}'s score: "))
            opponent_score = float(input(f"{team2}'s score: "))
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid data.")
            continue

        team = teams[team1]
        opponent = teams[team2]

        if score > opponent_score:
            team.record_h2h_win(True, week)
            opponent.record_h2h_win(False, week)
        elif opponent_score > score:
            team.record_h2h_win(False, week)
            opponent.record_h2h_win(True, week)

        team.update_score(score, week)
        opponent.update_score(opponent_score, week)

        available_teams = [team for team in teams if not teams[team].is_done]


def give_extra_wins(teams, week):
    sorted_teams = sorted(teams.values(), key=lambda x: (x.weekly_points[week-1]))[len(teams)//2:]
    for team in sorted_teams:
        team.record_points_win(week)


def display_rankings(teams, week):
    sorted_teams = sorted(teams.values(), reverse=True)
    for i, team in enumerate(sorted_teams):
        team.ranks[week - 1] = i + 1

    # Create the new rankings table for the current week as Markdown
    new_rankings_table = f"# Week {week} Rankings\n"
    new_rankings_table += "| Standings | Team | Owner | Wins Total | H2H Win (Week {}) | Points Win (Week {}) | Points For (Week {}) | H2H Wins (Cum'l) | Points Wins (Cum'l) | Points For (Cum'l) | +/- + |\n".format(week, week, week)
    new_rankings_table += "|:---------:|:----:|:-----:|:----------:|:----------------:|:-------------------:|:-------------------:|:----------------:|:-------------------:|:------------------:|:------:|\n"

    for i, team in enumerate(sorted_teams, start=1):
        if week == 1:
            rank_str = '-'
        else:
            rank_delta = team.ranks[week - 2] - team.ranks[week - 1]
            if rank_delta == 0:
                rank_str = '-'
            elif rank_delta > 0:
                rank_str = f'+{rank_delta}'
            else:
                rank_str = f'{rank_delta}'

        new_rankings_table += f"| {i} | {team.name} | {team.owner} | {team.total_wins} | {team.h2h_wins[week - 1]} | {team.points_wins[week - 1]} | {team.weekly_points[week - 1]:5.2f} | {team.total_h2h_wins} | {team.total_points_wins} | {team.total_points:5.2f} | {rank_str} |\n"
    new_rankings_table += "\n\n"
    # Save the new rankings table to the rankings.md file
    with open("rankings.md", "r+") as md_file:
        content = md_file.read()
        md_file.seek(0, 0)
        md_file.write(new_rankings_table + content)


def save_rankings_history(teams, week):
    # Save the team data to a JSON file
    with open(f"teams.json", "w") as json_file:
        data = {team.name: {
            "owner": team.owner,
            "total_wins": team.total_wins,
            "h2h_wins": team.h2h_wins,
            "total_h2h_wins" : team.total_h2h_wins,
            "total_points": team.total_points,
            "weekly_points": team.weekly_points,
            "points_wins": team.points_wins,
            "total_points_wins": team.total_points_wins,
            "ranks": team.ranks
        } for team in teams.values()}
        json.dump(data, json_file, indent=1)


def main():
    # Check if team data already exists in the .json file
    teams = load_team_data()

    if not teams:
        num_teams = int(input("Enter the number of teams in your league: "))
        for _ in range(num_teams):
            team_name = input("Enter team name: ")
            owner_name = input(f"Enter the owner of {team_name}: ")
            if team_name not in teams:
                teams[team_name] = FantasyTeam(team_name, owner_name)
                teams[team_name].is_done = False

    while True:
        week = int(input("Input the week: "))
        input_results_for_week(week, teams)
        give_extra_wins(teams, week)
        for team in teams.values():
            team.update_cuml_stats()
        display_rankings(teams, week)
        save_rankings_history(teams, week)

        continue_input = input("Do you want to input results for another week? (yes/no): ").strip().lower()
        if continue_input != 'yes':
            break


if __name__ == "__main__":
    main()

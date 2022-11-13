
class Stats:
    def __init__(self) -> None:
        self.total_games = 0
        self.wins = 0
        self.losses = 0
        pass

    def increment_win(self) -> None:
        self.total_games += 1
        self.wins += 1

    def increment_loss(self) -> None:
        self.total_games += 1
        self.losses += 1

    def __str__(self) -> str:
        msg = "WINS: " + str(self.wins) + " and LOSSES: " + str(self.losses) + '\n'
        winrate = str(round((self.wins / self.total_games) * 100, 2))
        msg = msg + "Winrate of: " + winrate
        return msg
import web_admin as api


class Game:
    def __init__(self, game_map, game_type):
        self.game_map = game_map
        self.game_type = game_type
        self.difficulty = api.DIFF_NORM
        self.wave = 0
        self.length = api.LEN_NORM
        self.time = 0

        self.zeds_wave_killed = 0
        self.zeds_wave_total = 0
        self.zeds_killed = 0

        self.dosh_wave_earned = 0
        self.dosh_earned = 0

        self.password = None
        self.password_enabled = False

    def __str__(self):
        return "Mode: {}\nMap: {}\nDifficulty: {}\nWave {}/{}".format(
            self.game_type,
            self.game_map.title,
            self.difficulty,
            self.wave,
            self.length
        )


class GameMap:
    def __init__(self, name, title="kf-default"):
        self.name = name
        self.title = title

        self.plays_survival = 0
        self.plays_weekly = 0
        self.plays_endless = 0
        self.plays_survival_vs = 0
        self.plays_other = 0
        self.highest_wave = 0
        self.votes = 0

    def reset_stats(self):
        self.plays_survival = 0
        self.plays_weekly = 0
        self.plays_endless = 0
        self.plays_survival_vs = 0
        self.plays_other = 0
        self.highest_wave = 0
        self.votes = 0

    def __str__(self):
        return ("Title: {}\nPlays survival: {}\nPlays survival_vs: {}\n"
                "Plays endless: {}\nPlays weekly: {}")\
            .format(self.title, self.plays_survival, self.plays_survival_vs,
                    self.plays_endless, self.plays_weekly)

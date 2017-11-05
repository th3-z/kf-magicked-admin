import sqlite3
from os import path

class ServerDatabase:
    
    def __init__(self, name):
        self.sqlite_db_file = name + "_db" + ".sqlite"

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.conn = sqlite3.connect(self.sqlite_db_file, check_same_thread = False)
        self.cur = self.conn.cursor()

        print("Database for " + name + " initialised")

    def build_schema(self):
        print("Building fresh schema...")

        conn = sqlite3.connect(self.sqlite_db_file)
        cur = conn.cursor()

        with open('server_schema.sql') as schema_file:
            cur.executescript(schema_file.read())

        conn.commit()
        conn.close()
    
    def start_session(self, player):
        pass 

    def end_session(self, player):
        pass

    def end_game(self, game):
        pass

    def player_dosh(self, username):
        self.cur.execute('SELECT (dosh) FROM players WHERE username="{un}"'.\
            format(un=username))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_dosh_spent(self, username):
        self.cur.execute('SELECT (dosh_spent) FROM players WHERE username="{un}"'.\
            format(un=username))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_kills(self, username):
        self.cur.execute('SELECT (kills) FROM players WHERE username="{un}"'.\
            format(un=username))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_deaths(self, username):
        self.cur.execute('SELECT (deaths) FROM players WHERE username="{un}"'.\
            format(un=username))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def load_player(self, player):
        player.total_kills = self.player_kills(player.username)
        player.total_dosh =  self.player_dosh(player.username)
        player.total_deaths = self.player_deaths(player.username)
        player.total_dosh_spent = self.player_dosh_spent(player.username)

    def save_player(self, player):
        self.cur.execute("INSERT OR IGNORE INTO players (username) VALUES ('{un}')".\
            format(un=player.username))

        self.cur.execute("UPDATE players SET dosh_spent = {d} WHERE username = '{u}'".\
            format(d=player.total_dosh_spent, u=player.username))
        self.cur.execute("UPDATE players SET dosh = {d} WHERE username = '{u}'".\
            format(d=player.total_dosh, u=player.username))
        self.cur.execute("UPDATE players SET kills = {k} WHERE username = '{u}'".\
            format(k=player.total_kills, u=player.username))
        self.cur.execute("UPDATE players SET deaths = {d} WHERE username = '{u}'".\
            format(d=player.total_deaths, u=player.username))

        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()


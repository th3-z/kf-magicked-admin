from chatbot.commands.command import Command

import time
import threading

ALL_WAVES = 99

class CommandOnWave():
    
    def __init__(self, args, wave, length, chatbot):
        if wave > 0:
            self.wave = wave
        if wave < 0:
            # the boss wave is length+1, this should equate to -1
            self.wave = (length + 1) + (wave + 1)
        self.args = args
        self.chatbot = chatbot

    def new_wave(self, wave):
        if wave == self.wave or self.wave == ALL_WAVES:
            self.chatbot.command_handler("server", self.args, admin=True)

class CommandOnTime(threading.Thread):

    def __init__(self, args, time_interval, chatbot):
        self.exit_flag = threading.Event()
        self.args = args
        self.chatbot = chatbot
        self.time_interval = float(time_interval)

        threading.Thread.__init__(self)

    def terminate(self):
        self.exit_flag.set()

    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.chatbot.command_handler("server", self.args, admin=True)
        
class CommandOnTimeManager(Command):

    def __init__(self, server, chatbot, adminOnly = True):
        self.command_threads = []
        self.chatbot = chatbot
        Command.__init__(self, server, adminOnly)
    
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if args[0] == "stop_tc":
            self.terminate_all()
            return "Timed commands stopped"
        
        try:
            time = int(args[1])
        except ValueError:
            return "Malformed command, \""+args[1]+"\" is not an integer."

        time_command = CommandOnTime(args[1:], time, self.chatbot)
        self.command_threads.append(time_command)

    def terminate_all(self):
        if len(self.command_threads) > 0:
            for command_thread in self.command_threads:
                commnd_thread.terminate()
        else:
            return "Nothing was running"

class CommandOnWaveManager(Command):
    def __init__(self, server, chatbot, adminOnly = True):
        self.commands = []
        self.chatbot = chatbot
        Command.__init__(self, server, adminOnly)
       
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if args[0] == "stop_wc":
            return self.terminate_all()
        elif args[0] == "start_wc":
            if len(args) < 2:
                return "Malformed command, missing second argument"
            return self.start_command(args[2:], args[1])
        elif args[0] == "new_wave":
            for command in self.commands:
                command.new_wave(int(args[1]))
        
    def terminate_all(self):
        if len(self.commands) > 0:
            self.wave_commands = []
            return "Wave commands halted."
        else:
            return "Nothing was running."
    
    def start_command(self, args, wave):
        if len(args) < 1:
            return "Missing argument (command)."
            
        game_length = self.server.game['length']
        
        try:
            wc = CommandOnWave(args, int(wave), game_length)
        except ValueError:
            wc = CommandOnWave(args, ALL_WAVES, game_length)
        self.commands.append(wc)
        return "Wave command started."
        
class CommandOnTraderManager(Command):
    def __init__(self, server, chatbot, adminOnly = True):
        self.commands = []
        self.chatbot = chatbot
        
        Command.__init__(self, server, adminOnly)
        
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if args[0] == "start_trc":
            return self.start_command(args[1:])
        elif args[0] == "stop_trc":
            return self.terminate_all()
        elif args[0] == "t_open":
            for command in self.commands:
                self.chatbot.command_handler("server", command, admin=True)
    
    def terminate_all(self):
        if len(self.commands) > 0:
            self.commands = []
            return "Trader commands stopped."
        else:
            return "Nothing was running."
    
    def start_command(self, args):
        if len(args) < 1:
            return "Missing argument (command)."
        
        self.commands.append(args)
        return "Trader command started."
        
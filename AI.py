import Human
import os, sys
from subprocess import Popen, PIPE

class ComputerPlayer(Human.HumanPlayer):
    """AI Player aka Bot. Communicates with a script using
        the subprocess module"""
    type = 'Computer'
    def __init__(self, turn, path, name = None):
        """Creates a bot, which takes  arguments:
            turn - 1 for horizontal 0 for vertical
            path - if an .exe file on windows, no extension needed,
                    else (if a .py file or on linux) with extension
            (optional) name - name of the bot
            """
        self.python = False
        if name == None:
            self.name = path
        else:
            self.name = name
        self.turn = turn
        if path[-3:] == '.py': #python file
            extension = ''
            self.python = True
        elif sys.platform == 'win32':
            extension = '.exe'
        else: #linux?
            extension = ''
        self.path = os.path.join('Scripts', '%s%s' % (path,extension))

    def get_input(self, message = None):
        """Communicates with the 'bot."""
        a = self.prog.stdin.write(message)
        b = self.prog.stdout.readline()
        return tuple(map(int, b.split()))
    
    def output(self, message):
        try:
            self.prog.stdin.write(message)
        except IOError:
            #already closed, StopGate.py will detect
            pass
        
    def kill(self):
        """Kills the bot. If on windows, kills the process using PID"""
        #todo - process killing on linux
        if sys.platform == 'win32' and self.alive:
            os.popen('TASKKILL /PID '+str(self.prog.pid)+' /F')
            self.alive = False
        
    def start(self):
        """Starts the pipe, using a separate shell provided
            by the subprocess module.
            If bot is from python, prepends the argument python
            and appends -u
            Ex: "python lolllammas.py -u"
            """
        if not self.python:
            self.prog = Popen(self.path,
                          shell = True,
                          stdin = PIPE,
                          stdout = PIPE)
        else:
            print self.path
            self.prog = Popen("python %s -u" % self.path,
                              shell = True,
                              stdin = PIPE,
                              stdout = PIPE)
        self.alive = True

import logging
#TODO: Implement a logging service
class LogService():
    def __init__(self, GlobalStat, logLevel="DEFAULT", timestamp = None, filename = None):
        self.filename = filename
        self.Stat = GlobalStat
        self.logLevel = logLevel
        self.timestamp = timestamp
    
    def create_log_file(self):
        if self.filename is None:
            self.filename = 'log.txt'
            
        with open(self.filename, 'w') as f:
            return f is None
        
        return False
    
    def setLogLevel(self, logLevel):
        self.logLevel
    
    def log(self, message):
        content = '[{} {}]: {}'.format(self.logLevel, self.timestamp, message)
        return content
    
    def commit(self, message): 
        with open(self.filename, 'w+') as f:
            f.write(message)
        
    
import os
import logging
import logging.handlers


def config_logging():
    logfile = os.path.join(os.path.dirname(__file__), "logfile.log")
    #logging.basicConfig(filename=logfile,
    #                    filemode="w",  # a - append logs, w - rewrite logs
    #                    format='%(asctime)s - %(levelname)s - %(message)s',
    #                    datefmt='%Y-%m-%d %X',
    #                    level=logging.INFO)
    filehandler = TruncatedFileHandler(logfile, "w", 120000)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %X',
        level=logging.INFO, handlers=[filehandler])


# https://stackoverflow.com/questions/24157278/limit-python-log-file
class TruncatedFileHandler(logging.handlers.RotatingFileHandler):
    """ Logging file handler for truncating the old logfile when it gets too big """

    def __init__(self, filename, mode='a', maxBytes=0, encoding=None, delay=0):
        super(TruncatedFileHandler, self).__init__(
            filename, mode, maxBytes, 0, encoding, delay)

    def doRollover(self):
        """Truncate the file"""
        if self.stream:
            self.stream.close()
        dfn = self.baseFilename + ".1"
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(self.baseFilename, dfn)
        os.remove(dfn)
        self.mode = 'w'
        self.stream = self._open()

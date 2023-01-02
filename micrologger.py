import sys
import time
import os 
from event_timer import EventTimer
#from uasyncio import Lock

class MicroLogger(object):
    VERBOSE = (0, "VRB")
    DEBUG = (1, "DBG")
    INFORMATION = (2, "INF")
    WARNING = (3, "WRN")
    ERROR = (4, "ERR")
    FATAL = (5, "FTL")

    level = INFORMATION
    directory: str = None
    retention_count: int = 72 #hours
    
    _file_output_name = None 
    _file_output_stream = None
    _file_output_message_cache = []
    _file_output_message_cache_max_length = 128
    _flush_timer = None
    #_file_output_message_cache_lock = Lock()

    def __init__(self, source = ""):
        self.source = source
        if self.directory is not None:
            try:
                os.mkdir(f"{self.directory}")
                self.flush_stream() # also opens stream, so we are ready for dumping stacktrace

                if self._flush_timer is None:
                    self._flush_timer = EventTimer(60000)
                    self._flush_timer.elapsed.add(self.flush_stream)
            except OSError:
                pass
                

    def write(self, level, message: str):
        if level[0] >= self.level[0]:
            tm = time.localtime()
            output = f"[{tm[3]:02d}:{tm[4]:02d}:{tm[5]:02d} {level[1]}] {self.source:18} {message}"
            print(output)
            if self.directory is not None:
                self._append_to_file(output)


    def verb(self, message: str):
        self.write(MicroLogger.VERBOSE, message)


    def debug(self, message: str):
        self.write(MicroLogger.DEBUG, message)


    def info(self, message: str):
        self.write(MicroLogger.INFORMATION, message)


    def warn(self, message: str):
        self.write(MicroLogger.WARNING, message)


    def error(self, message: str):
        self.write(MicroLogger.ERROR, message)


    def fatal(self, message: str):
        self.write(MicroLogger.FATAL, message)


    def exception(self, exception: Exception):
        self.write(MicroLogger.ERROR, f"{exception}")
        sys.print_exception(exception)
        if self._file_output_stream is not None:
            self.flush_stream() # ensure we are at correct position
            sys.print_exception(exception, self._file_output_stream)
            self.flush_stream()


    def _append_to_file(self, message):
        try:
            #self._file_output_message_cache_lock.acquire()
            self._file_output_message_cache.append(message)
        finally:
            #self._file_output_message_cache_lock.release()
            pass

        if len(self._file_output_message_cache) >= self._file_output_message_cache_max_length:
            self.flush_stream()
        
            
    def flush_stream(self):
        if self.directory is not None:
            try:
                tm = time.localtime()
                file_path = f"{self.directory}/{tm[0]}_{tm[1]:02d}_{tm[2]:02d}__{tm[3]:02d}_debuglog.txt"

                if self._file_output_name != file_path: # we are not streaming to this file
                    if self._file_output_stream is not None:
                        self._file_output_stream.close() # close eisting before attempting retention operation
                        self._file_retention()

                    self._file_output_stream = open(file_path, 'a')
                    self._file_output_name = file_path

                #self._file_output_message_cache_lock.acquire()
                for line in self._file_output_message_cache:
                    self._file_output_stream.write(line)
                    self._file_output_stream.write('\n')
                self._file_output_message_cache.clear()
                self._file_output_stream.flush()

            except OSError as os_ex:
                print(os_ex)
            except Exception as ex:
                print(ex)
            finally:
                #self._file_output_message_cache_lock.release
                pass

    def _file_retention(self):
        try:
            log_files = sorted(os.listdir(self.directory))
            #log_files.reverse()
            for index, file_path in enumerate(log_files):
                if (len(log_files) - index) > self.retention_count:
                    os.remove(f"{self.directory}/{log_files[index]}")
        
        except OSError as os_ex:
                print(os_ex)
        except Exception as ex:
                print(ex)         
        finally:
            pass


if __name__ == "__main__":
    MicroLogger.directory = "/logs"
    MicroLogger.retention_count = 3
    logger = MicroLogger("TestLog")
    

    for i in range(5):
        logger.debug("this is a debug message")
        logger.info("this is a info message")
        logger.warn("this is a warning message")
        try:
            raise Exception("throw ex test")
        except Exception as ex:
            logger.error(f"exception! {ex}")
            logger.exception(ex)

    #logger._file_output_stream.close()
    logger._file_retention()


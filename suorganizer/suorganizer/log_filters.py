from logging import Filter
from pprint import pprint


class ManagementFilter(Filter):
    #Luckily, all of the SQL output is created by a function called execute(), 
    #and so we can simply filter our LogRecord objects according to whether 
    #the record was created by the execute() function
    def filter(self, record):
        if (hasattr(record, 'funcName') and record.funcName == 'execute'):
            return False
        else:
            return True
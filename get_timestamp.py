import datetime

def get_datetime_no_spaces():
    return str(datetime.datetime.now()).replace(" ","_").replace(":","-").split(".")[0]
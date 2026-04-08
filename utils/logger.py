import datetime

def log_event(message):

    with open("system.log","a") as f:

        f.write(str(datetime.datetime.now())+" : "+message+"\n")
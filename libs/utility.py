import random

def get_sms_code(digits=4):
    return random.randint( pow(10,digits), pow(10,(digits+1))-1)
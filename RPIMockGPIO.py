BOARD = 0
OUT = 0
IN = 1
RPI_REVISION = -1
VERSION = -1

def output(pin, mode):
    print "Pin: {} and Mode: {}".format(pin, mode)

def input(pin):
    print "Pin {} on input".format(pin)
    return False

def setmode(mode):
    pass

def setup(pin, mode):
    pass

def cleanup():
    pass

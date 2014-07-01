import ConfigParser
import os

CONFFILE = "denat.conf"

def read_conf_file(filename):
    filename = os.path.abspath(filename)
    config = ConfigParser.SafeConfigParser()
    config.read(filename)
    return config


if __name__ == '__main__':
    c = read_conf_file(CONFFILE)
    print c

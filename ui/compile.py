import os

from utils import my_commands
import sys
PATH = r"C:\Anaconda2\Lib\site-packages\PyQt4\uic"


def compile_ui(fname):
    cmd = "python.exe {1}\\pyuic.py {0}.ui -o {0}.py".format(fname.replace(".ui", ""), PATH)
    print 'cmd=', cmd
    print my_commands.getstatusoutput(cmd)


def main():
    compile_ui("dock.ui")
    print 'done'


if __name__ == '__main__':
    main()
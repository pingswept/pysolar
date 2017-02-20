#!/usr/bin/env python

"""
read write file experiment
"""
def mod_file():
    """
    modify file
    """
    infile = open('earth.B4.vsop.txt', 'r')
    outfile = open('vsopearth.B4.txt', 'w')
    while True:
        text0 = infile.readline()
        if len(text0) == 0:
            break
        print(text0)
        text1 = '('
        text2 = text0.replace('  ', ', ')
        text3 = text2.replace(',  ', ', ')
        text4 = text3.replace('\n', '),\n')
        text5 = text1 + text4

        # Put any more processing logic here
        outfile.write(text5)

    infile.close()
    outfile.close()

mod_file()

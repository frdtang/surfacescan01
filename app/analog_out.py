#!/usr/bin/env python
#
# MCC 118 example program
# Read and display analog input values
#
import sys
from daqhats import hat_list, HatIDs, mcc118

# get hat list of MCC daqhat boards
board_list = hat_list(filter_by_id = HatIDs.ANY)

entry = board_list[0]
# Read and display every channel
while True:
    board = mcc118(entry.address)    
    value = board.a_in_read(0)
    print("Ch {0}: {1:.3f}".format(0, value))	
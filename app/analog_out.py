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
 
    print("Board {}: MCC 118".format(entry.address))
    board = mcc118(entry.address)
    channel = board.info().NUM_AI_CHANNELS[0]
    value = board.a_in_read(channel)
    print("Ch {0}: {1:.3f}".format(channel, value))	
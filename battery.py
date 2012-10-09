#!/usr/bin/env python
import curses, argparse, sys

import pygame
from utils import load_banks

parser = argparse.ArgumentParser('Battery - a simple CLI & headless rompler')
parser.add_argument('-b', '--bank-kit', action='store', dest='bank_kit', default='default')
args = parser.parse_args()

# That's all what MaKeyMaKey has in stock setting, except 'SPC' and 'w'
AVAILABLE_KEYS = 'LEFT RIGHT DOWN UP a s d f g h j'.split()
KEYS = dict(
    [(key, getattr(curses, 'KEY_%s' % key, ord(key[0]))) for key in AVAILABLE_KEYS])

# We need to init mixer before pygame initializations, smaller buffer should avoid lags
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
# Get 4 channels for each key + one for system sounds
pygame.mixer.set_num_channels(4 * len(KEYS) + 1)

banks, banks_iter = load_banks(args.bank_kit)
if not banks and not banks_iter:
    sys.exit('Can\'t load bank kit file "%s". Are you sure about this?' % file)
curr_bank, curr_bank_nr, reverse = banks_iter.next(), 1, False

# init curses
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
LINES, COLS = screen.getmaxyx()

def bank_flash(curr_bank_nr):
    screen.addstr(0, 0, 'Bank: #%s' % (str(curr_bank_nr).zfill(2)), curses.A_REVERSE)


def tray_msg(msg, row=0):
    screen.addstr(LINES - 1 - row, 0, msg)


bank_flash(curr_bank_nr)
tray_msg('Use %s keys to play. "SPACE" to change bank, "w" to reverse, "ESC" or "q" to exit.' % ', '.join(
    map(lambda x: '"%s"' % x, AVAILABLE_KEYS)))

while True:
    event = screen.getch()
    if event in (ord('q'), 27): #q or ESC
        break
    elif event == ord(' '):
        curr_bank = banks_iter.next()
        curr_bank_nr += 1 if curr_bank_nr < len(banks) else -(len(banks) -1)
        bank_flash(curr_bank_nr)
    elif event == ord('w'):
        reverse = not reverse
        tray_msg('mode: %s' % 'reversed' if reverse else 'normal  ', row=1)
    for key, code in KEYS.iteritems():
        if event == code:
            try:
                curr_bank[key][int(reverse)].play()
            except KeyError:
                tray_msg('No sample defined for "%s" key\n' % key, row=1)

# This should somehow restore terminal back, but it doesn't work all the time.
# Call "reset" in your shell if you need to
curses.endwin()
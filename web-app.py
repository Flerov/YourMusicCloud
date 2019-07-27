#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from remi import start, App
import remi.gui as gui
import db_updown
import sys
import os

intro = """\033[0;34m\n
---------------------------------
         Music Cloud
           V. 1.0.
---------------------------------
\033[0;0m
"""


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.container = gui.Widget(width='90%', height='35%')
        self.container2 = gui.Widget(width='50%', height='50%')
        self.container3 = gui.VBox(width='100%', height='50%')
        self.title = gui.Label('Music Cloud', width='50%', height='30%')
        self.input = gui.TextInput('Input Dialog', 'Song name?',
                                   width='80%', height='15%')
        self.button = gui.Button('Download')
        self.button.onclick.do(self.submit_song)

        self.title.style['font-size'] = '200%'
        self.title.style['text-decoration'] = 'underline solid black'
        self.title.style['overflow'] = 'auto'
        self.title.style['margin'] = 'top'
        self.title.style['position'] = 'absolute'
        self.title.style['top'] = '12px'
        self.title.style['left'] = '42%'
        self.title.style['bottom'] = '0'
        self.title.style['right'] = '0'

        self.container.style['overflow'] = 'auto'
        self.container.style['margin'] = 'auto'
        self.container.style['position'] = 'absolute'
        self.container.style['top'] = '0'
        self.container.style['left'] = '0'
        self.container.style['bottom'] = '0'
        self.container.style['right'] = '0'
        self.container.style['border'] = 'solid black'

        self.container2.style['overflow'] = 'auto'
        self.container2.style['margin'] = 'auto'
        self.container2.style['position'] = 'absolute'
        self.container2.style['top'] = '50%'
        self.container2.style['left'] = '0'
        self.container2.style['bottom'] = '0'
        self.container2.style['right'] = '0'

        self.input.style['overflow'] = 'auto'
        self.input.style['margin'] = 'auto'
        self.input.style['position'] = 'middle'
        self.input.style['top'] = '150px'

        self.button.style['width'] = '90%'
        self.button.style['overflow'] = 'auto'
        self.button.style['margin'] = 'auto'
        self.button.style['position'] = 'auto'
        self.button.style['padding'] = 'auto'
        self.button.style['top'] = '15px'
        self.button.style['left'] = '30px'
        self.button.style['background-color'] = '#f44336'  # red

        self.container2.append(self.input)
        self.container2.append(self.button)
        self.container.append(self.title)
        self.container.append(self.container2)

        return self.container

    def submit_song(self, button):
        string = "'{}'".format(self.input.get_text())
        print('\033[0;31m[DEBUG]\033[0;0m Song(s): {} submitted...Fetching music!'.format(string))
        songs = preparestring(string=string)
        
        #for nsong in range(0, len(songs)):
        #    self.change_button(songs, nsong)
        #    _cmd = cmd + songs[nsong]
        #    os.system(_cmd)
        print('\033[0;31m[DEBUG]\033[0;0m Syncing Dropbox - ~/MyMusic with local dir ~/Music')
        db_updown.main()
        print('\033[0;31m[DEBUG]\033[0;0m Dropbox synced')
        button.style['background-color'] = '#4CAF50'  # green

    def change_button(self, songs, nsong):
        _txt = 'Downloaded  Music {}/{}'.format(nsong + 1, len(songs))
        self.button.set_text(_txt)


# String check ; String prepare
def preparestring(string):
    if '.' in string:
        songs = string.split('.')
        for nsong in range(len(songs)):
            songs[nsong] = '"' + songs[nsong] + '"'
    else:
        songs = ['"' + string + '"']
    return songs


if __name__ == '__main__':
    try:
        start(MyApp, address='143.181.197.80', port=8082, start_browser=False)
        sys.stdout.write(intro)  # INTRO
        print("\033[0;31m[DEBUG]\033[0;0m Server up!\n")
    except KeyboardInterrupt:
        print("\033[0;31m\n[DEBUG]\033[0;0m Keyboard Interruption detected!\n")
    finally:
        print("\n\033[0;31m[DEBUG]\033[0;0m Server down!\n")

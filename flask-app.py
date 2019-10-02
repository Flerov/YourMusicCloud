#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from spotdl import youtube_tools
from spotdl import downloader
from spotdl import internals
from spotdl import const
from spotdl import handle

from flask import Flask
from flask import render_template
from flask import request

from multiprocessing import Pool
import sys
import os


app = Flask(__name__)
template_path = os.path.join(os.path.dirname(__file__), 'templates')


def get_track():
    const.args = handle.get_arguments()

    internals.filter_path(const.args.folder)
    youtube_tools.set_api_key()

    try:
        if const.args.song:
            for track in const.args.song:
                track_dl = downloader.Downloader(raw_song=track)
                track_dl.download_single()
    except KeyboardInterrupt as e:
        print("Exception occured in method 'get_track':", e)
        return False
    return True


def on_finish_get_track(result):
    with app.app_context():
        if result:
            print('[LOG] Download finished. Process stopped!')
            return render_template('mainpage.html', status='Download finished!')
        else:
            return render_template('mainpage.html', status='Download failed. Something went wrong!', show_back_button=True)


@app.route('/')
def main():
    return render_template('mainpage.html', status='Ready to perform!')


@app.route('/get', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        return "POST"
    else:
        #  LOGIC HERE
        song = request.args.get('song')
        sys.argv.append('-s')
        sys.argv.append(song)
        sys.argv.append('--overwrite')
        sys.argv.append('force')
        sys.argv.append('--trim-silence')
        pool = Pool(processes=1)
        result = pool.apply_async(func=get_track, callback=on_finish_get_track)
        return render_template('mainpage.html', status='Download in progress', show_back_button=True)


@app.route('/sync', methods=['POST', 'GET'])
def sync():
    if request.method == 'POST':
        # coming soon > upload downloaded tracks to your dropbox as cloud to have music on all devices
        print('NOT AVAILABLE YET')
        return render_template('mainpage.html', msg='Dropbox synchronized')
    else:
        return render_template('404.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

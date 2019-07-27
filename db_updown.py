#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: github.com/Flerov
# @version: 4.20

import unicodedata
import contextlib
import argparse
import datetime
import dropbox
import time
import sys
import six
import os


TOKEN = ''  # YOUR DROPBOX TOKEN
cmd = 'spotdl --song '
parser = argparse.ArgumentParser(description='Sync ~/MyMusic to Dropbox')
parser.add_argument('folder', nargs='?', default='MyMusic',
                    help='Folder name in Dropbox')  # default=Name of your dropbox folder linked to your dropbox TOKEN
parser.add_argument('rootdir', nargs='?', default='~/Music',
                    help='Local directory to upload') # default=Name of your local folder. Best is to not change this folder


def main():
    time.sleep(3)
    # LOGIC
    args = parser.parse_args()
    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(TOKEN)

    # directory and subdirectory walk
    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
               name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already snyced [stats match]')
                else:

                    print(name, 'exists with different stats, downloading')
                    res = download(dbx, folder, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        sys.stdout.write('\033[0;43m', name, 'is already synced [content match]\033[0;0m\n')
                    else:
                        sys.stdout.write('\033[0;34m', name, 'has changed since last sync\033[0;0m\n')
                        upload(dbx, fullname, folder, subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep


def list_folder(dbx, folder, subfolder):
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, ' -- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv


def download(dbx, folder, subfolder, name):
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files.download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    sys.stdout.write('\033[0;32muploaded as', res.name.decode('utf-8'), '\033[0;0m\n')
    return res


def download_songs(songs: list):
    for nsong in range(0, len(songs)):
        _cmd = cmd + songs[nsong]
        os.system(_cmd)


@contextlib.contextmanager
def stopwatch(message):
    t0 = time.time()
    print('\033[0;31m[DEBUG]\033[0;0m', message)
    try:
        yield  # yielding back to caller after that returning back here -> to finally
    finally:
        t1 = time.time()
        print('\033[0;31m[DEBUG]\033[0;0m Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        songs = sys.argv[2]
        print(songs)
        print(type(list(songs)))
        songs = list(songs)
        print(songs[:-1])

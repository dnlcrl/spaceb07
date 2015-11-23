#!/usr/bin/env python
# encoding: utf-8

'''Upload the contents of a folder to Dropbox.
This is an example app for API v2.
'''

import datetime
import os
import six
import time
import unicodedata
from constants import FileNames

import dropbox


class Saver:

    '''Upload the contents of your Downloads folder to Dropbox.
    This is an example app for API v2.

    Requires API credentials to be available in environment
    variables.

    TODO: methods docstrings

    '''

    def __init__(self):
        self.dbx = dropbox.Dropbox(os.environ.get('DROPBOX_ACCESS_TOKEN'))
        self.rootdir = './data'
        self.folder = '/'
        self.init_files()
        self.sync()

    def init_files(self):
        for filename in [FileNames.log_file, FileNames.last_tweets]:
            try:
                _, f = self.dbx.files_download(
                    '/' + filename.split(os.sep)[-1])
                content = f.content
            except Exception, e:
                content = ''
                print 'Error: ' + str(e) + ' with filename ' + filename
            out = open(filename, 'wb')
            out.write(content)
            out.close()

    def sync(self):
        for dn, dirs, files in os.walk(self.rootdir):
            subfolder = dn[len(self.rootdir):].strip(os.path.sep)
            listing = self.list_folder(self.folder, subfolder)

            # First do all the files.
            for name in files:
                fullname = os.path.join(dn, name)
                if not isinstance(name, six.text_type):
                    name = name.decode('utf-8')
                nname = unicodedata.normalize('NFC', name)
                if name.startswith('.'):
                    pass
                    # print('Skipping dot file:', name)
                elif name.startswith('@') or name.endswith('~'):
                    pass
                    # print('Skipping temporary file:', name)
                elif name.endswith('.pyc') or name.endswith('.pyo'):
                    pass
                    # print('Skipping generated file:', name)
                elif nname in listing:
                    md = listing[nname]
                    mtime = os.path.getmtime(fullname)
                    mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                    size = os.path.getsize(fullname)
                    if (isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size):
                        pass
                        # print(name, 'is already synced [stats match]')
                    else:
                        # print(name, 'exists with different stats, downloading')
                        res = self.download(self.folder, subfolder, name)
                        with open(fullname) as f:
                            data = f.read()
                        if res == data:
                            pass
                            # print(name, 'is already synced [content match]')
                        else:
                            # print(name, 'has changed since last sync')
                            self.upload(
                                fullname, self.folder, subfolder, name, overwrite=True)
                else:
                    self.upload(fullname, self.folder, subfolder, name)

            # Then choose which subdirectories to traverse.
            keep = []
            for name in dirs:
                if name.startswith('.'):
                    pass
                    # print('Skipping dot directory:', name)
                elif name.startswith('@') or name.endswith('~'):
                    pass
                    # print('Skipping temporary directory:', name)
                elif name == '__pycache__':
                    pass
                    # print('Skipping generated directory:', name)
                else:
                    keep.append(name)

            dirs[:] = keep

    def list_folder(self, folder, subfolder):
        '''List a folder.
        Return a dict mapping unicode filenames to
        FileMetadata|FolderMetadata entries.
        '''
        path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
        while '//' in path:
            path = path.replace('//', '/')
        path = path.rstrip('/')
        try:
            res = self.dbx.files_list_folder(path)
        except dropbox.exceptions.ApiError as err:
            print('Folder listing failed for', path, '-- assumped empty:', err)
            return {}
        else:
            rv = {}
            for entry in res.entries:
                rv[entry.name] = entry
            return rv

    def download(self, folder, subfolder, name):
        '''Download a file.
        Return the bytes of the file, or None if it doesn't exist.
        '''
        path = '/%s/%s/%s' % (folder,
                              subfolder.replace(os.path.sep, '/'), name)
        while '//' in path:
            path = path.replace('//', '/')
        try:
            md, res = self.dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
        data = res.content
        # print(len(data), 'bytes; md:', md)
        return data

    def upload(self, fullname, folder, subfolder, name, overwrite=False):
        '''Upload a file.
        Return the request response, or None in case of error.
        '''
        path = '/%s/%s/%s' % (folder,
                              subfolder.replace(os.path.sep, '/'), name)
        while '//' in path:
            path = path.replace('//', '/')
        mode = (dropbox.files.WriteMode.overwrite
                if overwrite
                else dropbox.files.WriteMode.add)
        mtime = os.path.getmtime(fullname)
        with open(fullname, 'rb') as f:
            data = f.read()
        try:
            res = self.dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
        # print('uploaded as', res.name.encode('utf8'))
        return res

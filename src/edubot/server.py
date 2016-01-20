import posixpath
import urllib
import os

from SimpleHTTPServer import SimpleHTTPRequestHandler

import SocketServer
import threading


class RequestHandler(SimpleHTTPRequestHandler):

    # modify this to add additional routes
    ROUTES = []

    def translate_path(self, path):

        # set default root to cwd
        root = os.getcwd()

        # look up routes and set root directory accordingly
        for pattern, rootdir in RequestHandler.ROUTES:
            if path.startswith(pattern):
                # found match!
                path = path[len(pattern):]  # consume path up to pattern len
                root = rootdir
                break

        # normalize path and prepend root directory
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)

        path = root
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)

        return path


class Httpd(threading.Thread):

    def __init__(self, port=10000, docroot="../../ext/snap"):

        threading.Thread.__init__(self)

        RequestHandler.ROUTES.append(('', docroot))

        self.daemon = True
        self.port = port

    def run(self):

        httpd = SocketServer.TCPServer(("", self.port), RequestHandler)

        print "serving at port", self.port
        httpd.serve_forever()

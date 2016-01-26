import os
import threading
from bottle import static_file, Bottle


class App(Bottle):

    def __init__(self, doc_root_snap=".", snap_extensions={}, doc_root_overlay=None):

        Bottle.__init__(self)

        self.doc_root_snap = doc_root_snap
        self.snap_extensions = snap_extensions
        self.doc_root_overlay = doc_root_overlay

        self.route("/snap/libraries/<file_path>", callback=self.serve_library)
        self.route("/snap/<file_path:path>", callback=self.serve_snap)

    def serve_library(self, file_path):

        res = ""

        if file_path == "LIBRARIES":

            for ext in self.snap_extensions:
                res += "%s.xml\t%s\n" % (ext.name, ext.description)

        else:

            for ext in self.snap_extensions:
                if ext.name == file_path[:-4]:
                    res = ext.generate_snap()
                    break

        # TODO: if no matching ext. found, error response needed
        return res

    def serve_snap(self, file_path):

        root = self.doc_root_snap

        if self.doc_root_overlay is not None and os.path.exists(os.path.join(self.doc_root_overlay, file_path)):
            root = self.doc_root_overlay

        return static_file(file_path, root=root)


class Httpd(threading.Thread):

    def __init__(self, host="localhost", port=10000, doc_root_snap="../../ext/snap", snap_extensions={},
                 doc_root_overlay=None):

        threading.Thread.__init__(self)

        self.daemon = True
        self.host = host
        self.port = port
        self.app = App(doc_root_snap, snap_extensions, doc_root_overlay)

    def run(self):
        self.app.run(host=self.host, port=self.port, quiet=False, debug=True)

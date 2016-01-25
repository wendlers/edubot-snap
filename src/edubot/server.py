import threading
from bottle import static_file, Bottle


class App(Bottle):

    def __init__(self, doc_root=".", snap_extensions={}):

        Bottle.__init__(self)

        self.doc_root = doc_root
        self.snap_extensions = snap_extensions

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
        return static_file(file_path, root=self.doc_root)


class Httpd(threading.Thread):

    def __init__(self, host="localhost", port=10000, doc_root="../../ext/snap", snap_extensions={}):

        threading.Thread.__init__(self)

        self.daemon = True
        self.host = host
        self.port = port
        self.app = App(doc_root, snap_extensions)

    def run(self):

        self.app.run(host=self.host, port=self.port, quiet=False, debug=True)

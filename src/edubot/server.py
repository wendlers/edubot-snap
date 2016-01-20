import threading
from bottle import static_file, route, run


class Httpd(threading.Thread):

    _snap_exts = []

    def __init__(self, port=10000, doc_root="../../ext/snap", snap_exts={}):

        threading.Thread.__init__(self)

        self.daemon = True
        self.port = port

        Httpd._snap_exts += snap_exts

    @staticmethod
    @route("/snap/libraries/<filepath>")
    def serve_library(filepath):

        res = ""

        if filepath == "LIBRARIES":

            for ext in Httpd._snap_exts:
                res += "%s.xml\t%s\n" % (ext.name, ext.description)

        else:

            for ext in Httpd._snap_exts:
                if ext.name == filepath[:-4]:
                    res = ext.generate_snap()
                    break

        # TODO: if no matching ext. found, error response needed
        return res

    @staticmethod
    @route("/snap/<filepath:path>")
    def serve_snap(filepath):
        return static_file(filepath, root="../../ext/snap")

    def run(self):

        run(host='localhost', port=10000, quiet=False, debug=True)

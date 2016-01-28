import os
import threading
import pkg_resources

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

    '''
    def serve_snap(self, file_path):

        root = self.doc_root_snap

        if self.doc_root_overlay is not None and os.path.exists(os.path.join(self.doc_root_overlay, file_path)):
            root = self.doc_root_overlay

        return static_file(file_path, root=root)
    '''

    def serve_snap(self, file_path):

        file_path = "snap/" + file_path

        print("file_path", file_path)

        if pkg_resources.resource_exists("overlay", file_path):
            module = "overlay"
        else:
            module = "ext"

        content = pkg_resources.resource_string(module, file_path)
        root = os.path.join(os.path.expanduser('~'), ".edubot/cache")
        print("root", root)
        if not os.path.exists(root):
            os.makedirs(root)

        file_name = "%x" % hash(file_path)
        resource = os.path.join(root, file_name)

        if not os.path.exists(resource):

            print("file_name", file_name)
            print("resource", resource)

            with open(resource, "wb") as f:
                f.write(content)
        else:
            print("cache hit!")

        '''
        # resource = pkg_resources.resource_filename(module, file_path)

        root = os.path.dirname(resource)
        file_name = os.path.basename(resource)

        print("res=%s, dir=%s, base=%s" % (resource, root, file_name))
        '''

        return static_file(file_name, root=root)


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

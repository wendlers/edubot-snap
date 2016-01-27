import threading

import blockext
import blockext.generate


class BaseExtension(threading.Thread):

    def __init__(self, blocks_cls, port, name, description, menus=None):

        threading.Thread.__init__(self)

        self.daemon = True

        self.blocks_cls = blocks_cls
        self.port = port
        self.name = name
        self.description = description

        self.desc = blockext.Descriptor(
            name=self.name,
            port=self.port,
            blocks=blockext.get_decorated_blocks_from_class(self.blocks_cls),
            menus=menus,
        )

    def generate_snap(self):
        language = self.desc.translations["en"]
        return blockext.generate.generate_snap(self.desc, language)

    def run(self):
        extension = blockext.Extension(self.blocks_cls, self.desc)
        extension.run_forever(debug=True)

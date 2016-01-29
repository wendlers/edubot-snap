##
# The MIT License (MIT)
#
# Copyright (c) 2016 Stefan Wendler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##

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

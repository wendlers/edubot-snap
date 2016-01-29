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

import os

import edubot.client as client
import edubot.server as server

import edubot.snapext.nodebot as nodebot
import edubot.snapext.joystick as joystick
import edubot.snapext.tinr2d2 as tinr2d2


def run():

    ext_bot = nodebot.Extension()
    ext_bot.start()

    ext_js = joystick.Extension()
    ext_js.start()

    ext_r2d2 = tinr2d2.Extension()
    ext_r2d2.start()

    snp_srv = server.Httpd(
            doc_root_snap="../../ext/snap",
            doc_root_overlay="../../overlay/snap",
            snap_extensions=[ext_bot, ext_js, ext_r2d2])
    snp_srv.start()

    snp_cli = client.Browser(url="http://localhost:10000/snap/snap.html",
                             user_data_dir=os.path.join(os.path.expanduser('~'), ".edubot"))
    return snp_cli.start()

if __name__ == "__main__":

    exit(run())

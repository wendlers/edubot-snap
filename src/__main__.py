import os

import edubot.client as client
import edubot.server as server

import edubot.snapext.nodebot as nodebot
import edubot.snapext.joystick as joystick


if __name__ == "__main__":

    ext_bot = nodebot.Extension()
    ext_bot.start()

    ext_js = joystick.Extension()
    ext_js.start()

    snp_srv = server.Httpd(
            doc_root_snap="../../ext/snap",
            doc_root_overlay="../../overlay/snap",
            snap_extensions=[ext_bot, ext_js])
    snp_srv.start()

    snp_cli = client.Browser(url="http://localhost:10000/snap/snap.html",
                             user_data_dir=os.path.join(os.path.expanduser('~'), ".edubot"))
    ret = snp_cli.start()

    exit(ret)

    # raw_input("blah")
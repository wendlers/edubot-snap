import os

import client
import server

import snapext.nodebot as nodebot
import snapext.joystick as joystick


if __name__ == "__main__":

    ext_bot = nodebot.Blocks()
    ext_bot.start()

    ext_js = joystick.Blocks()
    ext_js.start()

    snp_srv = server.Httpd(snap_extensions=[ext_bot, ext_js])
    snp_srv.start()

    snp_cli = client.Browser(url="http://localhost:10000/snap/snap.html",
                             user_data_dir=os.path.join(os.path.expanduser('~'), ".edubot"))
    ret = snp_cli.start()

    exit(ret)


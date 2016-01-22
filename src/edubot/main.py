import snap
import server
import client
import os


if __name__ == "__main__":

    ext_bot = snap.EduBot()
    ext_bot.start()

    snp_srv = server.Httpd(snap_exts=[ext_bot])
    snp_srv.start()

    snp_cli = client.Browser(url="http://localhost:10000/snap/snap.html",
                             user_data_dir=os.path.join(os.path.expanduser('~'), ".edubot"))
    ret = snp_cli.start()

    exit(ret)


import snap
import server
import subprocess


if __name__ == "__main__":

    ext_bot = snap.EduBot()
    ext_bot.start()

    snp_srv = server.Httpd(snap_exts=[ext_bot])
    snp_srv.start()

    result = subprocess.call(["google-chrome",
                              "--app=http://localhost:10000/snap/snap.html",
                              "--user-data-dir=/home/stefan/.edubot"])

    exit(result)


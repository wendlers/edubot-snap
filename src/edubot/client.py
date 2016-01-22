import os
import subprocess


class AbstractBrowser:

    _binary = None

    def __init__(self, url, user_data_dir):

        self.user_data_dir = os.path.join(user_data_dir, self._binary)
        self.url = url

        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    @staticmethod
    def _available(binary):

        extensions = os.environ.get("PATHEXT", "").split(os.pathsep)

        for directory in os.environ.get("PATH", "").split(os.pathsep):
            base = os.path.join(directory, binary)

            options = [base] + [(base + ext) for ext in extensions]

            for filename in options:
                if os.path.exists(filename):
                    return True

        return False

    def _start(self, args):

        print("running: " + self._binary)

        try:
            subprocess.check_output([self._binary] + args)
        except subprocess.CalledProcessError as e:
            print(e.output)
            return e.returncode
        except Exception as e:
            print(e)
            return -1

        return 0

    def start(self):
        return -1

    @staticmethod
    def available():
        return False


class Chrome(AbstractBrowser):

    _binary = "google-chrome"

    @staticmethod
    def available():
        return AbstractBrowser._available(Chrome._binary)

    def start(self):
        args = ["--app=%s" % self.url]
        args += ["--user-data-dir=%s" % self.user_data_dir]
        return self._start(args)


class Chromium(Chrome):

    _binary = "xchromium"

    @staticmethod
    def available():
        return AbstractBrowser._available(Chromium._binary)


class Firefox(AbstractBrowser):

    _binary = "firefox"

    @staticmethod
    def available():
        return AbstractBrowser._available(Firefox._binary)

    def start(self):

        args = ["--profile", self.user_data_dir]
        args += ["--no-remote"]
        args += [self.url]
        return self._start(args)


class Browser:

    def __init__(self, url, user_data_dir=None):

        self.client = None

        for cls in [Chrome, Chromium, Firefox]:
            if cls.available():
                self.client = cls(url, user_data_dir)
                break

        if self.client is None:
            raise Exception("No suitable client found!")

    def start(self):
        return self.client.start()

import os
import re
import urllib.request

NON_URL_SKELETON = re.compile('^[A-Za-z0-9_-]+$')

class Skeleton:
    def __init__(self, skeleton):
        self._skeleton = skeleton

        if NON_URL_SKELETON.match(skeleton):
            self._url = 'https://git.team23.de/build/b5-skel-{skeleton}.git'.format(skeleton=skeleton)

            '''if it's not a public repository, clone using ssh in order to allow ssh key file auth'''
            if not self.__is_public_repository():
                self._url  = 'git@git.team23.de:build/b5-skel-{skeleton}.git'.format(skeleton=skeleton)

        else:
            self._url = skeleton

    def __is_public_repository(self):
        req = urllib.request.urlopen(self._url)
        req_url = req.geturl()

        if self._url == req_url or os.path.splitext(self._url)[0] == req_url :
            try:
                if req.getcode() == 200 :
                    return True
            except Exception:
                return False

        return False

    @property
    def url(self):
        return self._url

    @property
    def skeleton(self):
        return self._skeleton

import os
import re
import urllib.request
from urllib.error import URLError


class Skeleton:

    def __init__(self, skeleton):
        self._skeleton = skeleton

    def get_url(self):
        if not self._url:
            non_url_skeleton = re.compile('^[A-Za-z0-9_-]+$')
            if non_url_skeleton.match(self._skeleton):
                self._url = 'https://git.team23.de/build/b5-skel-{skeleton}.git'.format(skeleton=self._skeleton)
                '''if it's not a public repository, clone using ssh in order to allow ssh key file auth'''
                if not self.__is_public_repository(self._url):
                    self._url = 'git@git.team23.de:build/b5-skel-{skeleton}.git'.format(skeleton=self._skeleton)
            else:
                self._url = self._skeleton
        return self._url

    def __is_public_repository(self, url):
        request = urllib.request.urlopen(self._url)
        request_url = request.geturl()

        if self._url == request_url or os.path.splitext(self._url)[0] == request_url:
            try:
                if request.getcode() == 200:
                    return True
            except URLError:
                pass
        return False

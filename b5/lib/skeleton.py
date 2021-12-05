import re
import urllib.request
from urllib.error import URLError


class Skeleton:
    NON_URL_SKELETON = re.compile('^[A-Za-z0-9_-]+$')

    _url: str

    def __init__(self, skeleton_identified: str) -> None:
        self._skeleton_identified = skeleton_identified

    def get_url(self) -> str:
        try:
            return self._url
        except AttributeError:
            skeleton_url = self._skeleton_identified
            if self.NON_URL_SKELETON.match(skeleton_url):
                skeleton_url = 'https://git.team23.de/build/b5-skel-{skeleton}.git'.format(
                    skeleton=self._skeleton_identified,
                )
                # If it's not a public repository, clone using ssh in order to allow ssh key file auth
                if not self._is_public_repository(skeleton_url):
                    skeleton_url = 'git@git.team23.de:build/b5-skel-{skeleton}.git'.format(
                        skeleton=self._skeleton_identified,
                    )
            self._url = skeleton_url
            return self._url

    def _is_public_repository(self, url: str) -> bool:
        request = urllib.request.urlopen(url)
        request_url = request.geturl()

        if url == request_url or url.rsplit('.', 1)[0] == request_url:
            try:
                if request.getcode() == 200:
                    return True
            except URLError:
                pass
        return False

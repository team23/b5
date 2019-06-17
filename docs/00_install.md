# Installing b5

## Mac OS X

```bash
brew tap team23/b5 https://git.team23.de/build/homebrew-b5.git
brew install b5
```

## Installing as normal Python package

When manually installing b5 I recommend using [pipsi](https://github.com/mitsuhiko/pipsi) to keep b5 and its
dependencies separated from the system packages. You may install it using:

```bash
pipsi install --python python3 b5
```

You may of course instead just do a normal pip install:

```bash
pip3 install b5
```

OR

```bash
git clone git@git.team23.de:build/b5.git
cd b5
pip install .
```

## Development installation (using live version of b5 repository)

```bash
cd work/path/
git clone git@git.team23.de:build/b5.git
cd b5
pipenv install --dev
```

or if you have b5 installed already

```bash
cd work/path/
git clone git@git.team23.de:build/b5.git
cd b5
b5 install  # ;-)
```

# Additional dependencies

**Note:** These dependencies are purely optional and are usually only needed at TEAM23 for our own
project setup. If you don't work at TEAM23 you probably don't need them or at least not all.

You may need to install the following packages in addition, as some of the projects might/will
require them:

* python2 and python3
* virtualenv
* pyenv and pipenv
* sassc
* docker
* docker-sync
* composer
* node/npm and yarn
* rsync
* wget and curl

Use the following commands to install everything on Mac OS X:
```bash
brew install python python@2 curl node pipenv pyenv rsync sassc wget yarn composer
brew postinstall python
brew postinstall python@2
brew cask install docker
sudo pip install virtualenv
sudo gem install docker-sync
```

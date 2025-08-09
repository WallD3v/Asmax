from setuptools import setup, find_packages

def readme():
  with open('README.rst', 'r') as f:
    return f.read()

setup(
  name='Asmax',
  version='0.1.1',
  author='WallD3v',
  author_email='walldevnewthon@gmail.com',
  description='Max Messanger UserAPI library',
  url='https://github.com/WallD3v/Asmax',
  packages=find_packages(),
  install_requires=['websocket-client==1.8.0','UserAgenter==1.3.1'],
  keywords='max messanger userapi api user',
  project_urls={
    'Telegram': 'https://t.me/wdp_owner'
  },
  python_requires='>=3.9'
)
#coding:utf-8

# from os.path import dirname, join
try:
    from pip.req import parse_requirements
except:
    from pip._internal.req import parse_requirements

from setuptools import find_packages,setup


# with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
#     version = f.read().decode('ascii').strip()

with open("VERSION.txt","rb") as f:
    version = f.read().strip()
    """
        作为一个合格的模块，应该要有版本号哦。
    """
setup(
    name='Screepy',    # 模块名称
    version=version,         #安装框架后的版本号
    description='A mini spider framework, like Scrapy',    # 描述
    packages=find_packages(exclude=[]),
    author='dirk2823',
    author_email='dirk2823@foxmail.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='#',
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],#所需的运行环境
    zip_safe=False, #表示在windows中可以正常卸载
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
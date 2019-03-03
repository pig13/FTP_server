#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import hashlib
import os


def check_md5(contents=None, file_path=None):
    """
    检测内容或文件的MD5值
    :param contents:
    :param file_path:
    :return:
    """
    if file_path:
        if not os.path.isfile(file_path):
            return
        file_hash = hashlib.md5()
        f = open(file_path, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            file_hash.update(b)
        f.close()
        return file_hash.hexdigest()
    elif contents:
        contents_hash = hashlib.md5()
        contents_hash.update(contents.encode('utf-8'))
        return contents_hash.hexdigest()
    else:
        return ''


def encryption_pwd(pwd):
    """
    加密密码，
    :param pwd:
    :return:
    """
    hash = hashlib.sha256()
    hash.update(pwd.encode('utf-8'))
    return hash.hexdigest()

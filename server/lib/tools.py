#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'

import os
import hashlib


def get_size(root):
    """
    获取当前文件夹或者文件大小
    :param root:
    :return: int
    """
    root_size = 0
    if os.path.isdir(root):
        for parent, dir_names, file_name in os.walk(root):
            for file in file_name:
                root_size += os.path.getsize(os.path.join(parent, file))
    else:
        root_size += os.path.getsize(root)
    return root_size


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

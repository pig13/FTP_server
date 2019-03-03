#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'

import os
from lib.cmd import execute_cmd
from lib.tools import get_size
from conf import settings

sql = __import__('db.' + settings.SQL, fromlist=[settings.SQL])
sql = sql.Db


class User:
    __ROOT = settings.USER_ROOT  # 所有用户的根目录
    UPLOADING_FOLDER = 'uploading'  # 存放用户上传文件的文件夹,在用户文件的根目录下。

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_root = os.path.join(__class__.__ROOT, self.user_id)
        self.current_folder = self.user_root
        if not os.path.isdir(self.user_root):
            execute_cmd('md {}'.format(self.user_id), __class__.__ROOT)
            execute_cmd('md {}'.format(__class__.UPLOADING_FOLDER), self.user_root)

        self.uploading_folder_path = os.path.join(self.user_root, __class__.UPLOADING_FOLDER)
        # 通过数据库操作获取用户空间大小
        self.user_sql = sql(user_id)
        self.total_space_size = self.user_sql.total_space_size
        self.remaining_space_size = self.user_sql.remaining_space_size

    def save(self):
        self.user_sql.save()

    def enter_upper_contents(self):
        """
        返回上层目录并展示，如果有权限的
        :return:
        """
        if os.path.dirname(self.current_folder) != __class__.__ROOT:
            self.current_folder = os.path.dirname(self.current_folder)
            return self.show_file()
        else:
            return 'No authority'

    def enter_lower_contents(self, folder):
        """
        进入下层目录,并展示
        :param folder:
        :return:
        """
        if os.path.isdir(os.path.join(self.current_folder, folder)):
            self.current_folder = os.path.join(self.current_folder, folder)
            return self.show_file()
        else:
            return 'File does not exist'

    def create_folder(self, folder_name):
        """
        在当前文件夹下新建文件夹
        :param folder_name:
        :return:
        """
        execute_cmd('md {}'.format(folder_name), self.current_folder)
        return True

    def clear_empty_file(self):
        """
        清空用户家目录下的空文件和空文件夹,并返回到家目录
        :return: bool
        """
        for parent, dir_names, file_names in os.walk(self.user_root):
            for file in file_names:
                if get_size(os.path.join(parent, file)) == 0:
                    os.remove(os.path.join(parent, file))
            for folder in dir_names:
                if get_size(os.path.join(parent, folder)) == 0:
                    os.rmdir(os.path.join(parent, folder))
        self.current_folder = self.user_root
        # 如果误删uploading文件夹，恢复
        if not os.path.isdir(self.uploading_folder_path):
            execute_cmd('md {}'.format(__class__.UPLOADING_FOLDER), self.user_root)
        return self.show_file()

    def show_file(self):
        """
        查看当前文件下的文件和文件夹
        :return:
        """
        file_parent, file_name = os.path.split(self.current_folder)
        # print(file_parent, file_name)
        ret = execute_cmd('dir {}'.format(file_name), file_parent).decode('gbk')
        # text = re.search(file_parent + '(.*?)', ret)

        # ret = file_name + ret.split(file_name)[-1]
        return ret

    def uploading_files(self, file_name):
        """
        上传文件，打开文件返回文件句柄
        :return:
        """
        real_path = os.path.join(self.uploading_folder_path, file_name)
        if os.path.isfile(real_path):
            f = open(real_path, 'ab')
        else:
            f = open(real_path, 'wb')
        return f

    def download_files(self, file_name, seek=0):
        """
        下载文件，打开文件返回文件句柄 和 文件总大小
        :param file_name:
        :param seek: 文件开始读取位置
        :return:
        """
        real_path = os.path.join(self.uploading_folder_path, file_name)
        file_size = os.path.getsize(real_path)
        f = open(real_path, 'rb')
        f.seek(seek)
        return f, file_size

    @classmethod
    def login_auth(cls, user_id, pwd):
        """
        调用数据库接口进行登录验证
        :param user_id:
        :param pwd:
        :return: bool
        """
        if sql.login(user_id, pwd):
            return True
        else:
            return False

    @classmethod
    def register(cls, user_id, pwd):
        """
        调用数据库接口进行登注册
        :param user_id:
        :param pwd:
        :return: bool
        """
        if sql.register(user_id, pwd):
            return True
        else:
            return False

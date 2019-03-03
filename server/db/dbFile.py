#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'


from conf import settings
from db.dbMode import DbMode
import os

# 文件数据库
FILE = os.path.join(settings.BASE_DIR, r'db\account')
SIZE = settings.USER_SPACE_SIZE


class Db(DbMode):
    def __init__(self, user_id=None):
        self.id = user_id
        if user_id:
            with open(FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip().split('\t')
                    if line[0] == user_id:
                        self.pwd = line[1]
                        self.total_space_size = int(line[2])
                        self.remaining_space_size = int(line[3])

    def save(self):
        with open(FILE, 'r', encoding='utf-8') as f:
            with open(FILE + '_', 'w', encoding='utf-8') as f2:
                for line in f:
                    if line.strip().split('\t')[0] == self.id:
                        f2.write('{}\t{}\t{}\t{}\n'.format(self.id, self.pwd, self.total_space_size,
                                                           self.remaining_space_size))
                    else:
                        f2.write(line)
                f2.flush()
        os.remove(FILE)
        os.rename(FILE + '_', FILE)

    @classmethod
    def login(cls, user, pwd):
        """
        查询文件，账号，密码是否正确
        :param user:
        :param pwd:
        :return:
        """
        login_success = False
        with open(FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if [user, pwd] == line.strip().split('\t')[:2]:
                    login_success = True
                    break
        return login_success

    @classmethod
    def register(cls, user, pwd):
        """
        查询文件，是否有此账号，有返回FALSE,没有在数据库中建立新纪录，返回True
        :param user:
        :param pwd:
        :return:
        """
        register_success = False
        register_already = False
        with open(FILE, 'r+', encoding='utf-8') as f:
            for line in f:
                if user == line.strip().split('\t')[0]:
                    register_already = True
                    f.seek(0, 2)
                    break
            if not register_already:
                f.write('{}\t{}\t{}\t{}\n'.format(user, pwd, SIZE, SIZE))
                register_success = True
        return register_success


if __name__ == '__main__':
    # 测试本模块，而且当前项目不是作为一个项目打开，需要加入以下三行代码
    # import sys
    # import os
    # sys.path.append(os.path.dirname(os.getcwd()))
    pass

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'


# 测试本模块，而且当前项目不是作为一个项目打开，需要加入以下三行代码
# import sys
# import os
# sys.path.append(os.path.dirname(os.getcwd()))
from db.dbMode import DbMode


# MySQL数据库

class Db(DbMode):
    @classmethod
    def login(cls, user, pwd):
        pass

    @classmethod
    def register(cls, user, pwd):
        pass

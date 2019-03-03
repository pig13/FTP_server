#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'


class DbMode(object):

    @classmethod
    def login(cls, user, pwd):
        """
        查询数据库，账号，密码是否正确
        :param user:
        :param pwd:
        :return: bool
        """
        raise NotImplementedError('没有实现login方法')

    @classmethod
    def register(cls, user, pwd):
        """
        查询数据库，是否有此账号，有返回FALSE,没有在数据库中建立新纪录，返回True
        :param user:
        :param pwd:
        :return: bool
        """
        raise NotImplementedError('没有实现register方法')

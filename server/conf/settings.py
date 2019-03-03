#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SQL = 'dbFile'
# SQL = 'dbMySQL'
# SQL = 'dbSQLServer'


USER_SPACE_SIZE = 1024 * 1024 * 1024  # 1GB

USER_ROOT = os.path.join(BASE_DIR, 'files')

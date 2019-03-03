#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import subprocess


def execute_cmd(cmd, path):
    """
    在windows操作系统指定路径下执行命令并返回结果
    :param cmd:
    :param path:
    :return:
    """
    cmd = 'cd {} && {}'.format(path, cmd)
    ret = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout = ret.stdout.read()
    stderr = ret.stderr.read()
    return stdout if stdout else stderr

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import socket
from core.client import *
from lib.tools import check_md5, encryption_pwd


def show_choice():
    """

    :return: str
    """
    print('请选择操作：')
    print('-->返回上一级目录(1)')
    print('-->进入下一级目录(2)')
    print('-->新建文件夹(3)')
    print('-->清空空文件(4)')
    print('-->查看当前文件夹(5)')
    print('-->上传文件(6)')
    # print('-->下载文件(7)')  # 未实现
    print('-->退出(0)')
    while True:
        operation = input('-->').strip()
        if operation.isdigit() and 0 <= int(operation) <= 7:
            break
        else:
            print('输入错误，请重新选择。')
    return operation


def show_user_authentication():
    """

    :return: str
    """
    print('请选择操作：')
    print('-->登录(1)')
    print('-->注册(2)')
    print('-->退出(0)')
    while True:
        operation = input('-->').strip()
        if operation.isdigit() and 0 <= int(operation) <= 3:
            break
        else:
            print('输入错误，请重新选择。')
    return operation


def run():
    client = socket.socket()
    client.connect(('127.0.0.1', 8899))
    # socket 数据交互
    while True:
        operation_auth = show_user_authentication()
        if operation_auth == '0':
            # 退出
            send_data_packet_client(client, operation=operation_auth)
            break
        elif operation_auth == '1':
            # 登录
            user = input('user:')
            pwd = input('password:')
            encrypt_pwd = encryption_pwd(pwd)
            send_data_packet_client(client, operation=operation_auth, account=user, password=encrypt_pwd)
            ret_state_code = recv_state_code_client(client)
            if ret_state_code == 1:
                print('login success')
                break
            else:
                print('login fail')
        elif operation_auth == '2':
            # 注册
            user = input('user:')
            pwd = input('password:')
            encrypt_pwd = encryption_pwd(pwd)
            send_data_packet_client(client, operation=operation_auth, account=user, password=encrypt_pwd)
            ret_state_code = recv_state_code_client(client)
            if ret_state_code == 1:
                print('register success')
                break
            else:
                print('register fail')
    while operation_auth != '0':
        operation = show_choice()
        if operation == '0':
            send_data_packet_client(client, operation=operation)
            break
        elif operation == '1':
            # enter_upper_contents,进入上层目录
            send_data_packet_client(client, operation=operation)
            ret_data = recv_data_client(client).decode('utf-8')
            print(ret_data)
        elif operation == '2':
            # enter_lower_contents,进入下层目录
            lower_contents_name = input('folder name:')
            send_data_packet_client(client, operation=operation, lower_contents_name=lower_contents_name)
            ret_data = recv_data_client(client).decode('utf-8')
            print(ret_data)
        elif operation == '3':
            # create_folder,创建新文件夹
            new_folder_name = input('new folder name:')
            send_data_packet_client(client, operation=operation, new_folder_name=new_folder_name)
            ret_state = recv_state_code_client(client)
            if ret_state:
                print('create success')
            else:
                print('create fail')
        elif operation == '4':
            # clear_empty_file，清空空文件和空文件夹
            send_data_packet_client(client, operation=operation)
            ret_data = recv_data_client(client).decode('utf-8')
            print(ret_data)
        elif operation == '5':
            # show_file,展示当前文件夹内的文件信息
            send_data_packet_client(client, operation=operation)
            ret_data = recv_data_client(client).decode('utf-8')
            print(ret_data)
        elif operation == '6':
            # uploading_files,上传文件
            while True:
                file_path = input('file path:')
                if os.path.isfile(file_path):
                    break
                else:
                    print('路径错误')
            name = os.path.basename(file_path.rstrip('\/'))
            size = os.path.getsize(file_path)
            md5 = check_md5(file_path=file_path)
            send_data_packet_client(client, operation=operation, uploading_files_name=name, uploading_file_size=size,
                                    uploading_file_md5=md5)
            flag_check_md5 = send_data_file_client(client, file_path=file_path)
            if flag_check_md5:
                print('文件上传完整')
            else:
                print('文件上传不完整')
        elif operation == '7':
            # download_files,下载文件，未实现
            pass

    client.close()


if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    run()

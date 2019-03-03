#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'

import socketserver
import struct
import json
import os
from lib.tools import check_md5
from core.user import User


class Server(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            # login_auth
            headers_login_auth = self.recv_data_packet_server()
            if headers_login_auth['operation'] == '0':
                # 退出
                break
            elif headers_login_auth['operation'] == '1':
                # 登录
                account = headers_login_auth['account']
                password = headers_login_auth['password']
                ret_login = User.login_auth(account, password)  # ret_login true false
                if ret_login:
                    self.send_state_code_server(1)
                    break
                else:
                    self.send_state_code_server(0)
            elif headers_login_auth['operation'] == '2':
                # 注册
                account = headers_login_auth['account']
                password = headers_login_auth['password']
                ret_register = User.register(account, password)  # ret_register  true false
                if ret_register:
                    self.send_state_code_server(1)
                    break
                else:
                    self.send_state_code_server(0)
        if headers_login_auth['operation'] != '0':
            # 当用户认证成功进入此模块
            user = User(headers_login_auth['account'])
            while True:
                # operation_choice
                headers_operation = self.recv_data_packet_server()
                if headers_operation['operation'] == '0':
                    # exit
                    break
                elif headers_operation['operation'] == '1':
                    # enter_upper_contents,进入上层目录
                    ret_data = user.enter_upper_contents()
                    self.send_data_server(ret_data)
                elif headers_operation['operation'] == '2':
                    # enter_lower_contents,进入下层目录
                    lower_contents_name = headers_operation['lower_contents_name']
                    ret_data = user.enter_lower_contents(lower_contents_name)
                    self.send_data_server(ret_data)
                elif headers_operation['operation'] == '3':
                    # create_folder,创建新文件夹
                    new_folder_name = headers_operation['new_folder_name']
                    ret_state = user.create_folder(new_folder_name)
                    ret_state = 1 if ret_state else 0
                    self.send_state_code_server(ret_state)
                elif headers_operation['operation'] == '4':
                    # clear_empty_file，清空空文件和空文件夹
                    ret_data = user.clear_empty_file()
                    self.send_data_server(ret_data)
                elif headers_operation['operation'] == '5':
                    # show_file,展示当前文件夹内的文件信息
                    ret_data = user.show_file()
                    self.send_data_server(ret_data)
                elif headers_operation['operation'] == '6':
                    # uploading_files,上传文件
                    self.recv_data_file_server(headers_operation, user)
                elif headers_operation['operation'] == '7':
                    # download_files,下载文件，未实现
                    pass
        self.request.close()

    def recv_data_packet_server(self):
        """
        从客户端接受一个数据报头，保证不粘包，并解析出数据。
        :return:
        """
        headers_json_bytes_len_pack = self.request.recv(4)
        headers_json_bytes_len = struct.unpack('i', headers_json_bytes_len_pack)[0]
        headers_json_bytes = self.request.recv(headers_json_bytes_len)
        headers_json = headers_json_bytes.decode('utf-8')
        headers = json.loads(headers_json)
        return headers

    def recv_data_file_server(self, headers, user):
        """
        接受客户端的发来的文件，进行断点续传，检查文件一致性。
        :param headers:
        :param user:
        :return:
        """
        uploading_file_size = headers.get('uploading_file_size')
        if user.remaining_space_size < uploading_file_size:
            exit_flag = -1
            exit_flag_pack = struct.pack('i', exit_flag)
            self.request.send(exit_flag_pack)
            return

        uploading_files_name = headers.get('uploading_files_name')
        uploading_file_md5 = headers.get('uploading_file_md5')
        file_path = os.path.join(user.uploading_folder_path, uploading_files_name)
        file_seek = 0
        if os.path.isfile(file_path):
            file_seek = os.path.getsize(file_path)
        file_seek_pack = struct.pack('i', file_seek)
        self.request.send(file_seek_pack)
        self.recv_data_server(file_handle=user.uploading_files(uploading_files_name))
        server_md5 = check_md5(file_path=file_path)

        user.user_sql.remaining_space_size -= uploading_file_size
        user.user_sql.save()

        flag_check_md5 = 0  # 0为假，1为真
        if uploading_file_md5 == server_md5:
            flag_check_md5 = 1
        self.request.send(struct.pack('i', flag_check_md5))

    def recv_data_server(self, file_handle=None):
        data_size_pack = self.request.recv(4)
        data_size = struct.unpack('i', data_size_pack)[0]
        if file_handle:
            while True:
                if data_size > 1024:
                    data = self.request.recv(1024)
                    file_handle.write(data)
                    data_size -= len(data)
                else:
                    data = self.request.recv(data_size)
                    file_handle.write(data)
                    break
                    # 保证接受完所有数据，可能导致因最后一点数据丢失而阻塞
                    # if len(data) == data_size:
                    # break
                    # data_size -= len(data)
            file_handle.close()
            return
        else:
            total_data = bytes()
            while True:
                if data_size > 1024:
                    data = self.request.recv(1024)
                    total_data += data
                    data_size -= 1024
                else:
                    data = self.request.recv(data_size)
                    total_data += data
                    break
            return total_data

    def send_data_server(self, content='', file_data_size=None, file_handle=None):
        """
        发送数据
        :param content:
        :param file_data_size:
        :param file_handle: 文件句柄
        :return:
        """
        if file_handle:
            data_len_pack = struct.pack('i', file_data_size)
            self.request.send(data_len_pack)
            self.request.sendfile(file_handle)
        else:
            if not isinstance(content, bytes):
                content = content.encode('utf-8')
            content_size = len(content)
            content_size_pack = struct.pack('i', content_size)
            self.request.send(content_size_pack)
            self.request.sendall(content)
        pass

    def send_state_code_server(self, state_code):
        """
        给客户端发送状态码
        :param state_code:
        :return:
        """
        if not isinstance(state_code, int):
            state_code = int(state_code)
        state_code_pack = struct.pack('i', state_code)
        self.request.send(state_code_pack)

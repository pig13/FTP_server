#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import json
import struct
import os

operation_user_authentication = {
    1: 'login_auth',
    2: 'register',
    0: 'exit',
}
operation_choice = {
    0: 'exit',
    1: 'enter_upper_contents',
    2: 'enter_lower_contents',
    3: 'create_folder',
    4: 'clear_empty_file',
    5: 'show_file',
    6: 'uploading_files',
    7: 'download_files'
}


def send_data_packet_client(conn, operation, account=None, password=None, new_folder_name=None,
                            lower_contents_name=None, uploading_files_name=None, uploading_file_md5=None,
                            uploading_file_size=None, download_file_name=None):
    """
    向服务端发送一个数据报头，保证不粘包。
    :param conn: 连接
    :param operation: exit,enter_upper_contents,enter_lower_contents,create_folder,clear_empty_file,show_file,
    uploading_files,download_files,login_auth,register
    :param account: user id
    :param password: user password
    :param new_folder_name:
    :param lower_contents_name:
    :param uploading_files_name:
    :param uploading_file_md5:
    :param uploading_file_size:
    :param download_file_name:
    :return:
    """
    headers = {'operation': operation}
    if account:
        headers['account'] = account
    if password:
        headers['password'] = password
    if new_folder_name:
        headers['new_folder_name'] = new_folder_name
    if lower_contents_name:
        headers['lower_contents_name'] = lower_contents_name
    if uploading_files_name:
        headers['uploading_files_name'] = uploading_files_name
    if uploading_file_md5:
        headers['uploading_file_md5'] = uploading_file_md5
    if uploading_file_size:
        headers['uploading_file_size'] = uploading_file_size
    if download_file_name:
        headers['download_file_name'] = download_file_name

    headers_json = json.dumps(headers)
    headers_json_bytes = bytes(headers_json, encoding='utf-8')
    headers_json_bytes_len = len(headers_json_bytes)
    headers_json_bytes_len_pack = struct.pack('i', headers_json_bytes_len)
    conn.send(headers_json_bytes_len_pack)
    conn.sendall(headers_json_bytes)


def send_data_client(conn, content='', file_data_size=None, file_handle=None):
    """
    发送数据
    :param conn:
    :param content:
    :param file_data_size:
    :param file_handle: 文件句柄
    :return:
    """
    if file_handle:
        data_len_pack = struct.pack('i', file_data_size)
        conn.send(data_len_pack)
        conn.sendfile(file_handle)
        # conn.send(file_handle.read())
    else:
        if not isinstance(content, bytes):
            content = content.encode('utf-8')
        content_size = len(content)
        content_size_pack = struct.pack('i', content_size)
        conn.send(content_size_pack)
        conn.sendall(content)


def send_data_file_client(conn, file_path):
    """
    发送文件数据。
    :param conn:
    :param file_path:
    :return: 0 1
    """
    seek_pack = conn.recv(4)
    seek = struct.unpack('i', seek_pack)[0]
    if seek == -1:
        return 'Lack of space'
    f = open(file_path, 'rb')
    f.seek(seek)
    data_size = os.path.getsize(file_path) - seek
    send_data_client(conn, file_data_size=data_size, file_handle=f)
    flag_check_md5_pack = conn.recv(4)
    flag_check_md5 = struct.unpack('i', flag_check_md5_pack)[0]
    # flag_check_md5 返回1 0 表示上传文件是否完整。
    return flag_check_md5


def recv_data_client(conn, file_handle=None):
    """
    接收数据
    :param conn:
    :param file_handle:
    :return:
    """
    data_size_pack = conn.recv(4)
    data_size = struct.unpack('i', data_size_pack)[0]
    if file_handle:
        while True:
            if data_size > 1024:
                data = conn.recv(1024)
                file_handle.write(data)
                data_size -= 1024
            else:
                data = conn.recv(data_size)
                file_handle.write(data)
                break
        file_handle.close()
        return
    else:
        total_data = bytes()
        while True:
            if data_size > 1024:
                data = conn.recv(1024)
                total_data += data
                data_size -= 1024
            else:
                data = conn.recv(data_size)
                total_data += data
                break
        return total_data


def recv_state_code_client(conn):
    """
    接收状态码
    :param conn:
    :return: int
    """
    state_code_pack = conn.recv(4)
    state_code = struct.unpack('i', state_code_pack)[0]
    return state_code

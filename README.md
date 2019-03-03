此程序是一个基于socket的FTP服务器，包括客户端和服务端，主要实现了：处理粘包，多用户登录，上传、下载文件，断点续传，简单命令操作。    
### 功能需求：
1. 支持多用户同时登录，服务端采用SocketServer实现
2. 用户加密认证
3. 上传/下载文件，保证文件一致性(下载文件未实现)
4. 对用户访问目录进行限制，只能在自己根目录下访问，不能切入其他目录
5. 对用户的空间进行限制，默认1GB
6. 支持端点续传
7. 用户可以创建文件、切换目录、删除文件、查看文件



### 运行环境
python 3.7.2  
client依赖模块:socket,json,struct，os,sys,hashlib  
client依赖模块:socketserver,os,sys,json,struct，subprocess,hashlib  
全为python内置模块  

### 程序目录

```text

client:
   |--start.py            (程序入口)
   | 
   |--bin                 (可执行文件目录）
   |  |-- ftp_client.py   (主接口文件,登录接口）
   | 
   |--core                (主程序目录)
   |  |-- client.py       (传输数据接口)
   |
   |--download            (文件下载存放目录)
   |
   |--lib                 (模块目录)
   |  |-- tools.py        (工具模块)

----------------------------------------------------------

server:
   |--start.py            (程序入口)
   | 
   |--bin                 (可执行文件目录）
   |  |-- ftp_server.py   (启动socket服务）
   |
   |--conf                (配置文件目录)
   |  |-- settings.py     (主配置文件)
   | 
   |--core                (主程序目录)
   |  |-- server.py       (传输数据接口)
   |  |-- user.py         (用户操作接口)
   |
   |--db                  (数据库配置目录)
   |  |-- account.py      (文件数据库)
   |  |-- dbFile.py       (文件数据库接口)
   |  |-- dbMode.py       (数据库接口模板)
   |  |-- dbMySQl.py      (MySQL数据库接口)
   |  |-- dbSQLServer.py  (SQLServer数据库接口)
   |
   |--files               (用户目录)
   |  |-- test            (测试用户)
   |  |  |-- uploading    (上传文件存放目录)
   |
   |--lib                 (模块目录)
   |  |-- cmd.py          (命令模块)
   |  |-- tools.py        (工具模块)
   |
   |--log                 (日志目录)
   
   
README.md                 (程序说明)

```






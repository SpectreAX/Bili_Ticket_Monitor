# Bili_Ticket_Monitor

开源免费，简单易上手，实时监测Bilibili会员购余票状态

> [!NOTE]
> 本程序仅供学习交流, 不得用于商业用途。
>
> 使用本程序进行违法操作产生的法律责任由操作者自行承担。

 ## 使用教程

### 一、安装

 - 请先安装Python和pip

 ```shell
 git clone https://github.com/TaiMiao/Bili_Ticket_Monitor
 cd Bili_Ticket_Monitor
 pip install requests
 pip install time
 pip install json
 pip install datetime
 pip install colorama
```
### 二、配置
- 如图，将你需要监测的展会ID填入对应的地方，其余配置根据文件内注释可自行更改
![image](https://github.com/user-attachments/assets/7a1cf2a8-ccca-44ab-acd7-4d6abdbf99c2)

### 三、运行
- 配置完成后直接运行`Bili_Ticket_Monitor.py`

### 四、注意事项
- 如果请求速度太快了可能会被业务风控，如图是典型的412风控：
![image](https://github.com/user-attachments/assets/43b50d6a-5ac0-405d-9c2c-dfbe8a8861cb)

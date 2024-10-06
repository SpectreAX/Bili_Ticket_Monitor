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
 pip install requests
 pip install time
 pip install datetime
 pip install colorama
 pip install tabulate
 pip install wcwidth
```
### 二、配置
- 如图，将你需要监测的票务ID填入对应的地方，其余配置根据文件内注释可自行更改，不让改的地方请别乱改
![image](https://github.com/user-attachments/assets/617230f6-cad2-461d-8787-9ce46294f494)



### 三、运行
- 配置完成后直接运行`Bili_Ticket_Monitor.py`
- 效果：
- ![image](https://github.com/user-attachments/assets/f3da27c6-888a-45f8-a7d2-e2a66cc239e7)



### 四、注意事项
- 请求间隔时间太短可能会被业务风控

import requests
import time
from datetime import datetime
from colorama import Fore, Style, init
import os

# 清屏函数，只清理屏幕的时间行，保留票务信息
def clear_screen_line():
    print("\033[F\033[K", end="")  # 将光标移到上一行并清除该行内容

# 初始化颜色输出
init(autoreset=True)

# 获取票务状态的函数
def fetch_ticket_status(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=100)  # 设置超时时间，避免长时间无响应
        response.raise_for_status()  # 检查响应状态码是否为200
        data = response.json()
        tickets = data.get('data', {}).get('screen_list', [])
        if not tickets:
            print("票务数据为空，请检查票务ID")
            return None

        # 构建表格数据
        table = []
        for screen in tickets:
            for ticket in screen.get('ticket_list', []):
                screen_name = ticket.get('screen_name', '')
                ticket_desc = ticket.get('desc', '')
                if ticket_desc == "普通票":
                    ticket_desc = "普通票\t\t"
                sale_status = ticket.get('sale_flag', {}).get('display_name', '')
                table.append([screen_name + ticket_desc, sale_status])

        return table

    except requests.exceptions.RequestException as e:
        print(f"请求错误(可能被风控): {e}")
        return None

# 打印票务表格的函数
def print_ticket_table(table):
    if not table:
        return

    # 计算每列的最大宽度
    max_desc_len = max(len(row[0]) for row in table)
    max_status_len = max(len(row[1]) for row in table)

    # 打印表头，确保列对齐
    header = f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}{'状态'.ljust(max_status_len)}{Style.RESET_ALL}"
    print(header)
    
    # 打印加长的分界线，保持与表头一致
    print('-' * (max_desc_len + max_status_len + 8))  # 增加额外长度以保证视觉效果

    # 打印表格内容
    for row in table:
        desc = Fore.YELLOW + row[0].ljust(max_desc_len) + Style.RESET_ALL
        status = Fore.GREEN + row[1].ljust(max_status_len) + Style.RESET_ALL
        print(f"{desc} {status}")  # 确保每一行与表头对齐

# 检查表格数据是否变化的函数
def has_table_changed(old_table, new_table):
    return old_table != new_table

# 显示时间的函数
def display_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}当前时间: {current_time}{Style.RESET_ALL}")

# 主程序
url = "https://show.bilibili.com/api/ticket/project/getV2?version=134&id=92785"  # 替换为实际票务ID
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

last_table = None  # 用于记录上一次的表格内容

# 初始获取票务状态
new_table = fetch_ticket_status(url, headers)
if new_table:
    print_ticket_table(new_table)
    last_table = new_table

# 进入主循环，持续刷新时间
    while True:
        try:
            # 显示当前时间，并刷新时间显示（不清屏票务信息）
            clear_screen_line()
            display_time()
            # 短暂休眠，保持时间流畅刷新
            time.sleep(1)
            # 每隔 2 秒刷新一次票务信息
            if time.time() % 2 < 1:
                new_table = fetch_ticket_status(url, headers)
                if new_table and has_table_changed(last_table, new_table):
                    print_ticket_table(new_table)  # 重新打印票务表格
                    last_table = new_table
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ticket status: {e}")
            break  # 停止循环

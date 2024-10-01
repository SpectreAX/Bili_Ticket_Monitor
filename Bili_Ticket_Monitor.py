import requests
import time
from datetime import datetime
from colorama import Fore, Style, init

# 常量声明
URL = "https://show.bilibili.com/api/ticket/project/getV2?version=134&id=替换这里"  # 请将此处替换为票务ID
TIMEOUT = 100  # 请求超时时间
SLEEP_INTERVAL = 0.9  # 时间显示刷新间隔，建议不要更改
TICKET_REFRESH_INTERVAL = 2  # 票务信息刷新间隔，直接影响风控概率
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# 清屏函数，只清理屏幕的时间行，保留票务信息
def clear_screen_line():
    print("\033[F\033[K", end="")  # 将光标移到上一行并清除该行内容

# 初始化颜色输出
init(autoreset=True)

# 获取票务状态
def fetch_ticket_status(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        tickets = data.get('data', {}).get('screen_list', [])
        name = data.get('data', {}).get('name', '')
        
        if not tickets:
            print("票务数据为空，请检查票务ID")
            return None, None

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

        return name, table

    except requests.exceptions.RequestException as e:
        print(f"请求错误(可能被风控): {e}")
        return None, None

# 打印票务信息表
def print_ticket_table(name, table):
    if not table:
        return

    # 计算每列的最大宽度
    max_desc_len = max(len(row[0]) for row in table)
    max_status_len = max(len(row[1]) for row in table)

    # 打印表头，确保列对齐
    header = f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}{'状态'.ljust(max_status_len)}{Style.RESET_ALL}"
    print(f"{Style.BRIGHT}{name}")
    print(header)
    
    # 打印加长的分界线，保持与表头一致
    print('-' * (max_desc_len + max_status_len + 16))  # 增加额外长度以保证视觉效果

    # 打印表格内容
    for row in table:
        desc = Fore.WHITE + row[0].ljust(max_desc_len) + Style.RESET_ALL
        
        # 根据状态设置颜色
        status = row[1]
        if status == "已售罄" or status == "已停售":
            status_colored = Fore.RED + status.ljust(max_status_len) + Style.RESET_ALL
        elif status == "暂时售罄":
            status_colored = Fore.YELLOW + status.ljust(max_status_len) + Style.RESET_ALL
        elif status == "预售中":
            status_colored = Fore.GREEN + status.ljust(max_status_len) + Style.RESET_ALL
        else:
            status_colored = status.ljust(max_status_len)  # 默认颜色

        print(f"{desc} {status_colored}")  # 确保每一行与表头对齐

# 检查表格数据是否变化
def has_table_changed(old_table, new_table):
    return old_table != new_table

# 显示时间
def display_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}当前时间: {current_time}{Style.RESET_ALL}")

# 主程序
def main():
    last_table = None  # 用于记录上一次的表格内容

    # 初始获取票务状态
    name, new_table = fetch_ticket_status(URL, HEADERS)

    # 检查票务信息是否为空
    if new_table is None:
        return  # 退出程序

    print_ticket_table(name, new_table)
    last_table = new_table

    # 进入主循环，持续刷新时间和票务信息
    while True:
        try:
            # 每隔指定时间刷新一次票务信息
            if time.time() % TICKET_REFRESH_INTERVAL < 1:
                name, new_table = fetch_ticket_status(URL, HEADERS)

                # 检查票务信息是否为空，若为空则退出循环
                if new_table is None:
                    break  # 退出循环

                if has_table_changed(last_table, new_table):
                    print_ticket_table(name, new_table)  # 重新打印票务表格
                    last_table = new_table

            # 显示当前时间，并刷新时间显示（不清屏票务信息）
            clear_screen_line()
            display_time()

            # 短暂休眠，保持时间流畅刷新
            time.sleep(SLEEP_INTERVAL)

        except requests.exceptions.RequestException as e:
            print(f"请求错误(可能被风控): {e}")
            break  # 停止循环

if __name__ == "__main__":
    main()
    print("按回车键退出...")
    input()

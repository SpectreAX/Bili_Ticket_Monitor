import requests
import time
from datetime import datetime
from colorama import Fore, Style, init

# 常量
URL = "https://show.bilibili.com/api/ticket/project/getV2?version=134&id=替换这里"  # 请替换为实际票务ID
TIMEOUT = 100  # 请求超时时间
SLEEP_INTERVAL = 0.9  # 时间显示刷新间隔
TICKET_REFRESH_INTERVAL = 2  # 票务信息刷新间隔
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# 初始化颜色输出
init(autoreset=True)

def clear_screen_line():
    # 清除终端当前行的内容
    print("\033[F\033[K", end="")  # 将光标移到上一行并清除该行内容

def fetch_ticket_status(url, headers):
    # 从提供的URL获取票务状态
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        tickets = data.get('data', {}).get('screen_list', [])
        name = data.get('data', {}).get('name', '')

        if not tickets:
            print("票务数据为空，请检查票务ID")
            return None, None

        table = [
            [ticket.get('screen_name', '') + ticket.get('desc', '').replace("普通票", "普通票\t\t"),
             ticket.get('sale_flag', {}).get('display_name', '')]
            for screen in tickets
            for ticket in screen.get('ticket_list', [])
        ]

        return name, table

    except requests.exceptions.RequestException as e:
        print(f"请求错误(可能被风控): {e}")
        return None, None

def print_ticket_table(name, table):
    # 打印票务信息表
    if not table:
        return

    max_desc_len = max(len(row[0]) for row in table)
    max_status_len = max(len(row[1]) for row in table)

    print(f"{Style.BRIGHT}{name}")
    print(f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}{'状态'.ljust(max_status_len)}{Style.RESET_ALL}")
    print('-' * (max_desc_len + max_status_len + 16))  # 延长的分隔线以增强视觉效果

    for row in table:
        desc = Fore.WHITE + row[0].ljust(max_desc_len) + Style.RESET_ALL
        status = row[1]
        status_colored = color_status(status, max_status_len)
        print(f"{desc} {status_colored}")

def color_status(status, max_status_len):
    # 根据销售状态返回对应颜色的状态
    if status in ["已售罄", "已停售"]:
        return Fore.RED + status.ljust(max_status_len) + Style.RESET_ALL
    elif status == "暂时售罄":
        return Fore.YELLOW + status.ljust(max_status_len) + Style.RESET_ALL
    elif status == "预售中":
        return Fore.GREEN + status.ljust(max_status_len) + Style.RESET_ALL
    return status.ljust(max_status_len)  # 默认颜色

def has_table_changed(old_table, new_table):
    # 检查票务表数据是否发生变化
    return old_table != new_table

def display_time():
    # 显示当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}当前时间: {current_time}{Style.RESET_ALL}")

def main():
    # 主程序循环
    last_table = None
    name, new_table = fetch_ticket_status(URL, HEADERS)

    if new_table is None:
        return  # 如果没有票务数据则退出

    print_ticket_table(name, new_table)
    last_table = new_table

    while True:
        try:
            if time.time() % TICKET_REFRESH_INTERVAL < 1:
                name, new_table = fetch_ticket_status(URL, HEADERS)
                if new_table is None:
                    break  # 如果没有新的票务数据则退出

                if has_table_changed(last_table, new_table):
                    print_ticket_table(name, new_table)
                    last_table = new_table

            clear_screen_line()
            display_time()
            time.sleep(SLEEP_INTERVAL)

        except requests.exceptions.RequestException as e:
            print(f"请求错误(可能被风控): {e}")
            break  # 出现错误时停止循环

if __name__ == "__main__":
    main()
    input("按回车键退出...")  # 等待用户输入以退出

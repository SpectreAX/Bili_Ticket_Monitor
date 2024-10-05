import requests
import time
from datetime import datetime
from colorama import Fore, Style, init

# 可以修改的东西
TICKET_ID = "请替换这里"  # 请替换为实际票务ID
TICKET_REFRESH_INTERVAL = 2  # 票务信息刷新间隔，1秒以下可能会被风控
TIMEOUT = 100  # 请求超时时间，根据网络状况设置

# 不要动下面的东西！！！
BASE_URL = "https://show.bilibili.com/api/ticket/project/getV2?version=134&id="
URL = f"{BASE_URL}{TICKET_ID}"  # 拼接完整的URL
SLEEP_INTERVAL = 0.9  # 时间显示刷新间隔
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"}

# 初始化颜色输出
init(autoreset=True)

def clear_screen_line():    # 清除终端当前行的内容
    print("\033[F\033[K", end="")  # 将光标移到上一行并清除该行内容

def fetch_ticket_status(url, headers):    # 从提供的URL获取票务状态
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        tickets = data.get('data', {}).get('screen_list', [])
        name = data.get('data', {}).get('name', '')

        if not tickets:
            print(Fore.RED + "数据为空，请检查票务ID" + Style.RESET_ALL)
            return None, None

        table = [
            [ticket.get('screen_name', '') + ticket.get('desc', '').replace("普通票", "普通票\t\t"),
             ticket.get('sale_flag', {}).get('display_name', '')]
            for screen in tickets
            for ticket in screen.get('ticket_list', [])
        ]

        return name, table

    except requests.exceptions.RequestException as e:   # 检查是否为412错误码
        if e.response and e.response.status_code == 412:
            print(Fore.RED + "IP被风控，请等待一段时间后继续，否则将会引发更大的问题" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"请求错误(请检查网络连接): {e}" + Style.RESET_ALL)
        return None, None

def print_ticket_table(name, table):    # 打印票务信息表
    if not table:
        return

    max_desc_len = max(len(row[0]) for row in table)
    max_status_len = max(len(row[1]) for row in table)

    print(f"{Style.BRIGHT}{name}")
    print(f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}{'状态'.ljust(max_status_len)}{Style.RESET_ALL}")
    print('-' * (max_desc_len + max_status_len + 16))  # 延长的分隔线

    for row in table:
        desc = Fore.WHITE + row[0].ljust(max_desc_len) + Style.RESET_ALL
        status = row[1]
        status_colored = color_status(status, max_status_len)
        print(f"{desc} {status_colored}")

def color_status(status, max_status_len):    # 根据销售状态返回对应颜色的状态
    if status in ["已售罄", "已停售", "不可售", "未开售"]:
        return Fore.RED + status.ljust(max_status_len) + Style.RESET_ALL
    elif status == "暂时售罄":
        return Fore.YELLOW + status.ljust(max_status_len) + Style.RESET_ALL
    elif status == "预售中":
        return Fore.GREEN + status.ljust(max_status_len) + Style.RESET_ALL
    return status.ljust(max_status_len)  # 默认颜色

def has_table_changed(old_table, new_table):    # 检查数据是否发生变化
    return old_table != new_table

def display_time():    # 显示当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}当前时间: {current_time}{Style.RESET_ALL}")

def main():    # 主程序循环
    last_table = None
    name, new_table = fetch_ticket_status(URL, HEADERS)

    if new_table is None:
        return  # 如果没有数据则退出

    print_ticket_table(name, new_table)
    last_table = new_table

    while True:
        try:
            if time.time() % TICKET_REFRESH_INTERVAL < 1:
                name, new_table = fetch_ticket_status(URL, HEADERS)
                if new_table is None:
                    break  # 如果没有新的数据则退出

                if has_table_changed(last_table, new_table):
                    print_ticket_table(name, new_table)
                    last_table = new_table

            clear_screen_line()
            display_time()
            time.sleep(SLEEP_INTERVAL)

        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 412:
                print(Fore.RED + "IP被风控，请等待一段时间后继续，否则将会引发更大的问题" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"请求错误(请检查网络连接): {e}" + Style.RESET_ALL)
            break  # 出现错误时停止循环

if __name__ == "__main__":
    main()
    input("按回车键退出...")  # 等待用户输入以退出

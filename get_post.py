from os import replace
from unittest import result
import psutil
import json
import random
import sys
from builtins import print
import re
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

sys.stdout.reconfigure(encoding="utf-8")
batch_file_path = r"f:\coding\python\seleniumpj\get_community\localhost19.bat"

import subprocess


def close_chrome(port):
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if process.info["name"] == "chrome.exe":
            try:
                cmd_line = process.cmdline()
                if f"--remote-debugging-port={port}" in cmd_line:
                    process.terminate()
                    print(f"Closed Chrome with port {port}")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass


close_chrome(9219)
subprocess.run([batch_file_path], shell=True)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-xss-auditor")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-webgl")
options.add_argument("--disable-popup-blocking")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
options.add_experimental_option("debuggerAddress", "localhost:9219")
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(10)
driver.implicitly_wait(10)
# Bật tính năng mạng.
driver.execute_cdp_cmd("Network.enable", {})
# Vô hiệu hóa bộ nhớ cache của trình duyệt.
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
# Chặn các yêu cầu đến các domain cụ thể
blocked_urls = [
    "https://yt3.googleusercontent.com/*",
    "https://yt3.ggpht.com/*",
    "https://i.ytimg.com/*",
]
driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_urls})
index = 0
while True:
    myobj = {"index": index}
    response = requests.post(
        f"https://server.com/tool/test.php?dsad189fmas92=query_youtube_url", data=myobj
    )
    print("seed")

    json_obj = json.loads(response.text)
    if len(json_obj) != 0:
        for item in json_obj:
            print(f'-------------{item["site_id"]} {item["youtube_url"]}')
            objall = []
            try:
                driver.get(f'{item["youtube_url"]}/community')
                sleep(5)
                count = 0
                scroll = 1
                while True:
                    elements = driver.find_elements(
                        By.TAG_NAME, "ytd-backstage-post-thread-renderer"
                    )
                    new_count = len(elements)

                    # Kiểm tra số lượng thẻ
                    if new_count >= 20:
                        print(f"Đã tìm thấy {new_count} thẻ, dừng cuộn trang.")
                        break
                    else:
                        if scroll > 10:
                            print(f"Không tìm thấy đủ 20 thẻ, dừng cuộn trang.")
                            break
                        print(f"Tìm thấy {new_count} thẻ, tiếp tục cuộn trang...")
                        count = new_count
                        scroll = scroll + 1
                        # Cuộn trang
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                        sleep(2)
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                        sleep(2)
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                        sleep(2)
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                        # Chờ một chút để nội dung mới tải về
                        sleep(2)
                post_thread_elements = driver.find_elements(
                    By.TAG_NAME, "ytd-backstage-post-thread-renderer"
                )
                index = 1
                # Lấy link từ thẻ <a> con của 20 thẻ đầu tiên
                for element in post_thread_elements[:20]:
                    try:
                        # Tìm thẻ <a> bên trong mỗi ytd-backstage-post-thread-renderer
                        link_element = element.find_element(
                            By.CSS_SELECTOR,
                            "#reply-button-end a.yt-spec-button-shape-next",
                        )
                        # Lấy giá trị thuộc tính href
                        link = link_element.get_attribute("href")

                        link = link.replace("https://www.youtube.com/post/", "")
                        last_five_uppercase = link[-8:].upper()
                        data = {
                            "site_id": item["site_id"],
                            "youtube_url": link,
                            "post_url": last_five_uppercase,
                        }
                        objall.append(data)
                        # print(f"Link {index}: {link}")
                        index += 1
                    except:
                        # Nếu không tìm thấy thẻ <a> trong ytd-backstage-post-thread-renderer, in ra thông báo
                        print(f"Link {index}: Không tìm thấy")

            except Exception as e:
                print("loi-la", e)
                sleep(5)
            # sys.exit()
            pust_data = requests.post(
                f"https://studio.kolsup.com/tool/test.php?dsad189fmas92=put_post1",
                json={"data": objall},
            )
            print("seed11")
            # print(objall)
            # print(pust_data.text)
            try:
                result = json.loads(pust_data.text)
                print("status:", result["status"], "-- message:", result["message"])
            except:
                print("text: ", pust_data.text)
    close_chrome(9219)
    # sys.exit()

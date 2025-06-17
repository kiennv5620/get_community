from calendar import c
from os import replace
from turtle import pu, right
from unittest import result
from distro import like
import psutil
import json
import random
import sys
from builtins import print
import re
from datetime import datetime, timedelta
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
batch_file_path = r"f:\coding\python\seleniumpj\get_community\localhost21.bat"

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


def convert_time_to_date(input_text):
    current_date = datetime.now()
    input_text = input_text.replace("(đã chỉnh sửa)", "")
    # Xử lý các trường hợp khác nhau
    if "giờ trước" in input_text:
        hours_ago = int(re.search(r"(\d+) giờ trước", input_text).group(1))
        target_date = current_date - timedelta(hours=hours_ago)
    elif "ngày trước" in input_text:
        days_ago = int(re.search(r"(\d+) ngày trước", input_text).group(1))
        target_date = current_date - timedelta(days=days_ago)
    elif "tuần trước" in input_text:
        weeks_ago = int(re.search(r"(\d+) tuần trước", input_text).group(1))
        target_date = current_date - timedelta(weeks=weeks_ago)
    elif "tháng trước" in input_text:
        months_ago = int(re.search(r"(\d+) tháng trước", input_text).group(1))
        # Đối với tháng, ta sẽ giả sử mỗi tháng có 30 ngày
        target_date = current_date - timedelta(days=(30 * months_ago))
    elif "năm trước" in input_text:
        years_ago = int(re.search(r"(\d+) năm trước", input_text).group(1))
        # Đối với năm, ta sẽ giả sử mỗi năm có 365 ngày
        target_date = current_date - timedelta(days=(365 * years_ago))
    else:
        return "Không thể xác định định dạng thời gian"

    return target_date.strftime("%Y-%m-%d")


def convert_likes_to_number(likes_str):
    mapping = {
        "K": 1000,
        "N": 1000,
        "Tr": 1000000,
        "M": 1000000,
        "T": 1000000000,
        "B": 1000000000,
    }

    # Loại bỏ khoảng trắng thừa và thay thế dấu phẩy bằng dấu chấm
    likes_str = likes_str.strip().replace(",", ".")

    for unit in mapping.keys():
        if likes_str.endswith(unit):
            number_part = likes_str[: -len(unit)]
            try:
                return int(float(number_part) * mapping[unit])
            except ValueError as e:
                print(f"Lỗi khi chuyển đổi số: {e}")
                return None

    try:
        return int(float(likes_str))
    except ValueError as e:
        print(f"Lỗi khi chuyển đổi số: {e}")
        return None


close_chrome(9221)
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
options.add_experimental_option("debuggerAddress", "localhost:9221")
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(10)
driver.implicitly_wait(10)
index = 0
while True:
    myobj = {"index": index}
    response = requests.post(
        f"https://server/tool/test.php?dsad189fmas92=query_youtube_url2", data=myobj
    )
    print("seed")
    json_obj = json.loads(response.text)
    if len(json_obj) != 0:
        for item in json_obj:
            print(f'-------------{item["id"]} {item["youtube_url"]}')
            objall = []
            try:
                driver.get(f'https://www.youtube.com/post/{item["youtube_url"]}')
                # driver.get(
                #     f'https://www.youtube.com/channel/UCYa6aqgfGlHXSMMZS3c3C-g/community?lb=Ugkx5W2THTqs8J0ojEzx__63EA1FXd0seMp_')
                sleep(5)

                published_time_text = driver.find_element(
                    By.CSS_SELECTOR, "#published-time-text"
                ).text
                published_time = convert_time_to_date(published_time_text)
                # print(published_time)

                content_text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#content-text"))
                )
                script = """
var images = document.querySelectorAll('img.small-emoji');
images.forEach(function(img) {
    var altText = img.alt; // Lấy giá trị alt của thẻ img
    var span = document.createElement('span'); // Tạo thẻ span mới
    span.className = 'emoji'; // Thêm class 'emoji' vào thẻ span
    span.textContent = altText; // Đặt nội dung của span là giá trị alt
    img.parentNode.replaceChild(span, img); // Thay thế thẻ img bằng thẻ span
});
"""
                driver.execute_script(script)
                # Thực thi JavaScript để xóa tất cả class trong các thẻ con và lấy
                html_content = driver.execute_script(
                    """
    var content = arguments[0];
    var elements = content.getElementsByTagName('*');
    for (var i = 0; i < elements.length; i++) {
        elements[i].className = 'text-content'; 
        if(elements[i].tagName.toLowerCase() === 'a') { // Nếu là thẻ a
            var href = elements[i].getAttribute('href');
            if(href && !href.includes('https://youtu.be')) {
                elements[i].setAttribute('href', 'https://www.youtube.com' + href);
            }
        }
    }
    return content.innerHTML;
""",
                    content_text,
                )

                # print(html_content)

                # print(content_text)
                content_attachments = []
                type_of_attachment = None
                first_child_of_first_attachment = driver.find_element(
                    By.XPATH, "//*[@id='content-attachment']/*[1]"
                )
                first_child_tag_name = first_child_of_first_attachment.tag_name
                if first_child_tag_name == "ytd-backstage-image-renderer":
                    image_url = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "img"
                    ).get_attribute("src")
                    content_attachments = [image_url]
                    type_of_attachment = 1
                elif first_child_tag_name == "ytd-video-renderer":
                    video_url = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "a"
                    ).get_attribute("href")
                    video_image = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "img"
                    ).get_attribute("src")
                    video_title = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "#video-title"
                    ).text
                    video_chanel_name = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "#channel-name"
                    ).text
                    video_chanel_href = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "#channel-name a"
                    ).get_attribute("href")
                    video_desc = first_child_of_first_attachment.find_element(
                        By.CSS_SELECTOR, "#description-text"
                    ).text
                    content_attachments = [
                        video_url,
                        video_image,
                        video_title,
                        video_chanel_name,
                        video_chanel_href,
                        video_desc,
                    ]
                    type_of_attachment = 2
                elif first_child_tag_name == "ytd-post-multi-image-renderer":
                    element = driver.find_element(By.ID, "right-arrow")
                    driver.execute_script(
                        "arguments[0].click();arguments[0].click();", element
                    )
                    sleep(2)
                    image_elements = first_child_of_first_attachment.find_elements(
                        By.CSS_SELECTOR, "img"
                    )
                    content_attachments = []
                    type_of_attachment = 3
                    for image_element in image_elements:
                        image_url = image_element.get_attribute("src")
                        content_attachments.append(image_url)
                else:
                    print("Không xác định được loại attachment")
                    pust_data = requests.post(
                        f"https://server/tool/test.php?dsad189fmas92=put_post2",
                        json={"data": {"id": item["id"], "status": "no_attachment"}},
                    )
                    print("seed11")
                    print(pust_data.text)
                # print(content_attachments)
                # continue
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                sleep(2)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                # Lấy thông tin về số lượt thích và số lượt bình luận
                like_count = driver.find_element(
                    By.CSS_SELECTOR, "#vote-count-middle"
                ).text
                like_count = convert_likes_to_number(like_count)
                if like_count is None or like_count == "":
                    like_count = 0
                # print(like_count)
                comment_count = driver.find_element(
                    By.CSS_SELECTOR, "#count > yt-formatted-string > span:nth-child(1)"
                ).text
                if comment_count == "" or comment_count == None:
                    comment_count = 0
                # print(comment_count)
                # Lấy danh sách 5 comment đầu tiên gồm nội dung và tên người bình luận ảnh người bình luận ngày đăng và like
                comment_elements = driver.find_elements(
                    By.CSS_SELECTOR, "ytd-comment-renderer#comment"
                )
                comments = []
                for comment_element in comment_elements[:5]:
                    comment_text = comment_element.find_element(
                        By.CSS_SELECTOR, "#comment #content-text"
                    ).text
                    commenter_name = comment_element.find_element(
                        By.CSS_SELECTOR, "#author-text"
                    ).text
                    commenter_image = comment_element.find_element(
                        By.CSS_SELECTOR, "#author-thumbnail img"
                    ).get_attribute("src")
                    comment_date = convert_time_to_date(
                        comment_element.find_element(
                            By.CSS_SELECTOR, ".published-time-text"
                        ).text
                    )
                    comment_likes = convert_likes_to_number(
                        comment_element.find_element(
                            By.CSS_SELECTOR, "#vote-count-middle"
                        ).text
                    )
                    if comment_likes is None:
                        comment_likes = 0
                    comments.append(
                        {
                            "comment_text": comment_text,
                            "commenter_name": commenter_name,
                            "commenter_image": commenter_image,
                            "comment_date": comment_date,
                            "comment_likes": comment_likes,
                        }
                    )
                print(comments)

                objall = {
                    "id": item["id"],
                    "site_id": item["site_id"],
                    "published_time": published_time,
                    "content_text": html_content,
                    "content_attachments": content_attachments,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "type_of_attachment": type_of_attachment,
                }
                print(objall)
                pust_data = requests.post(
                    f"https://server/tool/test.php?dsad189fmas92=put_post2",
                    json={"data": objall, "comments": comments},
                )
                print("seed11")
                print(pust_data.text)
                # driver.quit()
                # close_chrome(9221)
                # sleep(2)
                # subprocess.run([batch_file_path], shell=True)
                # sleep(2)
                # driver = webdriver.Chrome(service=Service(
                # ChromeDriverManager().install()), options=options)
                # driver.set_page_load_timeout(15)
                # driver.implicitly_wait(15)
                # sys.exit()
            except Exception as e:
                print(e)
                print("Không xác định được loại attachment")
                pust_data = requests.post(
                    f"https://server/tool/test.php?dsad189fmas92=put_post2",
                    json={"data": {"id": item["id"], "status": "no_attachment"}},
                )
                print("seed11")
                print(pust_data.text)

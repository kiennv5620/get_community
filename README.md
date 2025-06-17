# get_community

## Description

This project automates the process of collecting YouTube Community post data and comments using Selenium WebDriver and Chrome. The collected data is sent to a server via internal API endpoints.

## Main Files

- **get_post.py**: Crawls YouTube channels to collect community post links and sends them to the server.
- **get_detail_post.py**: Fetches detailed information for each post (content, attachments, like count, comment count, top 5 comments, etc.) and sends it to the server.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (automatically installed via `webdriver_manager`)
- Required Python packages: selenium, requests, psutil, webdriver_manager

Install dependencies:

```sh
pip install selenium requests psutil webdriver_manager
```

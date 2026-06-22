import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib3
import json
import re
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clean_text(text):
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_meta_content(soup, attrs_list):
    for attrs in attrs_list:
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return clean_text(tag.get("content"))
    return ""


def crawl_website(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    result = {
        "success": False,
        "url": url,
        "domain": "",
        "https": url.startswith("https://"),
        "title": "抓取失敗",
        "description": "",
        "og_title": "",
        "og_description": "",
        "author": "",
        "publish_time": "",
        "content": "",
        "error": ""
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=12,
            allow_redirects=True,
            verify=False
        )

        final_url = response.url
        result["url"] = final_url
        result["domain"] = urlparse(final_url).netloc.lower()
        result["https"] = final_url.startswith("https://")

        if response.status_code >= 400:
            result["error"] = f"HTTP 狀態碼：{response.status_code}"
            return result

        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")

        result["og_title"] = get_meta_content(soup, [
            {"property": "og:title"},
            {"name": "og:title"},
            {"name": "twitter:title"}
        ])

        if result["og_title"]:
            result["title"] = result["og_title"]
        elif soup.title:
            result["title"] = clean_text(soup.title.get_text())

        result["description"] = get_meta_content(soup, [
            {"name": "description"},
            {"property": "og:description"},
            {"name": "twitter:description"}
        ])

        result["og_description"] = get_meta_content(soup, [
            {"property": "og:description"},
            {"name": "og:description"}
        ])

        result["author"] = get_meta_content(soup, [
            {"name": "author"},
            {"property": "article:author"},
            {"name": "parsely-author"},
            {"name": "byl"},
            {"name": "dc.creator"},
            {"name": "creator"},
            {"property": "og:site_name"}
        ])

        result["publish_time"] = get_meta_content(soup, [
            {"property": "article:published_time"},
            {"property": "article:modified_time"},
            {"name": "article:published_time"},
            {"name": "pubdate"},
            {"name": "publishdate"},
            {"name": "date"},
            {"name": "datePublished"},
            {"itemprop": "datePublished"},
            {"name": "parsely-pub-date"},
            {"property": "og:updated_time"},
            {"name": "dc.date"},
            {"name": "DC.date.issued"}
        ])

        # JSON-LD 補抓作者與日期
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                if not script.string:
                    continue

                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]

                for item in items:
                    if not isinstance(item, dict):
                        continue

                    if not result["author"]:
                        author = item.get("author")

                        if isinstance(author, dict):
                            result["author"] = clean_text(author.get("name", ""))

                        elif isinstance(author, list) and author:
                            if isinstance(author[0], dict):
                                result["author"] = clean_text(author[0].get("name", ""))

                    if not result["publish_time"]:
                        result["publish_time"] = clean_text(
                            item.get("datePublished", "")
                            or item.get("dateModified", "")
                        )

            except Exception:
                pass

        text_all = soup.get_text(" ", strip=True)

        if not result["author"] and "bbc." in result["domain"]:
            if "sport" in result["url"]:
                result["author"] = "BBC Sport"
            else:
                result["author"] = "BBC News"

        # 從頁面文字抓真正作者，會覆蓋 Yahoo News
        author_patterns = [
            r"【記者\s*([^／\s]{2,8})\s*／",
            r"記者\s*([^\s/／]{2,8})\s*[／/]",
            r"作者[:：]?\s*([^\s，。]{2,12})",
            r"([^\s]{2,8})\s*[／/]\s*綜合報導",
            r"([^\s]{2,8})\s*[／/]\s*報導"
        ]

        for pattern in author_patterns:
            match = re.search(pattern, text_all)
            if match:
                result["author"] = clean_text(match.group(1))
                break

        # 頁面文字備援：抓中文日期
        if not result["publish_time"]:
            match = re.search(
                r"\d{4}年\d{1,2}月\d{1,2}日\s*週.\s*(上午|下午)?\d{1,2}:\d{2}",
                text_all
            )
            if match:
                result["publish_time"] = match.group(0)

        # 日期格式化：UTC 轉台灣時間
        if result["publish_time"]:
            try:
                dt = datetime.fromisoformat(
                    result["publish_time"].replace("Z", "+00:00")
                )
                dt = dt + timedelta(hours=8)
                result["publish_time"] = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass

        for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
            tag.decompose()

        content_list = []

        selectors = [
            "article",
            "[role='article']",
            ".article",
            ".article-content",
            ".article_body",
            ".articleBody",
            ".story-body",
            ".story-content",
            ".post-content",
            ".entry-content",
            ".caas-body",
            ".caas-content",
            "#articleBody",
            "#story-body"
        ]

        for selector in selectors:
            blocks = soup.select(selector)

            for block in blocks:
                for p in block.find_all(["p", "h2", "h3", "li"]):
                    text = clean_text(p.get_text(" ", strip=True))
                    if len(text) >= 20:
                        content_list.append(text)

            if len(" ".join(content_list)) > 600:
                break

        if not content_list:
            paragraphs = soup.find_all(["p", "h2", "h3", "li"])
            for p in paragraphs:
                text = clean_text(p.get_text(" ", strip=True))
                if len(text) >= 20:
                    content_list.append(text)

        content = "\n".join(dict.fromkeys(content_list))

        if not content:
            content = result["description"] or result["og_description"]

        result["content"] = content[:5000]

        if result["title"] != "抓取失敗" or result["description"] or result["content"]:
            result["success"] = True

        return result

    except Exception as e:
        result["error"] = str(e)
        print("Crawler Error:", e)
        return result
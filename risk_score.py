def calculate_score(website):
    reasons = []

    domain = website.get("domain", "").lower()
    content = website.get("content", "")
    length = len(content)

    trusted_news = [
        "tw.sports.yahoo.com", "yahoo.com",
        "cna.com.tw", "udn.com", "ltn.com.tw",
        "ettoday.net", "tvbs.com.tw", "setn.com",
        "storm.mg", "bbc.com", "reuters.com",
        "apnews.com", "cnn.com", "nytimes.com",
        "theguardian.com", "bloomberg.com"
    ]

    website_type = "一般網站"

    https_score = 10 if website.get("https") else 0
    title_score = 10 if website.get("title") else 0
    desc_score = 10 if website.get("description") else 0
    og_score = 5 if website.get("og_title") or website.get("og_description") else 0
    author_score = 10 if website.get("author") else 0
    publish_score = 10 if website.get("publish_time") else 0

    if length >= 2500:
        content_score = 15
    elif length >= 1200:
        content_score = 12
    elif length >= 500:
        content_score = 8
    else:
        content_score = 4

    if "gov" in domain:
        domain_score = 30
        website_type = "政府網站"
    elif "edu" in domain:
        domain_score = 28
        website_type = "教育網站"
    elif "who.int" in domain or "nature.com" in domain or "science.org" in domain:
        domain_score = 30
        website_type = "學術 / 專業機構"
    elif any(d in domain for d in trusted_news):
        domain_score = 30
        website_type = "新聞媒體"
    elif "ptt" in domain or "dcard" in domain or "reddit" in domain:
        domain_score = 12
        website_type = "論壇 / 討論平台"
    elif "facebook" in domain or "instagram" in domain or "threads" in domain:
        domain_score = 8
        website_type = "社群平台"
    else:
        domain_score = 10
        website_type = "一般網站"

    detail = {
        "https": https_score,
        "title": title_score,
        "description": desc_score,
        "og": og_score,
        "author": author_score,
        "publish": publish_score,
        "content": content_score,
        "domain": domain_score
    }

    score = sum(detail.values())
    score = min(score, 100)

    if https_score:
        reasons.append("✓ 使用 HTTPS 加密連線")
    else:
        reasons.append("⚠ 未使用 HTTPS")

    if title_score:
        reasons.append("✓ 成功取得網頁標題")
    else:
        reasons.append("⚠ 未取得網頁標題")

    if desc_score:
        reasons.append("✓ 網頁具有 Description")
    else:
        reasons.append("⚠ 未取得 Description")

    if og_score:
        reasons.append("✓ 有 Open Graph 資訊")
    else:
        reasons.append("⚠ 未取得 Open Graph 資訊")

    if author_score:
        reasons.append("✓ 有作者資訊")
    else:
        reasons.append("⚠ 未取得作者資訊")

    if publish_score:
        reasons.append("✓ 有發布日期")
    else:
        reasons.append("⚠ 未取得發布日期")

    if content_score >= 12:
        reasons.append("✓ 文章內容完整")
    elif content_score >= 8:
        reasons.append("✓ 有基本文章內容")
    else:
        reasons.append("⚠ 文章內容較少")

    reasons.append(f"✓ 網站類型：{website_type}")

    if score >= 85:
        risk = "低風險"
    elif score >= 65:
        risk = "中風險"
    else:
        risk = "高風險"

    return {
        "score": score,
        "risk": risk,
        "reasons": reasons,
        "detail": detail,
        "website_type": website_type,
        "content_length": length
    }
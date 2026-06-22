def simple_ai_analysis(content, score=None, website=None):
    original_content = content or ""
    content_lower = original_content.lower()

    website = website or {}
    score = score or {}

    credibility = score.get("score", 0)
    website_type = score.get("website_type", "一般網站")
    content_length = score.get("content_length", len(original_content))
    domain = website.get("domain", "").lower()

    # ==========================
    # 關鍵字設定
    # ==========================

    warning_words = [
        "震驚", "驚爆", "一定", "絕對", "保證", "唯一",
        "馬上", "立刻", "爆料", "驚人", "必看", "快分享",
        "shocking", "breaking", "urgent", "must", "guaranteed"
    ]

    emotion_words = [
        "可怕", "恐怖", "憤怒", "荒謬", "崩潰", "震怒",
        "慘", "痛批", "災難", "terrible", "angry", "outrage", "disaster"
    ]

    evidence_words = [
        "官方", "政府", "研究", "數據", "統計", "報告",
        "來源", "指出", "表示", "根據", "調查",
        "source", "data", "report", "research", "according to"
    ]

    diversity_words = [
        "不同觀點", "反方", "另一方", "多元", "但是", "不過",
        "然而", "相對", "另一方面",
        "however", "although", "but", "on the other hand"
    ]

    authority_words = [
        "專家表示", "研究指出", "官方表示", "醫師指出",
        "expert", "official", "research", "according to"
    ]

    group_words = [
        "大家都", "網友都", "多數人", "所有人",
        "everyone", "most people", "netizens"
    ]

    trusted_sources = [
        "Reuters", "BBC", "CNN", "AP", "中央社",
        "教育部", "衛福部", "WHO", "NASA",
        "政府", "法院", "立法院", "行政院",
        "FIFA", "官方"
    ]

    data_words = [
        "%", "％", "百分比", "人數", "人口", "統計",
        "調查", "數據", "報告", "研究", "萬人",
        "億元", "美元", "data", "statistics", "survey"
    ]

    # ==========================
    # 偵測結果
    # ==========================

    warning_hits = [w for w in warning_words if w in content_lower]
    emotion_hits = [w for w in emotion_words if w in content_lower]
    evidence_hits = [w for w in evidence_words if w in content_lower]
    diversity_hits = [w for w in diversity_words if w in content_lower]

    found_sources = []
    for s in trusted_sources:
        if s.lower() in content_lower:
            found_sources.append(s)

    data_hits = []
    for d in data_words:
        if d.lower() in content_lower:
            data_hits.append(d)

    source_count = len(evidence_hits)
    trusted_source_count = len(found_sources)

    # ==========================
    # 來源類型分析
    # ==========================

    if ".gov" in domain or "gov." in domain:
        source_type = "政府網站"
        source_level = "★★★★★"
    elif ".edu" in domain or "edu." in domain:
        source_type = "教育機構"
        source_level = "★★★★★"
    elif any(x in domain for x in [
        "bbc", "reuters", "cnn", "nytimes", "udn",
        "ltn", "ettoday", "cna", "tvbs", "yahoo",
        "apnews", "bloomberg"
    ]):
        source_type = "新聞媒體"
        source_level = "★★★★☆"
    elif "ptt" in domain or "dcard" in domain or "reddit" in domain:
        source_type = "論壇 / 討論平台"
        source_level = "★★☆☆☆"
    elif "facebook" in domain or "instagram" in domain or "threads" in domain:
        source_type = "社群平台"
        source_level = "★☆☆☆☆"
    else:
        source_type = "一般網站"
        source_level = "★★★☆☆"

    # ==========================
    # 語氣 / 點擊誘餌 / 情緒
    # ==========================

    if len(warning_hits) >= 3:
        tone = "高度煽動"
    elif warning_hits:
        tone = "可能具有誇大語氣"
    elif emotion_hits:
        tone = "略帶情緒性"
    else:
        tone = "語氣相對中立"

    clickbait_score = min(len(warning_hits) * 20, 100)
    emotion_score = min(len(emotion_hits) * 15, 100)

    # ==========================
    # 假新聞風險
    # 分數越高 = 風險越高
    # ==========================

    fake_news_score = 45

    if credibility >= 85:
        fake_news_score -= 25
    elif credibility >= 65:
        fake_news_score -= 12
    else:
        fake_news_score += 15

    if website.get("author"):
        fake_news_score -= 8
    else:
        fake_news_score += 10

    if website.get("publish_time"):
        fake_news_score -= 8
    else:
        fake_news_score += 10

    if found_sources:
        fake_news_score -= 10
    elif evidence_hits:
        fake_news_score -= 5
    else:
        fake_news_score += 10

    if warning_hits:
        fake_news_score += 12

    if emotion_hits:
        fake_news_score += 8

    if content_length < 500:
        fake_news_score += 15

    if source_type in ["政府網站", "教育機構", "新聞媒體"]:
        fake_news_score -= 10

    fake_news_score = max(0, min(fake_news_score, 100))

    if fake_news_score >= 70:
        fake_news_level = "高風險"
    elif fake_news_score >= 40:
        fake_news_level = "中風險"
    else:
        fake_news_level = "低風險"

    # ==========================
    # 資訊泡泡分析
    # 分數越高 = 泡泡風險越高
    # ==========================

    bubble_score = 35
    bubble_reasons = []

    if evidence_hits:
        bubble_score -= 8
        bubble_reasons.append("內容包含來源、數據或引用線索")
    else:
        bubble_score += 12
        bubble_reasons.append("引用來源較少，建議交叉查證")

    if diversity_hits:
        bubble_score -= 10
        bubble_reasons.append("內容可能包含不同觀點或補充說明")
    else:
        bubble_score += 12
        bubble_reasons.append("未明顯偵測到不同觀點或反方說明")

    if found_sources:
        bubble_score -= 8
        bubble_reasons.append("內容偵測到可信來源或官方線索")

    if content_length < 500:
        bubble_score += 15
        bubble_reasons.append("可分析內容較少，資訊來源可能不足")

    if source_type in ["政府網站", "教育機構", "新聞媒體"]:
        bubble_score -= 8
        bubble_reasons.append("來源類型具一定公信力，泡泡風險降低")

    bubble_score = max(5, min(bubble_score, 100))

    # ==========================
    # 認知偏誤分析
    # 分數越高 = 偏誤越高
    # ==========================

    bias_score = 10
    bias_list = []

    if warning_hits:
        bias_score += 20
        bias_list.append("確認偏誤或誇大表述")

    if emotion_hits:
        bias_score += 20
        bias_list.append("情緒偏誤")

    if any(w in content_lower for w in authority_words):
        bias_score += 10
        bias_list.append("權威偏誤")

    if any(w in content_lower for w in group_words):
        bias_score += 15
        bias_list.append("從眾偏誤")

    if tone == "語氣相對中立":
        bias_score -= 5

    if source_type in ["政府網站", "教育機構", "新聞媒體"]:
        bias_score -= 5

    bias_score = max(5, min(bias_score, 100))

    # ==========================
    # 多元觀點分析
    # 分數越高 = 越多元
    # ==========================

    diversity_score = 35
    diversity_reasons = []

    if evidence_hits:
        diversity_score += 20
        diversity_reasons.append("內容包含來源、數據、報告或引用資訊")

    if diversity_hits:
        diversity_score += 25
        diversity_reasons.append("內容可能包含不同觀點或補充說明")

    if found_sources:
        diversity_score += 15
        diversity_reasons.append("內容偵測到可信來源")

    if content_length > 1500:
        diversity_score += 10
        diversity_reasons.append("文章內容較完整，可分析資訊較多")

    if source_type in ["政府網站", "教育機構", "新聞媒體"]:
        diversity_score += 10
        diversity_reasons.append("來源類型具一定公信力")

    diversity_score = max(0, min(diversity_score, 100))

    if not diversity_reasons:
        diversity_reasons.append("未明顯偵測到多元來源或不同觀點")

    # ==========================
    # 交叉引用程度
    # ==========================

    cross_reference_score = min((source_count + trusted_source_count) * 20, 100)

    if cross_reference_score >= 80:
        cross_reference_level = "★★★★★"
    elif cross_reference_score >= 60:
        cross_reference_level = "★★★★☆"
    elif cross_reference_score >= 40:
        cross_reference_level = "★★★☆☆"
    elif cross_reference_score >= 20:
        cross_reference_level = "★★☆☆☆"
    else:
        cross_reference_level = "★☆☆☆☆"

    # ==========================
    # AI 資訊健康度
    # ==========================

    health_score = int(
        credibility * 0.35 +
        diversity_score * 0.25 +
        (100 - bubble_score) * 0.15 +
        (100 - bias_score) * 0.15 +
        (100 - fake_news_score) * 0.10
    )

    health_score = max(0, min(health_score, 100))

    # ==========================
    # AI 建議
    # ==========================

    suggestions = []

    if credibility >= 85:
        suggestions.append("網站可信度高，可作為參考來源。")
    elif credibility >= 65:
        suggestions.append("網站可信度中等，建議搭配其他來源查證。")
    else:
        suggestions.append("網站可信度偏低，建議提高警覺。")

    if fake_news_score >= 40:
        suggestions.append("偵測到假訊息風險，建議查詢官方或第二來源。")
    else:
        suggestions.append("假訊息風險較低，但仍建議保持交叉查證習慣。")

    if bubble_score >= 50:
        suggestions.append("資訊泡泡風險偏高，建議閱讀不同立場的資料。")

    if bias_score >= 40:
        suggestions.append("偵測到部分認知偏誤線索，閱讀時應注意語氣與立場。")

    if clickbait_score >= 40:
        suggestions.append("標題可能具有點擊誘餌特徵，建議不要只看標題判斷。")

    if not found_sources:
        suggestions.append("未明顯偵測到可信來源引用，建議補充官方或權威資料。")

    if not data_hits:
        suggestions.append("未明顯偵測到數據或統計資料，可再補充量化資訊佐證。")

    # ==========================
    # AI 摘要
    # ==========================

    if health_score >= 85:
        summary = (
            f"本文來自 {domain}，來源類型為「{source_type}」。"
            "整體資訊健康度高，網站可信度良好，假訊息與認知偏誤風險較低。"
            "可作為參考來源，但仍建議搭配其他來源查證。"
        )
    elif health_score >= 65:
        summary = (
            f"本文來自 {domain}，來源類型為「{source_type}」。"
            "整體資訊健康度中等，內容具一定可信度。"
            "建議補充官方資料、其他媒體或不同觀點進行比對。"
        )
    else:
        summary = (
            f"本文來自 {domain}，來源類型為「{source_type}」。"
            "整體資訊健康度偏低，可能存在來源不足、觀點單一或偏誤風險。"
            "建議不要只依賴單一文章。"
        )

    return {
        "tone": tone,
        "credibility": credibility,
        "summary": summary,
        "warning_words": warning_hits,

        "bubble_score": bubble_score,
        "bubble_reasons": bubble_reasons,

        "bias_score": bias_score,
        "bias_list": bias_list,

        "diversity_score": diversity_score,
        "diversity_reasons": diversity_reasons,

        "health_score": health_score,
        "suggestions": suggestions,

        "fake_news_score": fake_news_score,
        "fake_news_level": fake_news_level,

        "emotion_score": emotion_score,
        "clickbait_score": clickbait_score,
        "source_count": source_count,
        "emotion_words": emotion_hits,

        "source_type": source_type,
        "source_level": source_level,
        "trusted_sources": found_sources,
        "trusted_source_count": trusted_source_count,
        "data_hits": data_hits,
        "data_count": len(data_hits),
        "cross_reference_score": cross_reference_score,
        "cross_reference_level": cross_reference_level
    }
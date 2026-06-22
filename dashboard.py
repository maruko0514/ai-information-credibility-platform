import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


STATIC_DIR = "static"


def generate_dashboard_charts(stats):
    os.makedirs(STATIC_DIR, exist_ok=True)

    # ==========================
    # 1. 風險比例圖
    # ==========================

    labels = ["Low Risk", "Medium Risk", "High Risk"]
    values = [
        stats.get("low", 0),
        stats.get("middle", 0),
        stats.get("high", 0)
    ]

    if sum(values) == 0:
        values = [1, 0, 0]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Risk Level Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "risk_chart.png"))
    plt.close()

    # ==========================
    # 2. 平均分數比較圖
    # ==========================

    score_labels = [
        "Credibility",
        "Health",
        "Fake Risk",
        "Bubble",
        "Bias",
        "Clickbait",
        "Emotion",
        "Cross Ref"
    ]

    score_values = [
        stats.get("avg_score", 0),
        stats.get("avg_health", 0),
        stats.get("avg_fake", 0),
        stats.get("avg_bubble", 0),
        stats.get("avg_bias", 0),
        stats.get("avg_clickbait", 0),
        stats.get("avg_emotion", 0),
        stats.get("avg_cross", 0)
    ]

    plt.figure(figsize=(10, 5))
    plt.bar(score_labels, score_values)
    plt.ylim(0, 100)
    plt.ylabel("Score")
    plt.title("Average AI Analysis Scores")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "score_chart.png"))
    plt.close()

    # ==========================
    # 3. 來源類型分布圖
    # ==========================

    source_types = stats.get("source_types", [])

    source_labels = []
    source_values = []

    for row in source_types:
        source_labels.append(row["source_type"] or "Unknown")
        source_values.append(row["count"])

    if not source_values:
        source_labels = ["No Data"]
        source_values = [1]

    plt.figure(figsize=(7, 5))
    plt.bar(source_labels, source_values)
    plt.title("Source Type Distribution")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "source_chart.png"))
    plt.close()

    # ==========================
    # 4. Top 10 網站排行
    # ==========================

    top_domains = stats.get("top_domains", [])

    domain_labels = []
    domain_values = []

    for row in top_domains:
        domain_labels.append(row["domain"] or "Unknown")
        domain_values.append(row["count"])

    if not domain_values:
        domain_labels = ["No Data"]
        domain_values = [1]

    plt.figure(figsize=(9, 5))
    plt.barh(domain_labels, domain_values)
    plt.title("Top Domains")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "domain_chart.png"))
    plt.close()

    # ==========================
    # 5. 最近 7 天分析量
    # ==========================

    daily_counts = stats.get("daily_counts", [])

    day_labels = []
    day_values = []

    for row in reversed(daily_counts):
        day_labels.append(row["date"] or "Unknown")
        day_values.append(row["count"])

    if not day_values:
        day_labels = ["No Data"]
        day_values = [0]

    plt.figure(figsize=(8, 5))
    plt.plot(day_labels, day_values, marker="o")
    plt.title("Daily Analysis Count")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "daily_chart.png"))
    plt.close()
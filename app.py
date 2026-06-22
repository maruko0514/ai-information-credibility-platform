from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from dashboard import generate_dashboard_charts
from crawler import crawl_website
from risk_score import calculate_score
from ai_analyzer import simple_ai_analysis
from database import (
    init_db,
    save_analysis,
    get_all_history,
    get_dashboard_stats
)

load_dotenv(override=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:
            return render_template(
                "analyze.html",
                error="請輸入網址"
            )

        website = crawl_website(url)

        if not website.get("success"):
            return render_template(
                "result.html",
                website=website,
                score={
                    "score": 0,
                    "risk": "抓取失敗",
                    "reasons": [
                        website.get("error", "無法取得網站內容，請確認網址是否正確。")
                    ]
                },
                ai={
                    "tone": "無法分析",
                    "credibility": 0,
                    "summary": "因網站內容抓取失敗，系統無法進行可信度、資訊泡泡與認知偏誤分析。",
                    "warning_words": [],
                    "bubble_score": 0,
                    "bubble_reasons": ["無法取得文章內容"],
                    "bias_score": 0,
                    "bias_list": [],
                    "diversity_score": 0,
                    "diversity_reasons": ["無法取得文章內容"],
                    "health_score": 0,
                    "suggestions": ["請確認網址是否正確，或改用其他可公開瀏覽的新聞網址。"]
                }
            )

        score = calculate_score(website)

        ai = simple_ai_analysis(
            website.get("content", ""),
            score,
            website
        )

        save_analysis(website, score, ai)

        return render_template(
            "result.html",
            website=website,
            score=score,
            ai=ai
        )

    return render_template("analyze.html")


@app.route("/history")
def history():

    histories = get_all_history()

    return render_template(
        "history.html",
        histories=histories
    )


@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    generate_dashboard_charts(stats)

    return render_template(
        "dashboard.html",
        stats=stats
    )


@app.route("/about")
def about():

    return render_template("about.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5002)),
        debug=True
    )
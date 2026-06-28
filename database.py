import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise ValueError("找不到 DATABASE_URL，請先設定 Render PostgreSQL 的 DATABASE_URL")

    def get_connection():
      if not DATABASE_URL:
        raise ValueError("找不到 DATABASE_URL")

    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=30,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5,
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id SERIAL PRIMARY KEY,
            url TEXT,
            domain TEXT,
            title TEXT,
            description TEXT,
            author TEXT,
            publish_time TEXT,
            source_type TEXT,
            credibility_score INTEGER,
            health_score INTEGER,
            fake_news_score INTEGER,
            bubble_score INTEGER,
            bias_score INTEGER,
            diversity_score INTEGER,
            clickbait_score INTEGER,
            emotion_score INTEGER,
            cross_reference_score INTEGER,
            trusted_source_count INTEGER,
            data_count INTEGER,
            risk TEXT,
            created_at TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_analysis(website, score, ai):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO analysis_history (
            url,
            domain,
            title,
            description,
            author,
            publish_time,
            source_type,
            credibility_score,
            health_score,
            fake_news_score,
            bubble_score,
            bias_score,
            diversity_score,
            clickbait_score,
            emotion_score,
            cross_reference_score,
            trusted_source_count,
            data_count,
            risk,
            created_at
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """, (
        website.get("url", ""),
        website.get("domain", ""),
        website.get("title", ""),
        website.get("description", ""),
        website.get("author", ""),
        website.get("publish_time", ""),
        ai.get("source_type", ""),
        score.get("score", 0),
        ai.get("health_score", 0),
        ai.get("fake_news_score", 0),
        ai.get("bubble_score", 0),
        ai.get("bias_score", 0),
        ai.get("diversity_score", 0),
        ai.get("clickbait_score", 0),
        ai.get("emotion_score", 0),
        ai.get("cross_reference_score", 0),
        ai.get("trusted_source_count", 0),
        ai.get("data_count", 0),
        score.get("risk", ""),
        datetime.now(ZoneInfo("Asia/Taipei"))
    ))

    conn.commit()
    cur.close()
    conn.close()


def get_all_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *,
        created_at + INTERVAL '8 hours' AS created_at
        FROM analysis_history
        ORDER BY id DESC
     """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    def avg(column):
        cur.execute(f"SELECT AVG({column}) AS value FROM analysis_history")
        row = cur.fetchone()
        return round(row["value"] or 0, 1)

    cur.execute("SELECT COUNT(*) AS total FROM analysis_history")
    total = cur.fetchone()["total"] or 0

    avg_score = avg("credibility_score")
    avg_health = avg("health_score")
    avg_fake = avg("fake_news_score")
    avg_bubble = avg("bubble_score")
    avg_bias = avg("bias_score")
    avg_diversity = avg("diversity_score")
    avg_clickbait = avg("clickbait_score")
    avg_emotion = avg("emotion_score")
    avg_cross = avg("cross_reference_score")
    avg_trusted_sources = avg("trusted_source_count")
    avg_data_count = avg("data_count")

    cur.execute("SELECT COUNT(*) AS count FROM analysis_history WHERE risk = '低風險'")
    low = cur.fetchone()["count"] or 0

    cur.execute("SELECT COUNT(*) AS count FROM analysis_history WHERE risk = '中風險'")
    middle = cur.fetchone()["count"] or 0

    cur.execute("SELECT COUNT(*) AS count FROM analysis_history WHERE risk = '高風險'")
    high = cur.fetchone()["count"] or 0

    cur.execute("""
        SELECT source_type, COUNT(*) AS count
        FROM analysis_history
        GROUP BY source_type
        ORDER BY count DESC
    """)
    source_types = cur.fetchall()

    cur.execute("""
        SELECT domain, COUNT(*) AS count
        FROM analysis_history
        GROUP BY domain
        ORDER BY count DESC
        LIMIT 10
    """)
    top_domains = cur.fetchall()

    cur.execute("""
        SELECT DATE(created_at) AS date, COUNT(*) AS count
        FROM analysis_history
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    """)
    daily_counts = cur.fetchall()

    cur.execute("""
        SELECT *,
        created_at + INTERVAL '8 hours' AS created_at
        FROM analysis_history
        ORDER BY id DESC
        LIMIT 5
    """)
    recent = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "total": total,
        "avg_score": avg_score,
        "avg_health": avg_health,
        "avg_fake": avg_fake,
        "avg_bubble": avg_bubble,
        "avg_bias": avg_bias,
        "avg_diversity": avg_diversity,
        "avg_clickbait": avg_clickbait,
        "avg_emotion": avg_emotion,
        "avg_cross": avg_cross,
        "avg_trusted_sources": avg_trusted_sources,
        "avg_data_count": avg_data_count,
        "low": low,
        "middle": middle,
        "high": high,
        "source_types": source_types,
        "top_domains": top_domains,
        "daily_counts": daily_counts,
        "recent": recent
    }
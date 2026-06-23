# AI 網路資訊可信度與風險分析平台
## AI-Based Information Credibility and Risk Analysis Platform

> 結合人工智慧、網頁爬蟲、資料分析與 PostgreSQL 雲端資料庫之資訊可信度分析系統

---

# 專案簡介

本專題以 Python Flask 為核心，結合網頁爬蟲、人工智慧分析、資料分析及 PostgreSQL 雲端資料庫，建立一套 **AI 網路資訊可信度與風險分析平台**。

系統可自動擷取新聞網站內容，分析資訊可信度、資訊健康度、假新聞風險、資訊泡泡、認知偏誤、點擊誘餌及多元觀點等指標，並將分析結果儲存至 PostgreSQL，提供 Dashboard 統計分析及歷史查詢功能，協助使用者快速判斷網路資訊品質，提高媒體識讀能力。

---

# 研究背景

近年來，網路資訊傳播速度極快，各種新聞、自媒體及社群平台每日產生大量資訊。然而，假新聞、誤導性內容、點擊誘餌（Clickbait）、資訊泡泡及認知偏誤等問題，也逐漸影響民眾判斷資訊真實性的能力。

許多使用者缺乏快速辨識資訊可信度的方法，因此希望透過人工智慧與資料分析技術，建立一套客觀的資訊可信度分析平台，提供使用者更可靠的判斷依據。

---

# 研究動機

目前大部分新聞網站僅提供新聞內容，缺乏資訊可信度分析。

因此，本專題希望建立一套 AI 網路資訊可信度分析平台，透過網頁爬蟲、自動分析及資料分析模型，提供網站可信度評估、假新聞風險分析及資訊品質評估，降低錯誤資訊造成的影響。

---

# 研究目的

本系統希望完成以下目標：

- 建立 AI 網路資訊可信度分析平台
- 自動擷取網站內容
- 分析網站可信度
- 分析資訊健康度
- 分析假新聞風險
- 分析資訊泡泡
- 分析認知偏誤
- 分析點擊誘餌
- 分析多元觀點
- 建立 PostgreSQL 歷史資料庫
- 提供 Dashboard 統計分析
- 提供歷史分析紀錄

本專題不僅著重於程式設計與系統開發，更希望透過人工智慧、網頁爬蟲及資料分析技術，協助使用者快速判斷網路資訊可信度，提升媒體識讀能力，降低假新聞與錯誤資訊對社會造成的影響，展現資訊科技結合人文關懷的應用價值。

---

# 系統特色

- AI 網站可信度分析
- AI 資訊健康度分析
- AI 假新聞風險分析
- 點擊誘餌分析（Clickbait）
- 情緒分析
- 資訊泡泡分析
- 認知偏誤分析
- 多元觀點分析
- 網頁內容自動擷取
- Dashboard 統計分析
- 歷史分析紀錄
- PostgreSQL 雲端資料庫
- Render 雲端部署

---

# 系統架構

```
使用者
      │
      ▼
Flask Web
      │
      ▼
Web Crawler
      │
      ▼
AI Analyzer
      │
 ┌────┼───────────────┐
 ▼    ▼               ▼
可信度  假新聞風險   偏誤分析
      │
      ▼
PostgreSQL Database
      │
      ▼
Dashboard / History
```

---

# 系統流程

```
輸入網址
      │
      ▼
網頁爬蟲
      │
      ▼
擷取網站資訊
      │
      ▼
AI分析
      │
      ▼
可信度評分
      │
      ▼
存入 PostgreSQL
      │
      ▼
Dashboard
      │
      ▼
History
```

---

# 使用技術

| 技術 | 用途 |
|------|------|
| Python | 程式開發 |
| Flask | Web Framework |
| Requests | 網頁請求 |
| BeautifulSoup4 | HTML解析 |
| PostgreSQL | 雲端資料庫 |
| HTML5 | 前端設計 |
| CSS3 | 網頁樣式 |
| JavaScript | 前端互動 |
| Docker | 容器化部署 |
| Render | 雲端部署 |
| GitHub | 版本控制 |

---

# AI 分析項目

本系統分析內容包括：

- Website Credibility（網站可信度）
- Information Health（資訊健康度）
- Fake News Risk（假新聞風險）
- Bubble Score（資訊泡泡）
- Bias Score（認知偏誤）
- Diversity Score（多元觀點）
- Clickbait Score（點擊誘餌）
- Emotion Score（情緒分析）
- Cross Reference Score（交叉引用分析）

系統依據各項分析結果建立加權評分模型（Weighted Scoring Model），提供整體可信度評估。

---

# 資料庫設計

本系統使用 Render PostgreSQL。

主要資料表：

```
analysis_history
```

主要欄位：

- URL
- 網站名稱
- 標題
- 作者
- 發布日期
- 網站可信度
- 資訊健康度
- 假新聞風險
- 資訊泡泡
- 認知偏誤
- 多元觀點
- 點擊誘餌
- 情緒分析
- 分析時間

---

# 專案架構

```
AI-Information-Credibility-Platform

│

├── app.py
├── crawler.py
├── ai_analyzer.py
├── risk_score.py
├── dashboard.py
├── database.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── templates
│   ├── home.html
│   ├── result.html
│   ├── history.html
│   └── dashboard.html
│
└── static
    ├── css
    ├── js
    └── images
```

---

# 安裝方式

## 1. 安裝套件

```bash
pip install -r requirements.txt
```

## 2. 建立環境變數

建立 `.env`

```
DATABASE_URL=Your PostgreSQL Database URL
SECRET_KEY=your_secret_key
```

## 3. 啟動系統

```bash
python app.py
```

## 4. 開啟瀏覽器

```
http://127.0.0.1:5002
```

---

# Render 部署

本專題部署於 Render。

使用：

- Flask Web Service
- PostgreSQL Database
- Docker

Environment Variables：

```
DATABASE_URL
SECRET_KEY
```

---

# GitHub

本專案使用 GitHub 進行版本控制，方便團隊協作、版本管理及後續維護。

---

# 創新特色

- 結合 AI 與網路資訊可信度分析
- 動態網頁爬蟲自動擷取資訊
- 建立多項可信度評分模型
- PostgreSQL 雲端資料庫
- Dashboard 視覺化分析
- 歷史分析紀錄
- Render 雲端部署
- 可擴充大型語言模型（LLM）

---

# 未來發展

未來可持續擴充以下功能：

- Google Fact Check API
- AI 自動摘要
- 多語言新聞分析
- PDF 分析報告
- 使用者登入系統
- 個人收藏功能
- 即時新聞監控
- 行動裝置 App
- LLM 深度分析

---

# 專題成果

本專題完成：

- Flask 網站建置
- GitHub 版本控制
- Render PostgreSQL 雲端資料庫
- Render 雲端部署
- 動態網頁爬蟲
- AI 網路資訊分析
- Dashboard 統計分析
- History 歷史紀錄
- Docker 容器化

---

# 作者

**魏瑋彤**

輔仁大學  
數學資訊組

程式設計期末專題

2026

---

# License

This project is for educational purposes only.
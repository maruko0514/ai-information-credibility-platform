document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const loading = document.getElementById("loading");
    const text = document.getElementById("loading-text");
    const bar = document.getElementById("loading-progress");

    if (!form || !loading || !text || !bar) {
        return;
    }

    const steps = [
        "🌐 正在連線網站...",
        "📄 正在擷取網站內容...",
        "🛡 正在分析網站可信度...",
        "🫧 正在分析資訊泡泡...",
        "🧠 正在分析認知偏誤...",
        "📊 正在計算資訊健康度...",
        "🤖 AI 正在產生分析報告..."
    ];

    form.addEventListener("submit", function () {
        loading.style.display = "flex";

        let index = 0;
        text.innerHTML = steps[index];
        bar.style.width = "10%";

        setInterval(function () {
            index++;

            if (index >= steps.length) {
                index = steps.length - 1;
            }

            text.innerHTML = steps[index];
            bar.style.width = ((index + 1) / steps.length * 100) + "%";
        }, 700);
    });
});
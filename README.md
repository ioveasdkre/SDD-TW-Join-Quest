《 臺灣規格驅動開發研究組織 (SDD.TW) 》是一場由《水球軟體學院》發起的技術研究社群，目標是集結全台具備軟體開發能力的工程師，共同推進 AI × SDD/BDD 開發流程的研究與實踐。
「如果大家都關注 AI x SDD/BDD 這件事，台灣軟工進度就有機會超前國外；
當國外 AI 軟工都只會寫 rules 時，我們就已經全部都在寫 spec，產值絕對爆增。」

## 運行測試

本專案使用 `uv` 進行 Python 套件管理。運行以下命令來執行 BDD 測試（包括整合的單元測試）：

```bash
# 執行所有 BDD 功能測試（會先執行 pytest 單元測試）
uv run python -m behave --no-capture

# 或指定特定的功能檔案
uv run python -m behave features/order/order.feature --no-capture

# 僅執行單元測試
uv run python -m pytest -v
```

### 測試結果

- **BDD 情境**：31 個情境全部通過 (象棋: 22 個 ✅, 訂單: 9 個 ✅)
- **步驟定義**：103 個步驟全部通過 (象棋: 66 個 ✅, 訂單: 37 個 ✅)
- **功能檔案**：2 個功能檔案 (chess.feature, order.feature)
- **成功率**：100% ✅

## 生成測試報告

本專案支持生成美觀的 HTML 測試報告。報告數據將存儲在 `reports/` 目錄中，保持根目錄整潔。

### 快速開始

```bash
# 1. 生成 JSON 格式的測試數據
uv run python -m behave features/chess/chess.feature --format=json --outfile=reports/chess_report.json
uv run python -m behave features/order/order.feature --format=json --outfile=reports/order_report.json

# 2. 生成 HTML 報告和總覽儀表板
uv run python generate_reports.py
```

### 報告結構

```
reports/
├── index.html              ← 📋 總覽儀表板（主入口）
├── chess_report.html       ← ♟️ 象棋詳細報告
├── order_report.html       ← 📦 訂單系統詳細報告
├── chess_report.json       ← 象棋測試數據（原始）
└── order_report.json       ← 訂單系統測試數據（原始）
```

### 查看報告

#### 方式 1：使用瀏覽器

1. 在瀏覽器中打開 `reports/index.html`
2. 點擊各 Feature 卡片可查看詳細報告
3. 報告支持點擊展開/收起 Scenario 詳情

#### 方式 2：用檔案管理器

1. 導航至 `reports/` 目錄
2. 雙擊 `index.html` 即可在預設瀏覽器中打開

### 報告內容

**總覽儀表板** (`index.html`)：

- 全專案統計（總場景數、通過率、步驟數）
- 各 Feature 卡片摘要
- 快速鏈接至詳細報告

**詳細報告** (例：`chess_report.html`)：

- Feature 名稱與描述
- Scenario 清單及執行狀態（✓ 通過/✗ 失敗）
- 每個 Scenario 的完整 Step 定義
- 執行耗時統計
- 返回總覽按鈕

### 報告特性

✅ **視覺化設計**

- 漸層背景與卡片式佈局
- 綠色（✓ 通過）和紅色（✗ 失敗）狀態指示
- 進度條顯示通過比例

✅ **互動功能**

- 點擊 Feature 區塊展開/收起 Scenario
- 可點擊的報告卡片跳轉詳細內容
- 返回按鈕便捷導航

✅ **詳細資訊**

- 每個步驟的執行耗時（毫秒）
- Scenario 成功率百分比
- 報告生成時間戳記

✅ **便於分享**

- 整個 `reports/` 目錄可獨立分享給他人
- 無需依賴任何服務器或工具
- 任何瀏覽器都能打開

### 報告示例

| Feature | Scenarios | Steps    | 成功率 |
| ------- | --------- | -------- | ------ |
| ♟️ 象棋 | 22/22 ✅  | 66/66 ✅ | 100%   |
| 📦 訂單 | 9/9 ✅    | 37/37 ✅ | 100%   |

### 本組織將專注於以下目標

1. 本組織相信 AI x SDD/BDD 的方法，一定能讓 AI 在背景就產出 80%~90% 可靠且正確的程式，而這一定是未來 Vibe Coding 的趨勢，你一定是想要追求最前沿的軟工技術才加入本組織。
2. 組織規劃好了初步研究藍圖，分為底下三大路線
   a. 開發流程全自動化（後端）— Feature file (BDD) 到 API Spec/ERD 到程式
   b. 開發流程全自動化（前端）— 線框 到 User-flow (BDD) 到程式
   c. 回饋流程智能化 (全端) — 前後端整合自動化建立新的驗收測試
   這三者只要都研究完成，那 Vibe Coding 才算是成熟，軟體工程師能與與 AI 「平行」合作帶來百倍產出，故稱「AI 百倍軟工研究組織」。

### 歡迎所有人參與

你的參與，不僅代表你願意走在 AI 軟體開發方法論的最前線，更代表你願意投身於一場嚴謹、務實、強調產出價值與技術驗證的研究歷程（所有的研究紀錄都會使用 Github Repository 保存脈絡）。
報名方法：

1. 加入水球軟體學院 Discord：https://discord.gg/uWGTF7RSnW
2. 照著此 Discord 社群內 #加入研究計劃 置頂訊息的指示進行即可成功報名
   若你已準備好成為推動 AI × SDD/BDD 開發方法的革新者，誠摯邀請你完成報名，與來自全台的技術夥伴攜手共創。

#!/usr/bin/env python3
"""Generate HTML reports from Behave JSON output"""

import json
from datetime import datetime
from pathlib import Path


def generate_html_report(json_file: str, output_file: str, feature_name: str = None):
    """Convert Behave JSON output to HTML report"""

    # Read JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print(f"⚠️ No data found in {json_file}")
        return None

    # Calculate statistics
    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0

    for feature in data:
        for scenario in feature.get("elements", []):
            total_scenarios += 1
            scenario_passed = True

            for step in scenario.get("steps", []):
                total_steps += 1
                if step["result"]["status"] == "passed":
                    passed_steps += 1
                else:
                    failed_steps += 1
                    scenario_passed = False

            if scenario_passed:
                passed_scenarios += 1
            else:
                failed_scenarios += 1

    # Get feature name from data if not provided
    if not feature_name and data:
        feature_name = data[0].get("name", "Test Report")

    pass_percentage = (
        (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
    )

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{feature_name} - BDD 測試報告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .back-link {{
            display: inline-block;
            margin-top: 15px;
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-size: 0.95em;
            padding: 8px 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            transition: background 0.3s;
        }}
        
        .back-link:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
        }}
        
        .summary-card.passed {{
            border-left-color: #28a745;
        }}
        
        .summary-card.failed {{
            border-left-color: #dc3545;
        }}
        
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .summary-card.passed .value {{
            color: #28a745;
        }}
        
        .summary-card.failed .value {{
            color: #dc3545;
        }}
        
        .features {{
            padding: 30px;
        }}
        
        .feature {{
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .feature-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .feature-header h2 {{
            font-size: 1.3em;
        }}
        
        .scenarios {{
            background: white;
            display: none;
        }}
        
        .scenarios.show {{
            display: block;
        }}
        
        .scenario {{
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
        }}
        
        .scenario-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .scenario-status {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.8em;
        }}
        
        .scenario-status.passed {{
            background: #28a745;
        }}
        
        .scenario-status.failed {{
            background: #dc3545;
        }}
        
        .scenario-name {{
            flex: 1;
            font-weight: 500;
            color: #333;
        }}
        
        .scenario-time {{
            color: #999;
            font-size: 0.9em;
        }}
        
        .steps {{
            margin-top: 10px;
            padding-left: 40px;
        }}
        
        .step {{
            padding: 5px 0;
            color: #666;
            font-size: 0.95em;
            border-left: 2px solid transparent;
            padding-left: 10px;
        }}
        
        .step.passed {{
            color: #28a745;
            border-left-color: #28a745;
        }}
        
        .step.failed {{
            color: #dc3545;
            border-left-color: #dc3545;
        }}
        
        .step-keyword {{
            font-weight: bold;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}
        
        .progress-bar {{
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        }}
    </style>
    <script>
        function toggleFeature(element) {{
            const scenarios = element.nextElementSibling;
            scenarios.classList.toggle('show');
        }}
    </script>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>{feature_name}</h1>
            <p>BDD Test Report</p>
            <a href="index.html" class="back-link">← 返回總覽</a>
        </div>
        
        <!-- Summary -->
        <div class="summary">
            <div class="summary-card passed">
                <h3>通過的場景</h3>
                <div class="value">{passed_scenarios}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_percentage:.1f}%"></div>
                </div>
            </div>
            <div class="summary-card failed">
                <h3>失敗的場景</h3>
                <div class="value">{failed_scenarios}</div>
            </div>
            <div class="summary-card passed">
                <h3>通過的步驟</h3>
                <div class="value">{passed_steps}</div>
            </div>
            <div class="summary-card">
                <h3>總場景數</h3>
                <div class="value">{total_scenarios}</div>
            </div>
        </div>
        
        <!-- Features -->
        <div class="features">
"""

    # Add features and scenarios
    for feature in data:
        feature_name_in_data = feature.get("name", "Unknown Feature")
        feature_passed = all(
            all(
                step["result"]["status"] == "passed"
                for step in scenario.get("steps", [])
            )
            for scenario in feature.get("elements", [])
        )

        html_content += f"""            <div class="feature">
                <div class="feature-header" onclick="toggleFeature(this)">
                    <h2>{feature_name_in_data}</h2>
                    <span>{"✓ 通過" if feature_passed else "✗ 失敗"}</span>
                </div>
                <div class="scenarios show">
"""

        for scenario in feature.get("elements", []):
            scenario_name = scenario.get("name", "Unknown Scenario")
            scenario_passed = all(
                step["result"]["status"] == "passed"
                for step in scenario.get("steps", [])
            )
            scenario_duration = sum(
                step["result"].get("duration", 0) for step in scenario.get("steps", [])
            )

            html_content += f"""                    <div class="scenario">
                        <div class="scenario-header">
                            <div class="scenario-status {"passed" if scenario_passed else "failed"}">
                                {"✓" if scenario_passed else "✗"}
                            </div>
                            <div class="scenario-name">{scenario_name}</div>
                            <div class="scenario-time">{scenario_duration / 1e9:.3f}s</div>
                        </div>
                        <div class="steps">
"""

            for step in scenario.get("steps", []):
                step_keyword = step.get("keyword", "").strip()
                step_name = step.get("name", "")
                step_status = step["result"]["status"]
                step_time = step["result"].get("duration", 0) / 1e9

                html_content += f"""                            <div class="step {step_status}">
                                <span class="step-keyword">{step_keyword}</span> {step_name}
                                <span style="color: #999; font-size: 0.85em;"> ({step_time:.3f}s)</span>
                            </div>
"""

            html_content += """                        </div>
                    </div>
"""

        html_content += """                </div>
            </div>
"""

    # Footer
    html_content += f"""        </div>
        
        <div class="footer">
            <p>
                報告生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
                總計：{total_scenarios} 個場景，{passed_scenarios} 個通過，{failed_scenarios} 個失敗 | 步驟：{total_steps} 個，{passed_steps} 個通過，{failed_steps} 個失敗
            </p>
        </div>
    </div>
</body>
</html>
"""

    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Write HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 報告已生成：{output_file}")
    return {
        "total_scenarios": total_scenarios,
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "total_steps": total_steps,
        "passed_steps": passed_steps,
        "failed_steps": failed_steps,
    }


def generate_index_report(reports_data: list):
    """Generate index/dashboard report"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_all_scenarios = sum(r["total_scenarios"] for r in reports_data)
    passed_all_scenarios = sum(r["passed_scenarios"] for r in reports_data)
    total_all_steps = sum(r["total_steps"] for r in reports_data)
    passed_all_steps = sum(r["passed_steps"] for r in reports_data)

    pass_percentage = (
        (passed_all_scenarios / total_all_scenarios * 100)
        if total_all_scenarios > 0
        else 0
    )

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDD 測試報告 - 總覽</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
        }}
        
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .summary-card.passed {{
            border-left-color: #28a745;
        }}
        
        .summary-card.passed .value {{
            color: #28a745;
        }}
        
        .reports {{
            padding: 30px;
        }}
        
        .report-card {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }}
        
        .report-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .report-card a {{
            text-decoration: none;
            color: inherit;
        }}
        
        .report-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .report-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-value.passed {{
            color: #28a745;
        }}
        
        .report-link {{
            display: inline-block;
            padding: 8px 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.9em;
            transition: opacity 0.3s;
        }}
        
        .report-link:hover {{
            opacity: 0.9;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}
        
        .progress-bar {{
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🚀 BDD 測試報告總覽</h1>
            <p>Behavior Driven Development Test Dashboard</p>
        </div>
        
        <!-- Overall Summary -->
        <div class="summary">
            <div class="summary-card passed">
                <h3>總通過場景</h3>
                <div class="value">{passed_all_scenarios}/{total_all_scenarios}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_percentage:.1f}%"></div>
                </div>
            </div>
            <div class="summary-card">
                <h3>總場景數</h3>
                <div class="value">{total_all_scenarios}</div>
            </div>
            <div class="summary-card passed">
                <h3>總通過步驟</h3>
                <div class="value">{passed_all_steps}/{total_all_steps}</div>
            </div>
            <div class="summary-card">
                <h3>成功率</h3>
                <div class="value">{pass_percentage:.1f}%</div>
            </div>
        </div>
        
        <!-- Individual Reports -->
        <div class="reports">
            <h2 style="margin-bottom: 20px; color: #333;">詳細報告</h2>
"""

    for report in reports_data:
        percentage = (
            (report["passed_scenarios"] / report["total_scenarios"] * 100)
            if report["total_scenarios"] > 0
            else 0
        )

        html_content += f"""            <div class="report-card">
                <a href="{report["file"]}">
                    <div class="report-title">{report["name"]}</div>
                    <div class="report-stats">
                        <div class="stat">
                            <div class="stat-label">場景</div>
                            <div class="stat-value passed">{report["passed_scenarios"]}/{report["total_scenarios"]}</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">步驟</div>
                            <div class="stat-value">{report["passed_steps"]}/{report["total_steps"]}</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">成功率</div>
                            <div class="stat-value" style="color: {("#28a745" if percentage == 100 else "#667eea")}">{percentage:.1f}%</div>
                        </div>
                    </div>
                    <a href="{report["file"]}" class="report-link">查看詳細報告 →</a>
                </a>
            </div>
"""

    html_content += f"""        </div>
        
        <div class="footer">
            <p>
                報告生成時間：{timestamp}<br>
                共 {len(reports_data)} 個 Feature，{total_all_scenarios} 個場景，{passed_all_scenarios} 個通過
            </p>
        </div>
    </div>
</body>
</html>
"""

    # Write index file
    Path("reports").mkdir(parents=True, exist_ok=True)
    with open("reports/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ 索引報告已生成：reports/index.html")


if __name__ == "__main__":
    reports = []

    # Generate chess report
    print("📊 生成象棋報告...")
    chess_stats = generate_html_report(
        "reports/chess_report.json",
        "reports/chess_report.html",
        "♟️ 象棋 (Chinese Chess)",
    )
    if chess_stats:
        reports.append(
            {
                "name": "♟️ 象棋 (Chinese Chess)",
                "file": "chess_report.html",
                **chess_stats,
            }
        )

    # Generate order report
    print("📊 生成訂單報告...")
    order_stats = generate_html_report(
        "reports/order_report.json",
        "reports/order_report.html",
        "📦 訂單系統 (Order System)",
    )
    if order_stats:
        reports.append(
            {
                "name": "📦 訂單系統 (Order System)",
                "file": "order_report.html",
                **order_stats,
            }
        )

    # Generate index
    if reports:
        print("📋 生成總覽報告...")
        generate_index_report(reports)
        print("\n✅ 所有報告已生成在 reports/ 目錄中")
        print("📂 報告位置：reports/index.html")
    else:
        print("❌ 沒有找到任何報告數據")

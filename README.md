# ScrapeMap - 中国电厂信息爬虫工具
ScrapeMap是一个基于**Python**的网页爬虫类，用于从**OpenInfraMap**网站爬取中国地区不同能源类型的电厂信息，包括[电厂名称]、[英文名]、[运营商]、[发电功]率等。支持按**能源类型**（如煤电、风电、燃气、生物质能)分类抓取，输出为结构化的**Pandas DataFrame**，便于进一步分析与保存。

## 🧩 功能特性
- 支持能源类型筛选（coal、wind、gas、biomass etc.）
- 自动请求网页、解析 HTML、提取电厂基本信息
- 数据结构清晰，可导出为 xlsx, csv 等格式
- 简洁可扩展的类封装，便于维护和复用

## 📦 安装依赖
使用以下命令安装所需库：
```bash
pip install requests beautifulsoup4 pandas
```

## 🧠 使用说明
示例：
```python
from ScrapeMap import crawler
if __name__ == '__main__':
    data = crawler(source="wind")
    print(data.head())
```

## 🧑‍💻 交流与讨论
有任何疑问或意见建议欢迎随时联系<a href="mailto:wjingrong1119@163.com" target="_blank">wjingrong1119@163.com</a>

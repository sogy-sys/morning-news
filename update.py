"""毎朝実行: 各社のRSSから見出しとリンクを集めて news.json を出力(AI・APIキー不要)"""
import json, datetime
import feedparser

# ★ RSSのURLは各社の提供状況で変わります。取得に失敗した社はスキップされます。
FEEDS = {
    "NHK": "https://www.nhk.or.jp/rss/news/cat0.xml",
    "朝日新聞": "https://www.asahi.com/rss/asahi/newsheadlines.rdf",
    "毎日新聞": "https://mainichi.jp/rss/etc/mainichi-flash.rss",
    "読売新聞": "https://www.yomiuri.co.jp/rss/",  # 要確認
    "日本経済新聞": "https://assets.wor.jp/rss/rdf/nikkei/news.rdf",  # 要確認
}
PER_FEED = 10

items = []
for src, url in FEEDS.items():
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:PER_FEED]:
            items.append({"source": src, "title": e.get("title", ""),
                          "summary": "", "category": "", "link": e.get("link", "")})
        print(src, "OK", len(feed.entries))
    except Exception as ex:
        print(src, "SKIP", ex)

jst = datetime.timezone(datetime.timedelta(hours=9))
json.dump({"date": datetime.datetime.now(jst).strftime("%Y年%m月%d日"), "lead": "", "items": items},
          open("news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done", len(items))

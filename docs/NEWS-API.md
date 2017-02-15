> [Home](README.md) > News API
---

# News API

### **get_news(feed, max_news_items)**

#### **Parameters**
	-  `feed`: News feed - can be one of ("main_news", "cssd", "news_chronicle", "news_alerts"). Default is "main_news"
	-  `max_news_items`: Maximum number of news items. Default is 10.

#### **Returns**:
Returns a list of dictionaries with parameters 'title' and 'url' of each news article from each news feed category.
News fetched from `feed`.
Maximum length specified by `max_news_items`.


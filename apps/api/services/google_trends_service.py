from pytrends.request import TrendReq
import pandas as pd
from typing import List, Dict

class GoogleTrendsService:
    def __init__(self, hl='en-US', tz=330): # Default to IST timezone as per example
        self.pytrends = TrendReq(hl=hl, tz=tz)

    def get_trend_data_for_keyword(self, keyword: str, timeframe: str = 'today 12-m', geo: str = '') -> Dict:
        try:
            if not keyword:
                return {"keyword": keyword, "average_score": 0, "related_queries": []}

            # Interest over time
            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
            interest = self.pytrends.interest_over_time()
            
            if interest.empty or (interest[keyword] == 0).all():
                trend_score = 0
            else:
                trend_score = interest[keyword].mean()

            # Related queries
            related_queries_df = self.pytrends.related_queries().get(keyword, {}).get('top', pd.DataFrame())
            top_related_queries = related_queries_df['query'].tolist()[:3] if not related_queries_df.empty else []
            
            return {
                "keyword": keyword,
                "average_score": trend_score,
                "related_queries": top_related_queries
            }
        except Exception as e:
            print(f"Error fetching trend data for {keyword}: {e}")
            return {"keyword": keyword, "average_score": 0, "related_queries": []}

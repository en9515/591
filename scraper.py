import requests
import pandas as pd
import time
import random

def fetch_591_data(region=1, section=0):
    """
    region: 1 為台北市, 3 為新北市 (根據 591 代碼)
    """
    url = "https://rent.591.com.tw/home/search/rsList"
    
    # 模擬真實瀏覽器的 Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Device': 'pc'
    }
    
    # 591 必要的 Cookie 初始化 (先拿 Session)
    session = requests.Session()
    session.get("https://rent.591.com.tw/", headers=headers)
    
    params = {
        'is_format_data': '1',
        'is_new_list': '1',
        'type': '1',
        'region': region,
        'section': section,
        'firstRow': 0  # 起始筆數
    }

    all_data = []
    
    # 範例：抓取前 3 頁 (共 90 筆)
    for i in range(3):
        params['firstRow'] = i * 30
        print(f"正在抓取第 {i+1} 頁...")
        
        response = session.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', {}).get('data', [])
            all_data.extend(data)
        else:
            print(f"請求失敗: {response.status_code}")
            break
            
        time.sleep(random.uniform(2, 5)) # 隨機延遲，避免被封 IP
        
    return pd.DataFrame(all_data)
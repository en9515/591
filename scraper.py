import requests
import pandas as pd
import time
import random

def fetch_591_data(region=1):
    url = "https://rent.591.com.tw/home/search/rsList"
    
    # 1. 建立 Session 並先訪問首頁獲取 CSRF Token 與 Cookie
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    print("正在獲取 CSRF Token...")
    home_res = session.get("https://rent.591.com.tw/", headers=headers)
    
    # 從首頁的 Meta Tag 裡抓取 CSRF Token
    csrf_token = ""
    if 'csrf-token' in home_res.text:
        csrf_token = home_res.text.split('csrf-token" content="')[1].split('"')[0]
    
    # 2. 更新 Headers 包含必要的驗證資訊
    headers.update({
        'X-CSRF-TOKEN': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
        'Device': 'pc'
    })

    all_data = []
    # 抓取前 2 頁測試
    for i in range(2):
        params = {
            'is_format_data': '1',
            'is_new_list': '1',
            'type': '1',
            'region': region,
            'firstRow': i * 30
        }
        
        print(f"正在抓取第 {i+1} 頁...")
        res = session.get(url, headers=headers, params=params)
        
        if res.status_code == 200:
            data = res.json().get('data', {}).get('data', [])
            all_data.extend(data)
            print(f"成功抓取 {len(data)} 筆資料")
        else:
            print(f"請求失敗: {res.status_code}")
            # 如果還是 419，印出回應內容確認原因
            if res.status_code == 419:
                print("CSRF 驗證依賴失敗，請稍後再試或檢查 Header")
            break
            
        time.sleep(random.uniform(3, 6)) # 稍微拉長間隔，模擬真人行為
        
    return pd.DataFrame(all_data)

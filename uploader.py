import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

def sync_to_sheets(df, sheet_name):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # 從 GitHub Secrets 讀取 JSON 字串
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        if not creds_json:
            raise ValueError("找不到 GOOGLE_CREDENTIALS 環境變數")
            
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # 打開試算表並更新第一個分頁
        sh = client.open(sheet_name)
        worksheet = sh.get_worksheet(0)
        
        # 轉換 DataFrame 為 list 並寫入
        df = df.fillna('') # 處理空值
        data = [df.columns.values.tolist()] + df.values.tolist()
        
        worksheet.clear()
        worksheet.update(data)
        print("✅ Google Sheets 更新成功！")
        
    except Exception as e:
        print(f"❌ 上傳失敗: {e}")
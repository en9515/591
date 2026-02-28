from scraper import fetch_591_data
from uploader import sync_to_sheets

def main():
    print("🚀 開始執行 591 爬蟲任務...")
    
    # 1. 抓取資料 (預設抓台北市)
    df = fetch_591_data(region=1)
    
    if not df.empty:
        # 2. 同步至 Google Sheets (請確保試算表名稱正確)
        # 建議試算表名稱：591_Market_Data
        sync_to_sheets(df, "591_Market_Data")
    else:
        print("⚠️ 未抓取到任何資料。")

if __name__ == "__main__":
    main()
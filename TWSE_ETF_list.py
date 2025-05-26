import json
import urllib.request as req
import pandas as pd

# 下載資料
url = "https://www.twse.com.tw/zh/ETFortune/ajaxProductsResult"
with req.urlopen(url) as f:
    content = f.read()
# print(type(content))

# 解析 JSON
content_convert = json.loads(content)
# print(type(content_convert))
data = content_convert["data"]
print(content_convert["data"])

# 顯示第一筆資料，幫助理解欄位順序
print("前一筆資料欄位內容：")
for i, value in enumerate(data[0]):
    print(f"{i}: {value}")

# 根據實際觀察調整欄位索引
extracted_data = []
for row in data:
    stock_no = row.get("stockNo", "")
    stock_name = row.get("stockName", "")
    listing_date = row.get("listingDate", "")
    index_name = row.get("indexName", "")
    total_av = row.get("totalAv", "")
    extracted_data.append([stock_no, stock_name, listing_date, index_name, total_av])

# 建立 DataFrame 並儲存為 CSV
df_selected = pd.DataFrame(extracted_data, columns=["stockNo", "stockName", "listingDate", "indexName", "totalAv"])
df_selected.to_csv("TWSE_ETF_list.csv", index=False, encoding="utf-8")
print("✅ TWSE_ETF_list.csv 已建立")

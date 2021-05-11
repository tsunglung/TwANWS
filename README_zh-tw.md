<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

航空氣象服務網 觀測資料 [TwANWS](https://aoaws.anws.gov.tw/AWS/index.php) 支援 Home Assistant


這個整合是基於 MetOffice 所做的開發。

# 安裝

你可以用 [HACS](https://hacs.xyz/) 來安裝這個整合。 步驟如下 custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/TwANWS` > Category: Integration

或是手動複製 `aoaws_anws` 資料夾到你的 config 資料夾的  `custom_components` 目錄下。

然後重新啟動 Home Assistant.

# 設定

**請使用 Home Assistant 整合設定**


1. 從 GUI. 設定 > 整合 > 新增 整合 > Taiwan Navigation Weather Services (NWS)
   1. 如果 TwANWS 沒有出現在清單裡，請 重新整理 (REFRESH) 網頁。
   2. 如果 TwANWS 還是沒有出現在清單裡，請清除瀏覽器的快取 (Cache)。
2. 選擇機場名稱。
3. 選擇語言。


打賞

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/TwANWS/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
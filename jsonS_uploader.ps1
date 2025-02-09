# تنظیمات اولیه
$ElasticURL = "https://localhost:9200/faces/_doc"  # URL ایندکس الاستیک
$Username = "elastic"
$Password = "kx-p2DRTGyi-H*+M1dKM"
$ContentType = "application/json"
$CurlPath = "C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\curl-8.11.1_3-win64-mingw\bin\curl.exe"

# مسیر دایرکتوری شامل پوشه‌های افراد
$BaseDirectory = "C:\Users\mmras\OneDrive\Desktop\facial regognation Elastic\people_JSONs_train-test\train"

# پردازش هر دایرکتوری (نام افراد)
Get-ChildItem -Path $BaseDirectory -Directory | ForEach-Object {
    $PersonName = $_.Name  # نام دایرکتوری = نام شخص
    $PersonPath = $_.FullName

    # پردازش هر فایل JSON در دایرکتوری شخص
    Get-ChildItem -Path $PersonPath -Filter "*.json" | ForEach-Object {
        $JsonFile = $_.FullName  # مسیر فایل JSON
        Write-Host "-------->>> Sending file: $JsonFile for $PersonName"

        # ارسال درخواست به Elasticsearch
        & $CurlPath -k -u "$Username`:$Password" -X POST "$ElasticURL" -H "Content-Type: $ContentType" --data-binary "@$JsonFile"
    }
}

Write-Host "---------------------------------------------
>>>>>>>>>>>>>All files have been uploaded successfully!"

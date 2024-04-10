# DA_Project

## 如何執行試題1

1. 首先，確保你已經在你的電腦上安裝了 Docker。如果沒有，請參考 [Docker 官方網站](https://docs.docker.com/get-docker/) 來獲取安裝說明。

2. Build DA_Project Docker Image：

    ```bash
    docker build -t test_image .
    ```

3. 運行 Docker 容器：

    ```bash
    docker run -it --network="host" -v .:/app test1_image
    ```

    這個命令會在 Docker 容器中啟動 `test1.py` 。

## 如何執行試題2
1. 首先，執行先執行以下指令安裝所需套件。
    ```bash
    pip install -r requiments.txt
    ```
2. 然後到`試題3`中運行 docker-compose.yml，利用 Docker建立 Mongodb，一樣這裡需要安裝 Docker，可參考`試題1`至官方網站的安裝方式。
    ```bash
    docker-compose -f docker-compose up -d
    ```
3. 直接執行Python腳本即可將`CSV2JSON.csv`資料轉換成 Json格式，並且寫入 Mongodb。
    ```bash
    python test2.py
    ```
## 注意事項

- 請確保你的 Docker 版本符合要求，並且已經正確安裝了 Docker。
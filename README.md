# DA_Project

## 如何使用

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


## 注意事項

- 請確保你的 Docker 版本符合要求，並且已經正確安裝了 Docker。
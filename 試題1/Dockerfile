# 使用python 3.11官方image
FROM python:3.11-slim

# 將requirements.txt複製到/app
COPY requirements.txt /app/requirements.txt

# 在容器中安装 requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# 更新包索引並安装wget和gnupg
RUN apt-get update && apt-get install -y wget gnupg

# 下載並安裝Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 将程式複製到/app目錄下
COPY ./test1.py /app/test1.py

# 設置工作目錄為/app
WORKDIR /app

# 運行程序
CMD ["python", "test1.py"]

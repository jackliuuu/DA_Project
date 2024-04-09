# 使用python 3.11官方image作为基础镜像
FROM python:3.11-slim

# 将requirements.txt复制到/app目录下
COPY requirements.txt /app/requirements.txt

# 在容器中安装 requirements.txt 中指定的 Python 包
RUN pip install --no-cache-dir -r /app/requirements.txt


# 更新软件包索引并安装wget和gnupg
RUN apt-get update && apt-get install -y wget gnupg

# 下载并安装Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 将程序代码复制到/app目录下
COPY ./test1.py /app/test1.py

# 设置工作目录为/app
WORKDIR /app

# 运行程序
CMD ["python", "test1.py"]

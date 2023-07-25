# apt安装所需包
apt update && apt install -y $(cat requirements.apt)
# pip安装所需包
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 启动程序
python3 main.py
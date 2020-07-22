# KoalaGo

A simple search engine with a crawler and simple frontend.

Backend:  TF-IDF implemented with Python.

Frontend: Flask with Bootstrap

Usage:
```shell
pip install requirements.txt -r
mkdir data
cd crawler/
mkdir data
python crawler.py # Pages are saved at /crawler/data by default
python parser.py # Parsed pages are saved at /data by default
cd ../frontend/
python app.py
```

For more detailed introduction, please refer to `KoalaGo-report.pdf` and `KoalaGo-slides.pdf`.

For a live demo, please visit https://bj.zhuohao.me:2333/

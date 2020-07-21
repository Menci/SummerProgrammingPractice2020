rm -rf ./raw
rm -rf ./dict
mkdir ./raw
mkdir ./dict
python3 ./crawler_mt.py
python3 ./parser.py
python3 ./cutter.py
python3 ./index.py

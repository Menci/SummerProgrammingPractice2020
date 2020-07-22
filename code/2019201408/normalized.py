import os
import chardet
from bs4 import BeautifulSoup

def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

def makedir(path) :
    folder = os.path.exists(path)
    if not folder :
        os.makedirs(path)

def normalized_teacher(id) :
    namin = './web/' + str(id)
    namout = './normalized_title/' + str(id)
    fin = open(namin, 'r', encoding = 'utf-8-sig')

    html = fin.read()
    bs = BeautifulSoup(html, 'lxml')

    data = bs.title
    if data :
        fout = open(namout, 'w', encoding = 'utf-8')
        print(data.get_text(), file = fout)
        fout.close
    
    namout = './normalized_body/' + str(id)
    flag = 0
    intro = bs.find('div', class_ = 'intro')
    if intro :
        fout = open(namout, 'w', encoding = 'utf-8')
        flag = 1
        print(intro.get_text(), file = fout)

    data = bs.find_all('div', class_ = 'para')
    if data:
        if flag == 0 :
            fout = open(namout, 'w', encoding = 'utf-8')
            flag = 1
        for data_para in data :
            tmp = data_para.find_all('p')
            if tmp :
                for detial in tmp : 
                    print(detial.get_text(), file = fout)

    fin.close
    if flag == 1 :
        fout.close

def normalized_title(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8-sig')

        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')

        test = bs.find('div', class_ = 'intro')
        if not test :
            Title = bs.title
            if not Title :
                fin.close
                continue
            else :
                fout = open(namout, 'w', encoding = 'utf-8')
                print(Title.get_text(), file = fout)
                fout.close
            fin.close
        else :
            normalized_teacher(id)

def normalized_time(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8-sig')
        
        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')

        Time = bs.find('div', class_ = 'extra_info')
        if not Time :
            fin.close
            continue
        else :
            Time = Time.find('span', class_ = 'date');
            if not Time :
                fin.close
                continue
            else :
                fout = open(namout, 'w', encoding = 'utf-8')
                print(Time.get_text(), file = fout)

        fin.close
        fout.close

def normalized_source(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8-sig')
        
        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')
        
        Source = bs.find('div', class_ = 'extra_info')
        if not Source :
            fin.close
            continue
        else :
            Source = Source.find('span', class_ = 'source');
            if not Source :
                fin.close
                continue
            else :
                fout = open(namout, 'w', encoding = 'utf-8')
                print(Source.get_text(), file = fout)

        fin.close
        fout.close

def normalized_body(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8-sig')
        
        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')

        Body = bs.find('div', class_ = 'essay_body')
        if Body :
            Body = Body.find_all('p');
            if not Body :
                fin.close
                continue
            else :
                fout = open(namout, 'w', encoding = 'utf-8')
                for detial in Body :
                    print(detial.get_text(), file = fout);
                fout.close

        fin.close

def normalized_en_title(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web_en/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8')
        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')

        Title = bs.find('div', class_ = 'title')
        if not Title :
            fin.close
            continue
        else :  
            fout = open(namout, 'w', encoding = 'utf-8')
            print(Title.get_text(), file = fout)

        fin.close
        fout.close

def normalized_en_body(path) :
    for id in range (1, 6796) :
        print(id)

        namin = './web_en/' + str(id)
        namout = path + str(id)
        if not os.path.exists(namin) :
            continue
        ty = get_encoding(namin)
        if (ty != 'utf-8'):
            if (ty != 'UTF-8-SIG') :
                continue
        fin = open(namin, 'r', encoding = 'utf-8')
        html = fin.read()
        bs = BeautifulSoup(html, 'lxml')

        Body = bs.find('div', class_ = 'text')
        if not Body :
            fin.close
            continue
        else :
            Body = Body.find_all('p');
            if not Body :
                fin.close
                continue
            else :
                fout = open(namout, 'w', encoding = 'utf-8')
                for detial in Body :
                    print(detial.get_text(), file = fout);

        fin.close
        fout.close

makedir('./normalized_title')
makedir('./normalized_time')
makedir('./normalized_source')
makedir('./normalized_body')
makedir('./divided_en_title')
makedir('./divided_en_body')

normalized_title('./normalized_title/')
normalized_time('./normalized_time/')
normalized_source('./normalized_source/')
normalized_body('./normalized_body/')
normalized_en_title('./divided_en_title/')
normalized_en_body('./divided_en_body/')
#include<bits/stdc++.h>
#include<dirent.h>
#include<unistd.h>
#include<sys/types.h>
#include "cppjieba/include/cppjieba/Jieba.hpp"
#include "w2v.hpp"

using namespace std;

const char* const DICT_PATH = "./cppjieba/dict/jieba.dict.utf8";
const char* const HMM_PATH = "./cppjieba/dict/hmm_model.utf8";
const char* const USER_DICT_PATH = "./cppjieba/dict/user.dict.utf8";
const char* const IDF_PATH = "./cppjieba/dict/idf.utf8";
const char* const STOP_WORD_PATH = "./cppjieba/dict/stop_words.utf8";
cppjieba::Jieba jieba(DICT_PATH, HMM_PATH, USER_DICT_PATH, IDF_PATH, STOP_WORD_PATH);

unordered_map<string, int> s2i;
vector<pair<string, vector<pair<int,double> > > > dict;
struct T
{
    string url, title, body;
    double tl, bl;
    vector<double> vec;
};
vector<T> htmls;

int getint(FILE* f)
{
    char c;
    while(!isdigit(c = getc(f)));
    int res = c - '0';
    while(isdigit(c = getc(f)))
        res = res * 10 + c - '0';
    return res;
}

double getdouble(FILE* f)
{
    char c;
    while(!isdigit(c = getc(f)));
    double res = c - '0';
    while(isdigit(c = getc(f)))
        res = res * 10 + c - '0';
    if(c == '.')
        for(double t = 0.1; isdigit(c = getc(f)); t /= 10)
            res += t * (c - '0');
    return res;
}

void getstr(FILE* f, string &s)
{
    for(char c = getc(f); c != '\n' && c != '\r'; c = getc(f))
        s.push_back(c);
}

void load()
{
    w2vload();
    FILE* fd=fopen("dict/dict.utf8", "r");
    dict.resize(getint(fd));
    for(int i = 0;i < dict.size(); i++)
    {
        getstr(fd,dict[i].first);
        s2i[dict[i].first] = i;
        dict[i].second.resize(getint(fd));
        for(int j = 0; j < dict[i].second.size(); j++)
        {
            dict[i].second[j].first = getint(fd);
            dict[i].second[j].second = getdouble(fd);
        }
    }
    FILE* fh = fopen("dict/htmls.utf8","r");
    map<string, int> urls;
    htmls.resize(getint(fh));
    for(int i = 0; i < htmls.size(); i++)
    {
        getstr(fh, htmls[i].url);
        urls[htmls[i].url] = i + 1;
        getstr(fh, htmls[i].title);
        getstr(fh, htmls[i].body);
        htmls[i].tl = getdouble(fh);
        htmls[i].bl = getdouble(fh);
        for(int j = 0; j < veclen; j++)
            htmls[i].vec.push_back(wgetdouble(fh));
    }
}

vector<int> gettopX(const string &s) //default word2vec weight is the same as VSM
{
    vector<pair<int, double> > ws;
    jieba.extractor.Extract(s, ws, s2i, dict, -1);
    double sl = 0;
    for(auto x : ws)
        sl += x.second * x.second;
    sl = pow(sl, 0.5);
    vector<double> sco(htmls.size(), 0), times(htmls.size(), 0);
    for(auto i : ws)
        for(auto j : dict[i.first].second)
        {
            int id = j.first / 2;
            times[id]++;
            if(j.first & 1) //title is important than body
                sco[id] += j.second * i.second / htmls[id].bl / sl;
            else
                sco[id] += 2 * j.second * i.second / htmls[id].tl / sl;
        }
    vector<string> tws;
    jieba.Cut(s, tws);
    vector<double> svec(getvec(tws));
    for(int i = 0;i < sco.size(); i++)
        for(int j = 0; j < veclen; j++)
            sco[i] += 4 * htmls[i].vec[j] * svec[j];
    for(int i = 0; i < times.size(); i++)
        sco[i] *= times[i];
    vector<int> topX(10, -1);
    for(int i = 0;i < sco.size(); i++)
    {
        for(int j = 0; j < 10; j++)
            if(topX[j] < 0 || sco[i] > sco[topX[j]])
            {
                for(int k = 9; k > j; k--)
                    topX[k] = topX[k - 1];
                topX[j] = i;
                break;
            }
    }
    return topX;
}

vector<int> gettopC(const string &s) //default VSM
{
    vector<pair<int, double> > ws;
    jieba.extractor.Extract(s, ws, s2i, dict, -1);
    double sl = 0;
    for(auto x : ws)
        sl += x.second * x.second;
    sl = pow(sl, 0.5);
    vector<double> sco(htmls.size(), 0), times(htmls.size(), 0);
    for(auto i : ws)
        for(auto j : dict[i.first].second)
        {
            int id = j.first / 2;
            times[id]++;
            if(j.first & 1) //title is important than body
                sco[id] += j.second * i.second / htmls[id].bl / sl;
            else
                sco[id] += 2 * j.second * i.second / htmls[id].tl / sl;
        }
    for(int i = 0; i < times.size(); i++)
        sco[i] *= times[i];
    priority_queue<pair<double,int>, vector<pair<double,int> >, greater<pair<double,int> > > pq;
    for(int i = 0;i < sco.size(); i++)
    {
        pq.push(make_pair(sco[i], -i));
        if(pq.size() > 100)
            pq.pop();
    }
    vector<int> topC(pq.size());
    for(int i = topC.size() - 1; i >= 0; i--)
    {
        topC[i] = -pq.top().second;
        pq.pop();
    }
    return topC;
}

#include<bits/stdc++.h>
#include "../cppjieba/include/cppjieba/Jieba.hpp"

using namespace std;

const char* const DICT_PATH = "../cppjieba/dict/jieba.dict.utf8";
const char* const HMM_PATH = "../cppjieba/dict/hmm_model.utf8";
const char* const USER_DICT_PATH = "../cppjieba/dict/user.dict.utf8";
const char* const IDF_PATH = "../cppjieba/dict/idf.utf8";
const char* const STOP_WORD_PATH = "../cppjieba/dict/stop_words.utf8";
cppjieba::Jieba jieba(DICT_PATH, HMM_PATH, USER_DICT_PATH, IDF_PATH, STOP_WORD_PATH);

int main()
{
    std::ios::sync_with_stdio(false);
    freopen("wiki.zh.text.jian.utf-8","r",stdin);
    freopen("wiki.zh.text.jian.seg.utf-8","w+",stdout);
    string s;
    int line=0;
    while(getline(cin,s))
    {
        line++;
        vector<string> w;
        jieba.Cut(s,w);
        cerr<<line<<' '<<w.size()<<endl;
        for(int i=0;i<w.size();i++)
            if(w[i].size()>=2)
                cout<<w[i]<<' ';
        cout<<endl;
    }
    return 0;
}

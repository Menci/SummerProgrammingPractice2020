//
//  main.cpp
//  search_engine
//
//  Created by zhangqianyi on 2020/7/16.
//  Copyright © 2020 zhangqianyi. All rights reserved.
//

#include <iostream>
#include <string>
#include <list>
#include <vector>
#include <utility>
#include <fstream>
#include <cmath>

using namespace std;
using std::vector;

float N=1000;

class doc
{
    long docname;
    int frequence=1;
    string URL;
public:
    doc(long x,string y):docname(x),URL(y){};
    doc(long x,int z,string y):docname(x),URL(y),frequence(z){};
    string getURL()
    {
        return URL;
    }
    int getfrequence()
    {
        return frequence;
    }
    long getdocname()
    {
        return docname;
    }
    void addfrequency()
    {
        frequence++;
        return;
    }
    void print()
    {
        cout<<"name:"<<docname<<endl;
        cout<<"fre:"<<frequence<<endl;
        cout<<URL<<endl;
    }
};

class scores
{
    float length=0;
public:
    float score=0;
    doc document;
    scores(doc x):document(x){}
    void getdown()
    {
        score=score/length;
    }
    void calculate(int x,int y)
    {
        float w1=1+log10(x);
        float w2=log10(N/y);
        float q=w1*w2;
        score+=q;
        float z=length*length;
        float p=q*q;
        length=sqrt(z+p);
    }
    void print()
    {
        cout<<document.getURL()<<endl;
    }
};

vector<scores> content;

class wordindex
{
    string word;
    string attribute;
    list<doc> postins;
public:
    wordindex(string x,string y):word(x),attribute(y){}
    void putbuck(doc x)
    {
        postins.push_back(x);
    }
    void buildcontent()
    {
        int t;
        for (auto it=postins.begin(); it!=postins.end(); it++) {
            t=0;
            for (auto jt=content.begin(); jt!=content.end(); jt++) {
                if (jt->document.getdocname()==it->getdocname()) {
                    t=1;
                    jt->calculate(it->getfrequence(), postins.size());
                }
            }
            if (t==0) {
                doc tem(it->getdocname(),it->getURL());
                scores in(tem);
                in.calculate(it->getfrequence(), postins.size());
                content.push_back(in);
            }
        }
    }
    void print()
    {
        int i=0;
        for (auto it=postins.begin(); it!=postins.end(); it++,i++)
        {
            cout<<i<<"."<<word<<attribute;
            it->print();
        }
        return;
    }
    void getin(doc x){
        int t=0;
        if (postins.empty()) {
            postins.push_back(x);
            return;
        }
        for (auto it=postins.begin(); it!=postins.end(); it++) {
            if (x.getdocname()<it->getdocname()) {
                continue;
            }
            else if (x.getdocname()==it->getdocname()) {
                        t=1;
                        it->addfrequency();
                        break;
                    }
            else
            {
                postins.insert(it, x);
                t=1;
                break;
            }
        }
        if (t==0) {
            postins.push_back(x);
        }
        return;
    }
    string getword(){
        return word;
    }
};

vector<wordindex *> dictionary;

bool sortFun(const scores &p1, const scores &p2)
{
    return p1.score > p2.score;
}


void builddic()
{
    string href;
    ifstream file;
    file.open("/Users/zhangqianyi/Desktop/programming_training/URL.txt",ios::in);
    if(!file.is_open())
        return;
    string strLine;
    int num=0;
    while(getline(file,strLine))
    {
        num++;
//        if (num>=4000) {
//            int test=1;
//        }
        if(strLine.empty())
            continue;
        if(strLine.substr(0,4)=="http")
        {
            href=strLine;
            continue;
        }
        doc newdoc(atol(strLine.c_str()), href);
//        cout<<strLine<<endl;
        string index="/Users/zhangqianyi/Desktop/programming_training/cut_content1/"+strLine+"_body.txt";
//        string index="/Users/zhangqianyi/Desktop/programming_training/test_body_cut.txt";
        ifstream in(index,ios::in);
//        istreambuf_iterator<char> beg(in), end;
//        string html(beg, end);

        string index2="/Users/zhangqianyi/Desktop/programming_training/cut_content1/"+strLine+"_tittle.txt";
        ifstream in2(index,ios::in);
//        unsigned long startIndex =0;
//        unsigned long endIndex=0;
//        endIndex=html.find("_",startIndex);
//        if(endIndex!=string::npos)
//        {
//           string word=html.substr(startIndex,endIndex-startIndex);
//
//
//        }
        char word[1024];
        while (in>>word) {
            string tar=word;
            string tarword;
            string tarattribute;
            if (tar=="_w") {
                continue;
            }
            unsigned long length=tar.length();
            unsigned long startIndex =0;
            unsigned long endIndex=0;
            endIndex=tar.find("_",startIndex);
            if(endIndex!=string::npos)
            {
                tarword=tar.substr(startIndex,endIndex-startIndex);
                tarattribute=tar.substr(endIndex,length-endIndex);
//                cout<<tarword<<endl;
//                cout<<tarattribute<<endl;
            }
            int t=0;
            for (auto it=dictionary.begin(); it!=dictionary.end(); it++) {
                if ((*it)->getword()==tarword) {
                    t=1;
                    (*it)->getin(newdoc);
                    break;
                }
            }
            if (t==0) {
                wordindex *newword=new wordindex(tarword,tarattribute);
                newword->getin(newdoc);
                dictionary.push_back(newword);
            }
        }
        in.close();
        while (in2>>word) {
                    string tar=word;
                    string tarword;
                    string tarattribute;
                    if (tar=="_w") {
                        continue;
                    }
                    unsigned long length=tar.length();
                    unsigned long startIndex =0;
                    unsigned long endIndex=0;
                    endIndex=tar.find("_",startIndex);
                    if(endIndex!=string::npos)
                    {
                        tarword=tar.substr(startIndex,endIndex-startIndex);
                        tarattribute=tar.substr(endIndex,length-endIndex);
        //                cout<<tarword<<endl;
        //                cout<<tarattribute<<endl;
                    }
                    int t=0;
                    for (auto it=dictionary.begin(); it!=dictionary.end(); it++) {
                        if ((*it)->getword()==tarword) {
                            t=1;
                            (*it)->getin(newdoc);
                            break;
                        }
                    }
                    if (t==0) {
                        wordindex *newword=new wordindex(tarword,tarattribute);
                        newword->getin(newdoc);
                        dictionary.push_back(newword);
                    }
                }
                in2.close();
    }
    file.close();
    int j=0;
    for (auto it=dictionary.begin(); it!=dictionary.end(); it++,j++)
//        it->print();
        cout<<j<<endl;
    
    return;
}

void readdic()
{
    string infile="/Users/zhangqianyi/Desktop/programming_training/dictionary.txt";
    ifstream in(infile,ios::in);
    unsigned long startIndex=0,endIndex=0,starts=0,ends=0;
    istreambuf_iterator<char> beg(in), end;
    string dic(beg, end);
    in.close();
    for (int pos=0; pos<dic.length(); ) {
        startIndex=dic.find("$",startIndex);
        if (startIndex==string::npos) {
            break;
        }
        endIndex=dic.find("$",startIndex+1);
        string tar=dic.substr(startIndex+1,endIndex-startIndex-1);
        string tarword;
        string tarattribute;
        unsigned long length=tar.length();
        unsigned long sx =0;
        unsigned long ex=0;
        ex=tar.find("_",startIndex);
        if(endIndex!=string::npos)
        {
            tarword=tar.substr(sx,ex-sx);
            tarattribute=tar.substr(ex,length-ex);
        }
        wordindex *newword=new wordindex(tarword,tarattribute);
        startIndex=endIndex;
        endIndex=dic.find("$",startIndex+1);
        starts=startIndex;
        ends=startIndex;
        startIndex++;
        while(true) {
            starts=dic.find("@",starts);
            if (starts>endIndex) {
                break;
            }
            ends=dic.find("@",starts+1);
            string x=dic.substr(starts+1,ends-starts-1);
            starts=ends+1;
            starts=dic.find("@",starts);
            ends=dic.find("@",starts+1);
            string y=dic.substr(starts+1,ends-starts-1);
            starts=ends+1;
            starts=dic.find("@",starts);
            ends=dic.find("@",starts+1);
            string z=dic.substr(starts+1,ends-starts-1);
            doc newdoc(atol(x.c_str()),atoi(y.c_str()),z);
            newword->putbuck(newdoc);
        }
        startIndex++;
    }
}

void queryparser(string x)
{
    string query="/Users/zhangqianyi/Desktop/programming_training/query.txt";
    ofstream out(query,ios::out);
    out<<x;
    out.close();
    string query_cut="/Users/zhangqianyi/Desktop/programming_training/query_cut.txt";
    char str[512],str1[128],str2[128];
    strcpy(str1,query.c_str());
    strcpy(str2,query_cut.c_str());
    sprintf(str,"/Users/zhangqianyi/Desktop/programming_training/cut_word/cut_word/THULAC-master/./thulac -filter -model_dir /Users/zhangqianyi/Desktop/programming_training/THULAC-master/models -input %s -output %s",str1,str2);
    system(str);
    return;
}

bool querysearch()
{
    string query="/Users/zhangqianyi/Desktop/programming_training/query_cut.txt";
    ifstream in(query,ios::in);
    char word[512];
    while (in>>word) {
        string tar=word;
        string tarname;
        string tarattribute;
        if (tar=="_w") {
            continue;
        }
        unsigned long length=tar.length();
        unsigned long startIndex =0;
        unsigned long endIndex=0;
        endIndex=tar.find("_",startIndex);
        if(endIndex!=string::npos)
        {
            tarname=tar.substr(startIndex,endIndex-startIndex);
            tarattribute=tar.substr(endIndex,length-endIndex);
//                cout<<tarword<<endl;
//                cout<<tarattribute<<endl;
        }
        for (auto it=dictionary.begin(); it!=dictionary.end(); it++) {
            if ((*it)->getword()==tarname) {
                (*it)->buildcontent();
                break;
            }
        }
    }
    if (content.empty()) {
        return false;
    }
    for (auto it=content.begin(); it!=content.end(); it++) {
        it->getdown();
    }
    sort(content.begin(), content.end(), sortFun);
    return true;
}

int main(int argc, const char * argv[]) {
    readdic();
    string input;
    cout<<"query:"<<endl;
    while (cin>>input) {
        int i=0;
        queryparser(input);
        bool t=querysearch();
        cout<<"answer"<<endl;
        if (!t) {
            cout<<"No answer"<<endl;
            continue;
        }
        for (auto it=content.begin(); (it!=content.end())&&(i<9); it++,i++) {
            it->print();
        }
        content.clear();
        cout<<"query:"<<endl;
    }
    return 0;
}

//ACM 大赛
//优秀毕业生公示
//积极分子党课
//纽约州立宣讲
//夏令营名单
//明德图灵
//图灵实验班
//博士学位授予
//萨师煊晚会
//计算机专业培养方案
//人大信息学院研究生就业前景如何
//学院和国外高校合作交换的情况



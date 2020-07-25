//
//  main.cpp
//  test_0
//
//  Created by zhangqianyi on 2020/5/30.
//  Copyright © 2020 zhangqianyi. All rights reserved.
//

#include <map>
#include <string>
#include <queue>
#include <iostream>
#include <queue>
#include <map>
#include <string>
#include <fstream>
#include <stdlib.h>

using namespace std;
using std::map;
using std::pair;
using std::string;
using std::vector;
using std::queue;


namespace climb{



class BFSURL
{
private:
    string seed;
public:
    static int num;
    BFSURL(string seeds):seed(seeds){};
    void buildBFSURL();
    void build();
    
};

queue<string> URLQueue;
map<unsigned int ,string > URLmap;
map<unsigned int ,string > isfindURLmap;

std::string ntos(unsigned hashval);
unsigned int encoding(string &x);

std::string ntos(unsigned int hashval) {
    return URLmap[hashval];
}

unsigned int encoding(string &x) {
    const char * s=x.c_str();
    unsigned int hashValue = 0, seed1 = 0xeeeeee, seed2 = 0x34569;
    for(int i = 0; i < (int) strlen(s); i++) {
        unsigned char ch = s[i];
        seed1 = (ch << 3) + (seed1 ^ seed2);
        hashValue = (hashValue << 5) + seed1 + seed2 + ch;
    }
    return hashValue;
}


int BFSURL::num=0;

void BFSURL::buildBFSURL()
{
//    climb::BFSURL::num++;
//    int test=0;
//    if (seed=="http://info.ruc.edu.cn/notice_convert_detail.php?id=1990") {
//    if (num==2850) {
//        test=1;
//    }
//    if(num>=100000)
//    {
//        return;
//    }
    char str[512]={0};
    string tittle=to_string(encoding(seed))+".html";
    char sstr[512]={0};
    strcpy(sstr, tittle.c_str());
    sprintf(str, "wget -O %s %s",sstr,seed.c_str());
    system(str);
    string tittle1="/Users/zhangqianyi/"+tittle;
    ofstream out("/Users/zhangqianyi/Desktop/programming_training/URLs1.txt",ios::app);
    out<<seed<<endl;
    out<<encoding(seed)<<endl;
    out.close();
    ifstream in(tittle1, ios::in);
    istreambuf_iterator<char> beg(in), end;
    string html(beg, end);
    in.close();
    unsigned long startIndex =0;
    unsigned long endIndex=0;
    for(int pos=0;pos<html.length();)
    {
        int x=0;
        startIndex=html.find("href=\"",startIndex);
        if(startIndex==string::npos)
        {
            break;
        }
        startIndex+=6;
        endIndex=html.find("\"",startIndex);
        string href = html.substr(startIndex,endIndex-startIndex);
        unsigned long content=0;
        content=seed.find_last_of("/");
        string newseed=seed.substr(0,content);
        if(newseed.length()<=13)
            newseed="http://info.ruc.edu.cn";
        string min=href.substr(0,4);
        string target;
        if (min=="http") {
            target=href;
            min=href.substr(0,22);
            if (min!="http://info.ruc.edu.cn") {
                x=1;
            }
            unsigned long length=href.length();
            min=href.substr(length-3,3);
            if (min=="css") {
                x=1;
            }
        }
        else target = newseed+"/"+href;
        if (x==1) {
            startIndex=endIndex+1;
            continue;
        }
        if (URLmap.find(encoding(target))==URLmap.end()) {
        URLmap[encoding(target)]=target;
        if(isfindURLmap.find(encoding(target))==isfindURLmap.end())
        {
            URLQueue.push(target);
        }
    }
        startIndex=endIndex+1;
    }
    isfindURLmap[encoding(seed)]=seed;
    if (URLQueue.empty()) {
        return;
    }
//    if(test)
//    {
//        cout<<"**********************"<<endl;
//        int size=URLQueue.size();
//        for (int i=0; i<size; i++) {
//            cout<<URLQueue.front()<<endl;
//            URLQueue.push(URLQueue.front());
//            URLQueue.pop();
//        }
//        int test2=1;
//    }
    return;
}
} // namespace climb

int main()
{
    string seed="http://info.ruc.edu.cn/";
    climb::BFSURL begin(seed);
    begin.buildBFSURL();
    while (!climb::URLQueue.empty()) {
        climb::BFSURL::num++;
        if(climb::BFSURL::num>=100000)
        {
            return 0;
        }
        string nextseed=climb::URLQueue.front();
        climb::URLQueue.pop();
        climb::BFSURL next(nextseed);
        next.buildBFSURL();
    }
    return 0;
}

//
//  main.cpp
//  cut_word
//
//  Created by zhangqianyi on 2020/7/16.
//  Copyright © 2020 zhangqianyi. All rights reserved.
//

#include <iostream>
#include <fstream>
//#include "THULAC-master/include/thulac.h"
#include <stdlib.h>

using namespace std;

int main(int argc, const char * argv[]) {
    ifstream file;
    file.open("/Users/zhangqianyi/Desktop/programming_training/URL.txt",ios::in);
    if(!file.is_open())
        return 0;
    std::string strLine;
    while(getline(file,strLine))
    {
            if(strLine.empty())
                continue;
            if(strLine.substr(0,4)=="http")
                continue;
        char str[1024];
        char str1[128]={0},str2[128]={0};
        string tarindex1,tarindex2,outindex1,outindex2;
        tarindex1="/Users/zhangqianyi/Desktop/programming_training/extract_content/"+strLine+"_tittle.txt";
        tarindex2="/Users/zhangqianyi/Desktop/programming_training/extract_content/"+strLine+"_body.txt";
        outindex1="/Users/zhangqianyi/Desktop/programming_training/cut_content1/"+strLine+"_tittle.txt";
        outindex2="/Users/zhangqianyi/Desktop/programming_training/cut_content1/"+strLine+"_body.txt";
        strcpy(str1,tarindex1.c_str());
        strcpy(str2,outindex1.c_str());
        sprintf(str,"/Users/zhangqianyi/Desktop/programming_training/cut_word/cut_word/THULAC-master/./thulac -filter -model_dir /Users/zhangqianyi/Desktop/programming_training/THULAC-master/models -input %s -output %s",str1,str2);
        strcpy(str1, "");
        strcpy(str2, "");
        system(str);
        strcpy(str1,tarindex2.c_str());
        strcpy(str2,outindex2.c_str());
        sprintf(str,"/Users/zhangqianyi/Desktop/programming_training/cut_word/cut_word/THULAC-master/./thulac -filter -model_dir /Users/zhangqianyi/Desktop/programming_training/THULAC-master/models -input %s -output %s",str1,str2);
        system(str);
        strcpy(str1, "");
        strcpy(str2, "");
    }
//    THULAC test;
//    ifstream in("/Users/zhangqianyi/Desktop/programming_training/test_body.txt",ios::in);
//    istreambuf_iterator<char> beg(in), end;
//    string html(beg, end);
//    in.close();
//    THULAC_result result;
//    test.cut(html,result);
//    ofstream out("/Users/zhangqianyi/Desktop/programming_training/test_tittle.txt",ios::out);
//    for (THULAC_result::iterator it=result.begin(); it!=result.end(); it++) {
//        out<<it->first<<it->second<<endl;
//    }
//    out.close();
    return 0;
}

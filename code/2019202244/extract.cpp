//
//  main.cpp
//  extract
//
//  Created by zhangqianyi on 2020/7/15.
//  Copyright © 2020 zhangqianyi. All rights reserved.
//

#include <iostream>
#include <string>
#include <fstream>
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
        int t=0;
        if(strLine.empty())
            continue;
        if(strLine.substr(0,4)=="http")
            continue;
       string index="/Users/zhangqianyi/Desktop/programming_training/web/"+strLine+".html";
       ifstream in2(index,ios::in);
       istreambuf_iterator<char> beg2(in2), end2;
       string html(beg2, end2);
       in2.close();
       unsigned long startIndex =0;
       unsigned long endIndex=0;
       startIndex=html.find("<title>",startIndex);
        if (startIndex==string::npos) {
            continue;
        }
       string txt;
       if(startIndex!=string::npos)
       {
           startIndex+=7;
           endIndex=html.find("</title>",startIndex);
           txt = html.substr(startIndex,endIndex-startIndex);
       }
        string tarindex="/Users/zhangqianyi/Desktop/programming_training/extract_content/"+strLine+"_tittle.txt";
        ofstream out1(tarindex,ios::out);
        out1<<txt<<endl;
        out1.close();
//        if (strLine=="1929277968") {
//            int test1=0;
//        }
        startIndex =0;
        endIndex=0;
        for (int pos=0; pos<html.length();) {
           startIndex=html.find("=\"content\"",startIndex);
           if(startIndex!=string::npos)
           {
               startIndex=html.find(">",startIndex);
               int stack=1;
               endIndex=startIndex;
               while (stack) {
                   if(stack>20)
                   {
                       t=1;
                       break;
                   }
                   endIndex=html.find("<",endIndex);
                   unsigned long tar=html.find("/>",endIndex);
                   endIndex++;
                   if(tar<html.find("<",endIndex))
                       stack--;
                   
                   if (html.substr(endIndex,1)=="/") {
                       stack--;
                   }
                   else stack++;
               }
               if (t==1) {
                   break;
               }
               unsigned long start=startIndex;
    //           startIndex+=6;
    //           endIndex=html.find("</body>",startIndex);
               unsigned long end=0;
               for(int pos=0;pos<html.length();)
               {
                   start=html.find(">",start);
                   if((start==-1)||(start>endIndex))
                   {
                       break;
                   }
                   end=html.find("<",start);
                   txt=html.substr(start+1,end-start-1);
                   string tarindex2="/Users/zhangqianyi/Desktop/programming_training/extract_content/"+strLine+"_body.txt";
                   ofstream out2(tarindex2,ios::app);
                   out2<<txt<<endl;
                   out2.close();
                   start++;
                }
            }
            else
            {
                t=1;
                break;
            }
            startIndex++;
        }
        if (t==1) {
            startIndex=0;
            startIndex=html.find("<body>",startIndex);
            if(startIndex!=string::npos)
            {
                unsigned long start=startIndex;
                startIndex+=6;
                endIndex=html.find("</body>",startIndex);
                unsigned long end=0;
                for(int pos=0;pos<html.length();)
                {
                    start=html.find("<p",start);
                    if((start==-1)||(start>endIndex))
                    {
                        break;
                    }
                    end=html.find(">",start);
                    while(html.substr(end+1,1)=="<")
                    {
                        end=html.find(">",end+1);
                    }
                    start=end;
                    end=html.find("<",end+1);
                    txt=html.substr(start+1,end-start-1);
                    string tarindex2="/Users/zhangqianyi/Desktop/programming_training/extract_content/"+strLine+"_body.txt";
                    ofstream out2(tarindex2,ios::app);
                    out2<<txt<<endl;
                    out2.close();
                }
             }
        }
    }
//    ifstream in2("/Users/zhangqianyi/Desktop/programming_training/test_body.txt",ios::in);
//    istreambuf_iterator<char> beg2(in2), end2;
//    string html2(beg2, end2);
//    in2.close();
//    string tar[6]={"&nbsp;","&ensp;","&emsp;","&thinsp;","&zwnj;","&zwj;"};
//    for(int i=0;i<6;i++)
//    {
//        for(int pos=0;pos<html.length();)
//        {
//            int unique=0;
//            unique=html2.find(tar[i],unique);
//            if (unique==string::npos) {
//                break;
//            }
//            unique++;
//            html2.erase(unique,tar[i].length());
//        }
//    }
//    ofstream out3("/Users/zhangqianyi/Desktop/programming_training/test_body.txt",ios::out);
//    out3<<html2<<endl;
//    out3.close();
    return 0;
}

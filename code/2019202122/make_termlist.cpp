#include<iostream>
#include<string>
#include<fstream>
#include<string.h>
#include<set>
#include<map>
#include<stdlib.h>
using namespace std;
void analyze_passage(char* doc_path, int doc_num);
void add_term(string term, int doc_num);
#define file_number 6385
map<string, map<int,int>> Term_list;
set<string> stop_wordlist;
//函数总汇处 ，得到词表
void get_termlist() {
	unsigned int num = { 1 };
	char str[128];
	char sstr[128];
	for (;num <= file_number;num++) {
		sprintf(str, "/home/cpp/Content/%d/otitle.txt", num);
		analyze_passage(str, num);
		sprintf(sstr, "/home/cpp/Content/%d/ocontent.txt", num);
		analyze_passage(str, num);
		//cout << num << endl;
	}
}
//该函数用于获得停用词表
void get_stopword() {
	fstream in("/home/cpp/Make_termlist/stop_word.txt");
	if (!in) {
		cout << "Can`t get the stopped word list" << endl;
		exit(0);
	}
	string word;
	while (getline(in, word))  stop_wordlist.insert(word);
}
//文本分析操作函数
void analyze_passage(char* doc_path,int doc_num) {
	fstream in(doc_path);
	if(in) {
		string s;
		while (getline(in, s)) {
			const char* line = s.c_str();
			string term;
			for (int i = 0;i <= strlen(line);i++) {
				if (line[i] == ' '||i==strlen(line)) {
					if (term.size() == 0) continue;
					add_term(term,doc_num);
					term.clear();
					continue;
				}
				term = term + line[i];
			}
		}
	}
	in.close();
}
//用于向termlist中添加词表
void add_term(string term, int doc_num) {
	if (Term_list.find(term) != Term_list.end()) {  //存在这个词
		map<int,int> &Doc_count = Term_list[term];     
		if (Doc_count.find(doc_num) != Doc_count.end()) {    //已存在DocID则词频加一
			Doc_count[doc_num]++;
			//cout << Doc_count[doc_num] << endl;
		}
		else {  //不存在该DocID则设置DocID并设置词频为1
			Doc_count.insert(pair<int, int>(doc_num, 1));
		}
	}
	else {      //不存在这个词
		if (stop_wordlist.find(term) != stop_wordlist.end()) {} //这个词在停用词列表则不计入
		else {   //不在停词表中
			//加入这个词，并初始化DocID 设置词频为1
			Term_list[term].insert(pair<int, int>(doc_num, 1));
		}
	}
}
void Make_termlist() {
	ofstream ofile("Term_list.txt", ios::app);
	for (auto Iter = Term_list.begin();Iter != Term_list.end();Iter++) {
		string term = Iter->first;
		auto docs = Iter->second;
		ofile << term << "<" << docs.size() << "> :";
		for (auto iter = docs.begin();iter != docs.end();iter++) {
			int Doc_ID = iter->first;
			int tf = iter->second;
			ofile << " " << Doc_ID << "(" << tf << ") ";
		}
		ofile << endl;
	}
	ofile.close();
}

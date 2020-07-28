#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <queue>
#include <iostream>
#include <set>
#include <unistd.h>

using namespace std;

char str[1000010];
char ch[1000];

int tot = 0;

void get_html(string url) {
	sleep(1);//limit speed
	//crawl
	char *tmp_url = (char *)url.data();
	sprintf(str, "wget -q -O download.txt %s", tmp_url);
	system(str);
	//write content into file "tot.txt" 
	++ tot;
	sprintf(str, "wget -q -O %d.txt %s", tot, tmp_url);
	system(str);
	//put all urls in one file("url_list.txt") 
	FILE *fp;
	sprintf(str, "[%d]URL:", tot);
	fp = fopen("url_list.txt", "a");
	fwrite(str, sizeof(char), strlen(str), fp);
	fwrite(tmp_url, sizeof(char), strlen(tmp_url), fp);
	ch[0] = '\n';
	fwrite(ch, sizeof(char), 1, fp);
	fclose(fp);
}

queue<string> q;

set<string> prune;

vector<string> url_list;

char Content[1000010];
string Text;

void Extract(string url) {
	//extract content and href
	//find href;
	get_html(url);
	FILE *fp;
	fp = fopen("download.txt", "r");
	memset(Content, 0, sizeof(Content));
	fread(Content, sizeof(char), 1000000, fp);
	Text = "";

	for (int i = 0; i < strlen(Content); ++i) 
		Text.push_back(Content[i]);
	//
	int pos = 0;
	while ((pos = Text.find("href", pos)) != Text.npos){
		int st = Text.find('"', pos) + 1;
		int End = Text.find('"', st) - 1;
		string now = Text.substr(st, End - st + 1);
		url_list.push_back(now); //save urls
		pos = End;
	}

	fclose(fp);
}

bool qualified(string url) {
	
}

int main() {
	string url = "info.ruc.edu.cn";
	q.push(url);
	prune.insert(url);

	string ch = "\\";

	int pos = 0;
	while (!q.empty()) {
		url_list.clear();
		string T = q.front();
		q.pop();
		Extract(T);
		for (int i = 0; i < (int)url_list.size(); ++i) {
			string tmp = url_list[i];
			//normalize url
			if (tmp.find(url, 0) == tmp.npos) {
				if (tmp.find("http", 0) != tmp.npos) continue; //other websites
				if (tmp[0] == '/') tmp = url + tmp;
				else {
					string now = url;
					for (int j = (int)T.length() - 1; j > 0; --j) {
						if (T[j] == '/') {
							now = T.substr(0, j);
							break;
						}
					}
					tmp = now + '/' + tmp;
				}
			}
			else {
				pos = tmp.find(url, 0);
				tmp = tmp.substr(pos, tmp.length() - pos);
			}
			//convert & into "\&"
			pos = 0;
			while ( (pos = tmp.find('&', pos)) != tmp.npos) {
				tmp.insert(pos, ch);
				pos += 2;
			}
			//special judge some useless websites
			if (prune.find(tmp) != prune.end()) continue;
			if (tmp.find("ebook", 0) != tmp.npos) continue;
			if (tmp.find(".doc", 0) != tmp.npos) continue;
			if (tmp.find(".pdf", 0) != tmp.npos) continue;
			if (tmp.find(".css", 0) != tmp.npos) continue;
			if (tmp.find(".xls", 0) != tmp.npos) continue;
			prune.insert(tmp);
			q.push(tmp);
		}
	}
	printf ("%d\n", tot);
	
	return 0;
}

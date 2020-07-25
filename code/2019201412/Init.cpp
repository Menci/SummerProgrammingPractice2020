#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <map>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

char s[10000010];

map<string, int> ID; //string's docid = ?

vector< pair<int, int> > q[100010]; //string, docid, frequency

map<int, string> revID; //docid represent what string?

map<int, int> df; //string's appears how many times in Documents

int tot = 1;

string Text; //save char* to Text

map<int, string> du;// docid represent what url

double idf[100010];

int doctot = 6883;

void pre_idf() { // calc every words' idf 
	for (int i = 1; i < tot; ++i) {
		idf[i] = log10((double)doctot / (double)df[i]);
	} //
	printf ("idf done!\n");
}

map<string, int> words; //query string frequency
map<string, int>::iterator it; //iterator
//for every doc, score, length^2;
double Score[100010];//doc's score
double Length[100010]; //doc's length
vector <int> doc; //save doc's id
map <int , bool> doc_appear;

struct node {
	int id;
	double Val;
}Sort[100010];

bool cmp(node x, node y) {
	return x.Val > y.Val;
}

int topK = 10; // the number of candidates to be selected

void Search_engine() { //search the content
	doc_appear.clear();
	doc.clear();
	words.clear();
	FILE *fp;
	fp = fopen("input.txt", "r");
	Text = "";
	memset(s, 0, sizeof(s));
	fread(s, sizeof(char), 5000000, fp);
	fclose(fp);
	for (int i = 0; i < (int)strlen(s); ++i) Text.push_back(s[i]);
	cout << "text : " << Text << endl;
	int pos = 0;
	//parse input text
	while ( (pos = Text.find('[', pos)) != Text.npos) {
		int Right = Text.find(' ', pos);
		words[Text.substr(pos+1, Right - pos - 1)] ++;
		pos = Right + 1;
	}
	//
	double query_len = 0;
	for (it = words.begin(); it != words.end(); ++it) {
		string now = it->first;
		int val = it->second;
		if (ID[now] != 0) { //now is current string
			int now_id = ID[now];
			double now_val = (1.0 + log10(val)) * idf[now_id];
			query_len += now_val * now_val; //calc now length

			for (int j = 0; j < (int)q[now_id].size(); ++j) {
				int doc_id = q[now_id][j].first;
				int Fre = q[now_id][j].second;
				if (!doc_appear[doc_id]) {
	//				cout << du[doc_id] << endl;
					doc_appear[doc_id] = 1;
					doc.push_back(doc_id);
					Score[doc_id] = 0;
					Length[doc_id] = 0;
				}

				double doc_nowval = (1.0 + log10(Fre)) * idf[now_id];
				Score[doc_id] += now_val * doc_nowval;
				Length[doc_id] += doc_nowval * doc_nowval;
			}
		}
	}

	int Cnt = 0;
	query_len = sqrt(query_len);
	cout << (int)doc.size() << "..." << endl;
	for (int i = 0; i < (int)doc.size(); ++i) {
		Sort[++Cnt].id = doc[i];
		// calc the score
		if (query_len != 0 && Length[doc[i]] != 0) Sort[Cnt].Val = Score[doc[i]] / query_len / sqrt(Length[doc[i]]);
		else Sort[Cnt].Val = 0;
	}
	FILE *fw;
	fw = fopen("result.txt", "w");
	sort(Sort + 1, Sort + Cnt + 1, cmp);
	// output all the topK docids into "result.txt"
	for (int i = 1; i <= min(topK, Cnt); ++i) {
		char *tmp = (char *)du[Sort[i].id].data();
		sprintf(s, "%d\n", Sort[i].id);
		fwrite(s, sizeof(char), strlen(s), fw);
	}
	fclose(fw);
}

int main() {
	FILE *fp;
	fp = fopen("overall.txt", "r");
	memset(s, 0, sizeof(s));
	fread(s, sizeof(char), 10000000, fp);
	fclose(fp);
	Text = "";
	int Len = strlen(s);
	printf ("%d\n", Len);
	for (int i = 0; i < Len; ++i) {
		Text.push_back(s[i]);
	}

	cout << "input done!" << endl;
	
	int End = 0, pos = 0;
	//prework all the strings
	while ( (End = Text.find('\n', pos)) != Text.npos) {
		// get_string
		int Left = Text.find(' ', pos);
		int Right = Text.find(':', Left + 1);
		string now = Text.substr(Left+1, Right - Left - 1);
		ID[now] = tot;
		revID[tot] = now;
		// get string frequency in Documents
		Left = Text.find('[', Right);
		Right = Text.find(']', Left);
		now = Text.substr(Left+1, Right - Left - 1);
		df[tot] = atoi((char*)now.data());
		//get inverse retrieve
		while (1) {
			Left = Text.find('(', Right+1);
			if (Left == Text.npos || Left >= End) break;
			Right = Text.find(')', Left);
			int nowpos = Text.find(' ', Left);
			string L = Text.substr(Left+1, nowpos - Left - 1);
			string R = Text.substr(nowpos+1, Right - nowpos - 1);
			q[tot].push_back(make_pair(atoi((char*)L.data()), atoi((char*)R.data())));
		}

		++ tot;
		pos = End + 1;
	} // 
	printf ("read done!\n");

	pre_idf(); //precalc idf
	Search_engine();

	return 0;
}

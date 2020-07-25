#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <map>
#include <vector>

using namespace std;

char s[1000010];
char filename[1010];
string Text;
map<string, int> df;//document frequency a string have
map<string, int> ID;//give every string an ID
int totID; //id number
map<int, string> revID;//save every id's string
map<string, int> curtf;//current frequency a string in current doc
vector< pair<int , int> > Inverse[100010];//word, docid, frequency
map<string, int>::iterator it;

void calc(int tot) {
	int pos = 0, St = 0, End = 0;
	while ( (St = Text.find('[', pos)) != Text.npos) {
		End = Text.find(' ', St);
		string now = Text.substr(St+1, End-St-1);
		curtf[now] ++;
		pos = End;
	}

	for (it = curtf.begin(); it != curtf.end(); ++it) {
		string Left = it->first;
		int Right = it->second;
		df[Left] += 1;
		if (df[Left] == 1) {
			ID[Left] = ++ totID;
			revID[totID] = Left;
		}
		//create inverse retrieve list: word: a list of pair(docid, frequency the word in the doc) 
		Inverse[ID[Left]].push_back(make_pair(tot, Right));
	}
}

void Output() {
	FILE *fp;
	fp = fopen("overall.txt", "a");
	// output inverse retrieve into "overall.txt" 
	for (int i = 1; i <= totID; ++i) {
		string now = ' ' + revID[i] + ':' + ' ';
		char *tmp = (char*)now.data();
		fwrite(tmp, sizeof(char), strlen(tmp), fp);
		sprintf(s, "[%d] ", df[revID[i]]);
		fwrite(s, sizeof(char), strlen(s), fp);
		for (int j = 0; j < (int)Inverse[i].size(); ++j) {
			sprintf(s, "(%d %d)", Inverse[i][j].first, Inverse[i][j].second);
			fwrite(s, sizeof(char), strlen(s), fp);
		}
		s[0] = '\n';
		fwrite(s, sizeof(char), 1, fp);
	}
	fclose(fp);
}

int main() {
	int St = 1, End = 6883;
	for (int i = St; i <= End; ++i) {
		cout << i << endl;
		curtf.clear();
		Text = "";
		FILE *fp;
		sprintf(filename, "%dcut.txt", i);
		fp = fopen(filename, "r");
		memset(s, 0, sizeof(s));
		fread(s, sizeof(char), 1000000, fp);
		for (int j = 0; j < (int)strlen(s); ++j) Text.push_back(s[j]);
		fclose(fp);
		calc(i);
	}
	Output();
	

	return 0;
}

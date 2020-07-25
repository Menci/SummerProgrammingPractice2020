#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <cstring>
#include <vector>

using namespace std;

char s[1000010];

string Text;
vector<string> q;

void extract() {
	// deal with title information
	if (Text.find("title", 0) != Text.npos) {
		int tl = Text.find("title", 0);
		int tr = Text.find("title", tl+1);
		if (tr != Text.npos) q.push_back(Text.substr(tl, tr-tl));
	}
	//extract strategy: extract all the content between id="content" and id="footer" 
	int St = Text.find("id=\"main\"", 0);
	if (St == Text.npos) return;
	int End = Text.find("id=\"footer\"", St);
	int pos = St;
	if (Text.find("content", St) != Text.npos) {
		pos = Text.find("content", St);
	}
	//text part are between '>' and '<'
	while (pos < End) {
		int Left = Text.find('>', pos) + 1;
		if (Left > End) break;
		int Right = Text.find('<', Left);
		if (Right > End) break;
		q.push_back(Text.substr(Left, Right-Left));
		pos = Right;
	}
}

void output(int tot) {
	FILE *fp;
	sprintf(s, "%dext.txt", tot);
	fp = fopen(s, "w");

	Text = "";
	for (int i = 0; i < (int)q.size(); ++i) {
		string now = q[i];
		string Final = "";
		string Last = "..";
		//eliminate blanks
		for (int j = 0; j < now.length(); ++j) {
			if (now[j] == ' ' || now[j] == '\n') {
				if (Last[0] == ' ' || Last[0] == '\n') continue;
			}
			Last[0] = now[j];
			Final = Final + now[j];
		}
		Text = Text + Final + '\n';
	}
	char *tmp = (char*) Text.data();
	fwrite(tmp, sizeof(char), strlen(tmp), fp);
	fclose(fp);
}

int main() {
	int St = 1, End = 6883;
	for (int i = St; i <= End; ++i) {
		q.clear();
		FILE *fp;
		Text = "";
		sprintf(s, "%d.txt", i);
		fp = fopen (s, "r");
		memset(s, 0, sizeof(s));
		fread(s, sizeof(char), 1000000, fp);
		for (int j = 0; j < (int)strlen(s); ++j) {
			Text.push_back(s[j]);
		}
		fclose(fp);
		extract();
		output(i);
	}
	
	
	return 0;
}

#include <bits/stdc++.h>

const char * T1 = "<title>";
const char * T1_END = "</title>";

const char * T2 = "<p>";
const char * T2_END = "</";

const char * T3 = "<div class=\"para\">";

const char * T4 = "$website:";

void normalize(std::string& S, const std::string& errStr, const std::string& _str)
{
	int pos = S.find(errStr);
	while (pos != -1) {
		S.replace(pos, errStr.length(), _str);
		pos = S.find(errStr);
	}
}

void deleteErr(std::string& S)
{
	int pos = S.find("<");
	while (pos != -1) {
		int ed = S.find(">");
		S.replace(pos, ed-pos+1, "");
		pos = S.find("<");
	}
}

bool outputer(const char * str, const char * T, const char * T_END)
{
	const char * pos = strstr(str, T);

	while (pos) {
		pos += strlen(T);

		const char * ed = strstr(pos, T_END);
		if (ed) {
			char * url = new char[ed - pos + 1];

			if (ed != pos) {

				for (int i = 0; i < ed - pos; ++i) url[i] = pos[i];
				url[ed-pos] = '\0';

				std::string surl = url;
				deleteErr(surl);
				std::cout << surl << std::endl;
			}
			pos = strstr(pos, T);

			delete[] url;
			return true;
		}
	}
	return false;
}

void extractTitleAndP(std::string fileName, int docID)
{
	std::ifstream in;
	in.open(fileName);

	if (!in.is_open()) return ;
	std::string htmlStr = "", tmp;
	while (!in.eof()) {
		getline(in, tmp, '\n');
		htmlStr += tmp;
	}

	const char * str = htmlStr.c_str();
	in.close();
	bool flag = outputer(str, T1, T1_END);
	if (!flag) puts("this is a non-title page");

}


int main()
{
	freopen("result.out", "r", stdin);
	freopen("u_t.out", "w", stdout);

	std::string a;
	for (int i = 1; i <= 6897; ++i) {
		std::cin >> a;
		std::cout << a << std::endl;
		if (i != 1) std::cin >> a;
	}

	for (int i = 1; i <= 6897; ++i) {
		extractTitleAndP(std::to_string(i) + ".txt", i);
	}

	return 0;
}


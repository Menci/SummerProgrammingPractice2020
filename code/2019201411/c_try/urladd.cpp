#include <dirent.h>
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

void outputer(const char * str, const char * T, const char * T_END, std::ostream& out)
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
/*				normalize(surl, "&ldquo;", "\"");
				normalize(surl, "&rdquo;", "\"");
				normalize(surl, "&nbsp", " ");
				*/
				//&ndash -> - //&#8220 -> \" //&#8221 -> \" //&quot; -> \" //&lt; -> < //&gt; -> > //&mdash; -> --
				out << surl << std::endl;
//				std::cout << surl << std::endl;
			}
			pos = strstr(pos, T);

			delete[] url;
		}
	}
}

void extractTitleAndP(std::string fileName)
{
	std::ifstream in;
	in.open(fileName);

	if (!in.is_open()) return ;
	std::string htmlStr = "", tmp;
	while (!in.eof()) {
		getline(in, tmp, '\n');
		htmlStr += tmp;
	}

	in.close();

//	std::cout << htmlStr << std::endl;
	for (int i = 0; i < (int) htmlStr.length(); ++i) {
		if (htmlStr[i] == 0) htmlStr[i] = '0';
	}
	const char * str = htmlStr.c_str();

	std::ofstream out;
	out.open(fileName+"~.cut", std::ios::app);

	out << "url:";
	const char * pos = strstr(str, T4);
	if (pos) {
		pos += strlen(T4);
		out << pos << std::endl;
//		std::cout << pos << std::endl;
	}
}

int main()
{

	std::vector<std::string> alldir;

	DIR * dir = opendir("./");
	dirent * p = NULL;

	while ((p = readdir(dir)) != NULL) {
		if (p->d_name[0] != '.') {
			std::string name = std::string(p->d_name);
			if (strstr(name.c_str(), "txt")) {
				const char * namec = name.c_str();
				if (strstr(namec, "txt~")) continue;
				if (strstr(namec, ".cut")) continue;
				alldir.push_back(name);
			}
		}
	}

	closedir(dir);

	for (auto str : alldir) {
		extractTitleAndP(str);
	}
	std::cerr << alldir.size() << std::endl;

	alldir.clear();
	return 0;
}


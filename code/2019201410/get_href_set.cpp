#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <regex>

using std::cout;
using std::endl;
using std::cerr;
using std::string;
using std::vector;

bool check(string url) {
	if (url.find("http://") != std::string::npos) {
		if (url.find("info.ruc.edu.cn") == std::string::npos)
			return false;
	}
	return true;
}

vector<string> get_href_set_in_file(string content) {
	vector<string> href_set;

	std::regex reg("<a[^<>]*?href=\"(http:[^\"]*|[\\da-zA-Z_/]+(.php[^\"]*|.html))\"[^<>]*?>");
	std::smatch match;

	while (regex_search(content, match, reg)) {
		if (check(match[1].str()))
			href_set.push_back(match[1].str());
		content = match.suffix();
		cerr << match[0].str() << endl << match[1].str() << endl << match[2].str() << endl;
		break;
	}

	return href_set;
}

vector<string> get_href_set(string file_name) {
	std::ifstream in(file_name);

	string content = "";

	if (!in.is_open()) {
		cout << "file open failed" << endl;
		cout << "file " << file_name << endl;
		return vector<string>();
	}

	char c;

	while( (c = in.get()) != EOF) {
		content += c;
	}

	return get_href_set_in_file(content);
}

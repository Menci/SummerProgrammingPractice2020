#include <cstdio>
#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <set> 
#include <cstring>

using std::cout;
using std::endl;
using std::cerr;
using std::string;
using std::vector;

bool isAbsoluteUrl(string url) {
	return url.find("http://") == 0;
}

string get_directory(string current_url) {
	int pos = current_url.rfind("/");
	return current_url.substr(0, pos + 1);
}

void replace_substring(string &url, string src, string dest) {
	for (int i = 0; i < url.length(); i ++) {
		if (url.substr(i, src.length()) == src) {
			url = url.substr(0, i) + dest + url.substr(i + src.length());
		}
	}
}

void normalize(string &current_url, string url) {
	if (isAbsoluteUrl(url)) {
		current_url = url.substr(strlen("http://"));
	}
	else if (url[0] == '/') {
		current_url = "info.ruc.edu.cn" + url;
	}
	else {
		current_url = get_directory(current_url) + url;
	}
	
	if (url.find(".php") == std::string::npos
		&& url.find(".html") == std::string::npos
		&& url.find(".aspx") == std::string::npos) {
		if (*current_url.rbegin() != '/')
			current_url += '/';

		current_url += "index.php";
	}
	replace_substring(current_url, "&amp;", "&");
}

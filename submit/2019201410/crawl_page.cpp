#include <cstdio>
#include <string>
#include <iostream>

using std::string;
using std::cout;
using std::endl;

string get_file_name(string url) {
	string ret = "web/";
	for (int i = url.find('/') + 1; i < url.length(); i ++) {
		if (url[i] == '/') {
			ret += "__";
		}
		else {
			ret += url[i];
		}
	}

	return ret;
}

string get_command(string file_name, string url) {
	string command = "wget -o wget-log -O ";
	for (int i = 0; i < file_name.length() ; i ++) {
		if (file_name[i] == '&') command += '\\';
		command += file_name[i];
	}

	command += " ";

	for(int i = 0; i < url.length(); i ++) {
		if (url[i] == '&') command += '\\';
		command += url[i];
	}
	return command;
} 

string crawl(string url) {
	string file_name = get_file_name(url);
	string command = get_command(file_name, url);

	cout << "str" << command.c_str() << endl;
	if(system(command.c_str())) {
		cout << "wget command failed" << endl;
		cout << "command: " << command << endl;
	}
	
	return file_name;
}

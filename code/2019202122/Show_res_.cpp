#include<httplib.h>
#include<string>
#include<iostream>
#include<string.h>
#include<set>
#include<stdlib.h>
#include<fstream>
#include<vector>
#include"Score.cpp"
using namespace std;

std::vector<string> URL, TITLE, CONTENT;
int r = 0;

void get_res(int DocID,int number) {
	char str[128];
	if (number == 1) sprintf(str, "/home/cpp/Content/%d/url.txt", DocID);
	if(number==2)sprintf(str, "/home/cpp/Content/%d/title.txt", DocID);
	if (number == 3)sprintf(str, "/home/cpp/Content/%d/content.txt", DocID);
	fstream in(str);
	string Res((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
	//cout << Res << endl;
	const char* r = Res.c_str();
	in.close();
	string res;
	res.clear();
	if (Res.size() <= 100) res = r;
	else {
		for (int i = 0;i <= 200;i++) {
			res = res + r[i];
		}
	}

	//cout  << res << endl;

	if (number==1)URL.push_back(res);
	if (number==2)TITLE.push_back(res);
	if (number==3)CONTENT.push_back(res);
}

int main() {
	get_stopword();
	get_termlist();
	cout << "-------------Initialize succesfully,Please input-------------" << endl;
	httplib::Server svr;
	svr.Get("/", [](auto& req, auto& res) {
		auto name = req.get_param_value("name");
		char str[128];
		rank_url(name);
		URL.clear();
		TITLE.clear();
		CONTENT.clear();
		for (int i = 1;i <= top;i++) {
			get_res(topID[i], 1);
			cout << URL[i - 1] << endl;
			get_res(topID[i], 2);
			get_res(topID[i], 3);
		}
		res.set_content(
			URL[0] + "\n" + URL[1] + "\n" + URL[2] + "\n" + URL[3] + "\n" + URL[4] + "\n" + URL[5] + "\n" + URL[6] + "\n" + URL[7] + "\n" + URL[8] + "\n" + URL[9] + "\n"
			, "text/plain");
		});
	svr.listen("0.0.0.0", 1234);
	delete[]topID;
	return 0;
}
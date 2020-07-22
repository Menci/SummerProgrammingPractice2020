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
		res.set_content(
			"<form action='/submit' method='post'accept-charset='UTF-8'>"
			"<input name='name'><button>Submit</button>"
			"</form>"
			, "text/html");
		});

	svr.Post("/submit", [](auto& req, auto& res) {
		auto name = req.get_param_value("name");
		char str[128];
		rank_url(name);
		URL.clear();
		TITLE.clear();
		CONTENT.clear();
		//for (auto iter = Que.begin();iter != Que.end();iter++)  cout << *iter << endl;          //ÓÃÓÚcheck  query
		for (int i = 1;i <= top;i++) {
			get_res(topID[i], 1);
			cout << URL[i - 1] << endl;
			get_res(topID[i], 2);
			get_res(topID[i], 3);
		}

		res.set_content(
			"<head>"
			"<meta charset = 'utf-8' >"
			"<div class='input-group search-margin search-container nofull'>"
			"<form action='/submit' method='post'accept-charset='UTF-8'>"
			"<input type='search' name='name'class='form-control'"
			"autocomplete='off' value=''>"
			"<span class='input-group-btn'>"
			"<button type='submit' class='btn input-lg'>"
			"Submit"
			"</button>"
			"</span>"
			"<div class='bang-container nofull' id='bang-container'>"
			" <div class='bang-boxs'>"
			"<div class='bang-left bangs' id='bang-left'></div>"
			"<div class='bang-right bangs' id='bang-right'></div>"
			"</div>"
			"<div class='aresult-header'>"
			" <div class='aresult-count'>"
			"Top10"
			"</div>"
			"<h4 class='result_header'><a href='" + URL[0] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[0] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[0] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>"
			"<h4 class='result_header'><a href='" + URL[1] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[1] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[1] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[2] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[2] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[2] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[3] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[3] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[3] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[4] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[4] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[4] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[5] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[5] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[5] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[6] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[6] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[6] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[7] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[7] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[7] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>""<h4 class='result_header'><a href='" + URL[8] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[8] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[8] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>"
			"<h4 class='result_header'><a href='" + URL[9] + "' target='_blank' rel='noopener noreferrer'><span"
			"class='highlight'>" + TITLE[9] + "</span> - Âê¿¨°Í¿¨°Ù¿Æ</a></h4>"
			"<p class='result-content'>" + CONTENT[9] + "</p>"
			"<div class=''>"
			"<div class='pull-right'>"
			" </div>"
			, "text/html");
		});

	svr.listen("0.0.0.0", 1234);
	delete[]topID;
	return 0;
}
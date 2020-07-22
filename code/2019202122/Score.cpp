//query parser
//set df.t
//figure tf.td
//score(term in doc)=(1+lg tf.td)*lg(N/df.t)
//func(string query)

#include<iostream>
#include<map>
#include<math.h>
#include<string>
#include<string.h>
#include<set>
#include"make_termlist.cpp"
using namespace std;
#define N 100000.0
#define top 10

int* topID = new int[top + 1];
set<string> query_parser(string query) {

	set<string> query_term;
	char str[128];
	char rm1[128];
	char rm2[128];
	sprintf(rm1, "rm query.txt");
	sprintf(rm2, "rm oquery.txt");
	ofstream ofile("query.txt", ios::app);
	ofile << query;
	ofile.close();
	///////////////////////////用来检查是否创建query.txt成功
	fstream in("query.txt");
	if (!in) {
		cout << "can not get query" << endl;
		exit(0);
	}
	in.close();
	///////////////////////
	sprintf(str, "/home/cpp/THULAC/THULAC/thulac -filter -seg_only -model_dir /home/cpp/THULAC/THULAC/models -input query.txt -output oquery.txt");
	system(str);
	in.open("oquery.txt");
	string query_;
	if (in) {
		getline(in, query_);
		const char* line = query_.c_str();
		string term;
		for (int i = 0;i <= strlen(line);i++) {
			if (line[i] == ' ' || i == strlen(line)) {
				if (term.size() == 0) continue;
				if (stop_wordlist.find(term) == stop_wordlist.end())query_term.insert(term);
				term.clear();
				continue;
			}
			term = term + line[i];
		}
	}
	in.close();
	system(rm1);
	system(rm2);
	return query_term;
}

double get_df(string term) {
	double df=1.0;
	int frequency = 0;
	if (Term_list.find(term) != Term_list.end()) {
		auto iter = Term_list.find(term);
		map<int, int> DocID = iter->second;
		for (auto i = DocID.begin();i != DocID.end();i++) {
			int count = i->second;
			frequency += count;
		}
		df = log10(N / frequency);
			//cout << df << endl;                 //此处用来测试数据
		return df;
	}
	return 0.0;
}
map<int,double> get_tf(string term) {
	map<int, double> tf;
	if (Term_list.find(term) != Term_list.end()) {
		auto iter = Term_list.find(term);
		map<int, int> DocID = iter->second;
		for (auto i = DocID.begin();i != DocID.end();i++) {
			int ID = i->first;
			int count = i->second;
			double soc = 1.0 + log10(double(count));
			tf[ID] = soc;
				//cout << soc << endl;		 //此处用来测试数据
		}
	}
	return tf;
}
map<int, double> get_score(string term) {
	double df=get_df(term);
	map<int,double> tf=get_tf(term);
	map<int, double> score_list;
	for (auto iter = tf.begin();iter != tf.end();iter++) {
		int ID = iter->first;
		double score = (iter->second) * df;
		score_list[ID] = score;
	}
	return score_list;
}
void rank_url(string query) {
	set<string> Que = query_parser(query);
	map<int, double> rank_url;
	//该for循环用于计算分数
	for (auto iter = Que.begin();iter != Que.end();iter++) {  
		map<int, double> score_list = get_score(*iter);
		//cout << *iter << endl;
		for (auto i = score_list.begin();i != score_list.end();i++) {
			int ID = i->first;
			double score = i->second;
			if (rank_url.find(ID) != rank_url.end()) {
				rank_url[ID] = rank_url[ID] + score;
			}
			else {
				rank_url[ID] = score;
			}
		}
	}
	set<int> id;
	for (int i = 1;i <= top;i++) {
		double top_score = 0.0;
		int docID=0;
		for (auto iter = rank_url.begin();iter != rank_url.end();iter++) {
			int ID = iter->first;
			double score = iter->second;
			if ((id.find(ID) == id.end()) && score > top_score) {
				top_score = score;
				docID = ID;
			}
		}
		topID[i] = docID;
		id.insert(docID);
	}
}
void Get_url() {
	char str[128];
	for (int i = 1;i <= top;i++) {
		//cout << topID[i] << endl;        //用于check DOCID
		sprintf(str, "/home/cpp/Content/%d/url.txt", topID[i]);
		fstream in(str);
		if (in) {
			string url((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
			cout << url << endl;
		}
		in.close();
	}
}


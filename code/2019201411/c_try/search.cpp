#include <bits/stdc++.h>
#include <dirent.h>

std::vector<std::string> qry;
std::vector<std::vector<int> > Index;//index[term] term - 1, 2, 3, 4...

int term_id = 0;
std::map<std::string, int> df;
std::map<std::string, int> id;
std::map<int, std::string> id_to_string;

int termIndexInsert(std::string term)
{
	if (!id.count(term)) {
		id_to_string[term_id] = term;
		id[term] = term_id++;
		std::vector<int> empty;
		Index.push_back(empty);
	}

	int tid = id[term];
	return tid;
}

bool cut_query() 
{
	system("python cut_query.py");

	std::ifstream in;
	in.open("query.txt.cut");
	if (!in.is_open()) return false;

	std::string term = "";
	while (!in.eof()) {
		in >> term;
		qry.push_back(term);
		in >> term;
	}

	in.close();
	return true;
}

void extract_term(std::ifstream& in, int docID)
{
	std::string term = "";
	std::map<std::string, int> tf;

	while (!in.eof()) {
		in >> term;
		if (strstr(term.c_str(), "url:")) break;

		int tid = termIndexInsert(term);

		if (!tf[term]) {
			df[term] ++;
			Index[tid].push_back(docID);
		}
		tf[term] ++;

		in >> term;//%*s
	}

	term.replace(0, 4, "");
	std::cout << std::to_string(docID) + ".txt~.cut" << " " << term << std::endl;

	for (auto iter = tf.begin(); iter != tf.end(); ++iter) {
		std::cout << iter->first << " " << iter->second << std::endl;
	}

	tf.clear();
	//term = url
}

bool index_build()
{
	std::vector<std::string> alldir;

	DIR * dir = opendir("./");
	dirent * p = NULL;

	while ((p = readdir(dir)) != NULL) {
		if (p->d_name[0] != '.') {
			std::string name = std::string(p->d_name);
			if (strstr(name.c_str(), ".txt~.cut")) {
				alldir.push_back(name);
			}
		}
	}

	closedir(dir);
//	alldir.push_back("100.txt~.cut");
//	alldir.push_back("1.txt~.cut");
	std::ifstream in;
	int max = 0;
	for (auto filename : alldir) {
		in.open(filename);
		extract_term(in, atoi(filename.c_str()));
		in.close();
	}
}

int main()
{
	freopen("data", "w", stdout);
//	cut_query();
	index_build();

	puts("__sum:");
	for (auto iter = df.begin(); iter != df.end(); ++iter) {
		std::cout << iter->first << " " << iter->second << std::endl;
	}

	puts("list->>");
	for (int i = 0; i < (int) Index.size(); ++i) {
		std::cout << id_to_string[i];
		printf(" %d\n", (int) Index[i].size());
		for (int j = 0; j < (int) Index[i].size(); ++j) {
			printf("%d%c", Index[i][j], j == (int)Index[i].size() - 1 ? '\n' : ' ');
		}
	}
	std::cerr << term_id << std::endl;

	return 0;
}


#include <cstdio>
#include <algorithm>
#include <queue>
#include <string>
#include <set>
#include <vector>
#include <iostream>
#include <queue>
#include <unistd.h>
#include <fstream>

#include "bfs.h"

#define MaxCount 8500

using std::cout;
using std::endl;
using std::cerr;
using std::string;
using std::set;
using std::vector;
using std::queue;

void gap() {
	//sleep(0.005);
}

bool filter(int counter, string url) {
	cerr << counter << endl;
	if (counter > MaxCount) {
		return false;
	}
	return true;
}

void bfs() {

	system("mkdir web");
	queue<string> q;
	set<string> visited;

	string root = "info.ruc.edu.cn/index.php";
	normalize(root, "");

	q.push(root);

	int counter = 0;

	while(!q.empty()) {

		string current_url = q.front();
		q.pop();
		if(visited.find(current_url) != visited.end()) continue;
		visited.insert(current_url);
		++counter;

		if (!filter(counter, current_url)) break;

		gap();
		string file_name = crawl(current_url);

		vector<string> href_set(get_href_set(file_name));
		for (string next_href: href_set) {
			auto next_url = current_url;
			normalize(next_url, next_href);
			if (visited.find(next_url) == visited.end()) {
				q.push(next_url);
			}
		}
	}

	std::ofstream out("list.txt");
	for (auto iter : visited) {
		out << iter << endl;
	}
}

int main() {
	bfs();

	return 0;
}

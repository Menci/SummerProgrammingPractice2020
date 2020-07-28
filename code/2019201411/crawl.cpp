#include <bits/stdc++.h>
#include <unistd.h>

//hash
unsigned int encode(const std::string& url)
{
	unsigned int hashValue = 0, seed1 = 0xeeeeee, seed2 = 0x34569;
	for (int i = 0; i < (int) url.size(); ++i) {
		unsigned char ch = url[i];
		seed1 = (ch << 3) + (seed1 ^ seed2);
		hashValue = (hashValue << 5) + seed1 + seed2 + ch;
	}
	return hashValue;
}
//

const int MAXCOUNTER = 15000;
const double SLEEP_TIME = 0.5;

const char * URL_PRE = "href=\"";
const char * URL_ROOT = "http://info.ruc.edu.cn/";

std::queue<std::string> Q;
std::map<unsigned int, bool> vis;

std::string nameHandler(const std::string& url)
{
	std::string newName; 
	newName.resize(url.size());
	for (int i = 0; i < (int) url.size(); ++i) {
		char ch = url[i];
		if (ch == '\\' || ch == '#' || ch == '/' || ch == '?' || ch == '%' || ch == ';' 
				|| ch == ':' || ch == '+' || ch == '=' || ch == '&' || ch == '(' || ch == ')') {//illegal char
			ch = '_';
		}
		newName[i] = ch;
	}
	return newName + ".txt";
}

static char shellStr[256];

void writeIntoFile(std::string fileName, std::string url)
{

	sprintf(shellStr, "wget -O %s -q --local-encoding=ENC \"%s\"", fileName.c_str(), url.c_str());//FIXME & -> /&
	system(shellStr);
	std::ofstream out;
	out.open(fileName.c_str(), std::ios::app);
	if (out) {
		out << "$website:" << url << std::endl;
		out.close();
	}
	sleep(SLEEP_TIME);

//	delete[] shellStr;
}

bool normalize(const std::string& dir, std::string& url)
{
	assert(url.length() != 0);

	const char * namec = url.c_str();
	if (strstr(namec, "doc") || strstr(namec, "pdf") || strstr(namec, "css") || 
			strstr(namec, "xls") || strstr(namec, "download") || strstr(namec, "rar") || strstr(namec, "flv")) return false;
	if (strstr(url.c_str(), "http")) {
		if (!strstr(url.c_str(), URL_ROOT)) return false;
	}
	else {
		if (url[0] == '/') {
			url = "http://info.ruc.edu.cn" + url;
			return true;
		}
		const char * str = dir.c_str();
		const char * pos = str;
		while (strstr(pos+1, "/")) {
			if (pos-str+1 == dir.length()) break;
			pos = strstr(pos+1, "/");
		}

		if (pos-str+1 == dir.length()) {
			url = dir + url;
		}
		else {
			std::string _url = dir;
			_url.replace(pos-str+1, dir.length()-(pos-str), url);
			url = _url;
		}
	}
	return true;
}


std::map<std::string, std::string> pre;//for debug

void extractUrl(std::string fileName, const std::string &dir)
{
	std::ifstream in;
	in.open(fileName);

	if (!in.is_open()) return ;
	std::string htmlStr = "", tmp;
	while (!in.eof()) {
		in >> tmp;
		htmlStr += tmp;
	}

	in.close();

	const char * str = htmlStr.c_str();
	const char * pos = strstr(str, URL_PRE);

	while (pos) {
		pos += strlen(URL_PRE);

		const char * ed = strstr(pos, "\"");
		if (ed) {
			char * url = new char[ed - pos + 1];
			sscanf(pos, "%[^\"]", url);

			if (ed != pos) {
				std::string surl = url;
				bool flag = normalize(dir, surl);
				unsigned int hashValue = encode(surl);
				if (flag) {
					if (!vis.count(hashValue)) {
						Q.push(surl);
						pre[surl] = fileName;
						vis[hashValue] = true;
					}
				}
			}

			pos = strstr(pos, URL_PRE);

			delete[] url;
		}
	}
}

void CLEAR()
{
	pre.clear();
	vis.clear();
}

void BFS(std::string urlRoot = URL_ROOT)
{
	Q.push(urlRoot);

	int bfs_counter = 0;
	while (!Q.empty()) {
		bfs_counter ++;
/*		if (bfs_counter >= MAXCOUNTER) {
			std::cerr << "TOO MANY" << std::endl;
			exit(0);
		}*/

		std::string curUrl = Q.front();
		std::cout << curUrl << std::endl;

		unsigned int hashValue = encode(curUrl);
		vis[hashValue] = true;

		std::string fileName = std::to_string(bfs_counter)+".txt";//nameHandler(curUrl);
		writeIntoFile(fileName, curUrl);

		//extract url
		extractUrl(fileName, curUrl);

		Q.pop();
	}

	CLEAR();

	return ;
}

int main()
{
	freopen("result.out", "w", stdout);
	BFS();
	return 0;
}


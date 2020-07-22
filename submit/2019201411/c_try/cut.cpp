#include <dirent.h>
#include <bits/stdc++.h>

static char shellStr[256];

int main()
{
	std::vector<std::string> alldir;

	DIR * dir = opendir("./");
	dirent * p = NULL;

	while ((p = readdir(dir)) != NULL) {
		if (p->d_name[0] != '.') {
			std::string name = std::string(p->d_name);
			if (strstr(name.c_str(), "txt~")) {
				alldir.push_back(name);
			}
		}
	}

	closedir(dir);

	for (auto str : alldir) {
		std::string cut = str + ".cut";
		sprintf(shellStr, "python -m jieba -p ^*, --pos ^* -q, --quiet %s > %s", str.c_str(), cut.c_str());//FIXME & -> /&
		system(shellStr);
	}
	std::cerr << alldir.size() << std::endl;

	alldir.clear();
	fclose(stdout);
	return 0;
}
//url : $website:http://info.ruc.edu.cn/news_detail.php?id=1721
//http___info.ruc.edu.cn_news_convert_detail.php_id_268.txt


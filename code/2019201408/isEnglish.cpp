#include <bits/stdc++.h>

std::map <std::string, int> web;

int main () {
    system("mkdir web_en");
    std::ifstream input{"./Reflect"};
    while (!input.eof()) {
        std::string nam = "", tmp = "";
        int id;
        input >>nam;
        if (input.eof()) break;
        while (1) {
            input >>tmp;
            if (tmp[0] >= '0' && tmp[0] <= '9') break;
            else nam = nam + tmp;
        }
        id = std::stoi(tmp);
        if (web.find(nam) == web.end()) {
            web.insert(make_pair(nam, id));
        }
    }
    for (auto p : web) {
        std::string tmp = p.first;
        if (tmp.find("info.ruc.edu.cn/en/") != -1) {
            std::string Command = "";
            Command = "mv ./web/" + std::to_string(p.second) + " ./web_en/";
            std::cout <<p.second <<std::endl;
            system((const char *)(Command.data()));
        }
    }
    return 0;
}
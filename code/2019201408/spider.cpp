#include <bits/stdc++.h>
#include <unistd.h>

int cnt = 0;
std::queue <std::string> que;
std::map <std::string, int> isVis;
std::ofstream output{"Report"};
std::ofstream Reflect{"Reflect"};

std::string geturl(std::string str, int pos) {
    std::string tmp = "";
    int l, r;
    l = str.find("\"", pos) + 1;
    r = str.find("\"", l) - 1;
    tmp = str.substr(l, r - l + 1);
    return tmp;
}

bool Download(std::ofstream &output, std::string url) {
    if (url.find(".rar") + 4 == url.size() || 
        url.find(".doc") + 4 == url.size() || 
        url.find(".png") + 4 == url.size() || 
        url.find(".jpg") + 4 == url.size() || 
        url.find(".docx") + 5 == url.size() || 
        url.find(".xls") + 4 == url.size() || 
        url.find(".flv") + 4 == url.size() || 
        url.find(".css") + 4 == url.size() || 
        url.find(".xlsx") + 5 == url.size()) return false;
    
    output <<"Download: " <<url <<std::endl;
    url = "\"" + url + "\"";
    std::string Command = "wget " + url + " -O " + "./web/" + std::to_string(++cnt);
    system ((const char *)Command.data());
    return true;
}

std::string transUrl(std::string url) {
    int pos;
    while (1) {
        pos = url.find("/");
        if (pos == -1) break;
        else url[pos] = '-';
    }
    while (1) {
        pos = url.find("&");
        if (pos == -1) break;
        else url[pos] = '-';
    }
    return url;
}

void BFS(std::string StartUrl) {
    std::ifstream input;
    
    que.push(StartUrl);
    if (isVis.find(StartUrl) == isVis.end()) {
        Download(output, StartUrl);
        isVis.insert(make_pair(StartUrl, cnt));
    }

    while (!que.empty()) {
        std::string url = que.front();
        que.pop();
        input.open("./web/" + std::to_string(isVis[url]));
        output <<"Processing: " <<url <<std::endl;
        while (!input.eof()) {
            std::string tmp, nxtUrl;
            getline(input, tmp);
            int pos, lapos = 0;
            while (1) {
                pos = tmp.find("href=", lapos);
                if (pos == -1) break;
                lapos = pos + 1;
                nxtUrl = geturl(tmp, pos);
                if (nxtUrl.find("http:") == -1 && nxtUrl.find("https:") == -1) {
                    if (nxtUrl[0] == '/') nxtUrl = StartUrl + nxtUrl;
                    else nxtUrl = StartUrl + "/" + nxtUrl;
                    if (isVis.find(nxtUrl) == isVis.end()) {
                        bool isSuccess = Download(output, nxtUrl);
                        if (isSuccess) {
                            isVis.insert(make_pair(nxtUrl, cnt));
                            que.push(nxtUrl);
                        }
                    }
                } else {
                    if (nxtUrl.find("http://" + StartUrl) == -1) continue;
                    else {
                        if (isVis.find(nxtUrl) == isVis.end()) {
                            bool isSuccess = Download(output, nxtUrl);
                            if (isSuccess) {
                                isVis.insert(make_pair(nxtUrl, cnt));
                                que.push(nxtUrl);
                            }
                        }
                    }
                }
            }
        }
        input.close();
    }
    for (auto i : isVis) {
        Reflect <<i.first <<" " <<i.second <<std::endl;
    }
}
int main () {
    system("mkdir web");
    BFS("info.ruc.edu.cn");
    BFS("info.ruc.edu.cn/en");
    output.close();
    Reflect.close();
    // test();
    return 0;
}
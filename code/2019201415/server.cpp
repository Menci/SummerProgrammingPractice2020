#include <bits/stdc++.h>
#include <stdlib.h>
#include <sys/time.h>
#include "cpp-httplib/httplib.h"
#include "search.hpp"

using namespace std;

string indx;
string res[4];
string sr[4];

void pages_load()
{
    ifstream idx("pages/index.html");
    string t;
    while(getline(idx, t))
        indx = indx + t;
    idx.close();
    ifstream r("pages/result.html");
    int x = 0;
    while(getline(r, t))
    {
        if(!isalpha(t[0]))
        {
            res[x] += t;
            continue;
        }
        x++;
    }
    r.close();
    ifstream srh("pages/search.html");
    x = 0;
    while(getline(srh, t))
    {
        if(!isalpha(t[0]))
        {
            sr[x] = sr[x] + t;
            continue;
        }
        x++;
    }
    srh.close();
}

string gored(const string &p, string str)
{
    vector<string> wp;
    jieba.Cut(p, wp);
    for(auto w : wp)
    {
        if(!isalpha(w[0]) && w.size() <= 3) continue;
        int crt = 0;
        while((crt = str.find(w,crt)) != string::npos)
        {
            str = str.substr(0, crt) + "<em>" + str.substr(crt, w.size()) + "</em>" + str.substr(crt + w.size(), string::npos);
            crt += 9 + w.size();
            if(crt > str.size())
                break;
        }
    }
    return str;
}

string getres(const string &p,int id)
{
    if(id < 0) return "";
    return res[0] + htmls[id].url + res[1] + gored(p,htmls[id].title) + res[2] + gored(p,htmls[id].body) + res[3];
}

string gethtml(const string &p) // w2v is the weight of word2vec
{
    vector<int> topX(gettopX(p));
    string res = sr[0] + p + sr[1] + p + sr[2];
    for(int i = 0; i<topX.size(); i++)
        res = res + getres(p, topX[i]);
    res = res + sr[3];
    return res;
}

string itoa(int x)
{
    char it[10];
    sprintf(it, "%d", x);
    return it;
}

int main()
{
    load();
    pages_load();
	httplib::Server svr;
	svr.Get("/", [](auto &req, auto &res)
	{
        res.set_content(indx, "text/html");
	});

	svr.Get("/search", [](auto &req, auto &res)
	{
        auto qry = req.get_param_value("query");
        if(qry.size())
        {
            vector<int> topC(gettopC(qry));
            string s;
            for(int i = 0; i < topC.size(); i++)
                s += htmls[topC[i]].url + '\n';
            res.set_content(s, "text/plain");
        }
        else
            res.set_content(gethtml(req.get_param_value("q")), "text/html");
	});

	svr.listen("0.0.0.0", 1234);
	return 0;
}

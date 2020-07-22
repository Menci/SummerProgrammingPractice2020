#include<bits/stdc++.h>
#include<dirent.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/stat.h>
#include "cppjieba/include/cppjieba/Jieba.hpp"
#include "w2v.hpp"

using namespace std;

const char* const DICT_PATH = "./cppjieba/dict/jieba.dict.utf8";
const char* const HMM_PATH = "./cppjieba/dict/hmm_model.utf8";
const char* const USER_DICT_PATH = "./cppjieba/dict/user.dict.utf8";
const char* const IDF_PATH = "./cppjieba/dict/idf.utf8";
const char* const STOP_WORD_PATH = "./cppjieba/dict/stop_words.utf8";
cppjieba::Jieba jieba(DICT_PATH, HMM_PATH, USER_DICT_PATH, IDF_PATH, STOP_WORD_PATH);

string cname(string t) //info.ruc.edu.cn
{
	t[15] = '/';
	for(int i = 16;i < t.size(); i++)
		if(t[i] == '.')
			t[i] = '/';
	for(int i = t.size() - 1; i >= 16; i--)
		if(t[i] == '/')
		{
			t[i] = '.';
			break;
		}
    if(t.back() == '.') t[t.size() - 1] = '/';
	t = "http://" + t;
	if(t.find('') != string::npos)
        t.replace(t.find('') - 2, 3, "?");
	return t;
}

string sfind(const string &h, const string &e)
{
	char c;
	string t;
	while((c=getchar())!=EOF)
	{
		t = t + c;
		if(t.size() > h.size())
			t.erase(0, 1);
		if(t == h)
			break;
	}
	if(c == EOF) return " ";
	string res;
	t.clear();
	while((c = getchar()) != EOF)
	{
		res = res + c;
		t = t + c;
		if(t.size() > e.size())
			t.erase(0, 1);
		if(t == e)
			break;
	}
	while(!res.empty() & !t.empty())
	{
		t.pop_back();
		res.pop_back();
	}
	int f;
	while((f = res.find('\t')) != string::npos)
        res.erase(f, 1);
    while((f = res.find('\n')) != string::npos)
        res.erase(f, 1);
    while((f = res.find('\r')) != string::npos)
        res.erase(f, 1);
    while((f = res.find("  ")) != string::npos)
        res.erase(f, 1);
    while(res.find("<script") != string::npos)
    {
        int l = res.find("<script"), r = res.find("</script>",l);
        res.erase(l, r - l);
    }
	while(res.find('<') != string::npos)
	{
        int l = res.find('<'), r = res.find('>',l);
        if(r == string::npos) break;
        res.erase(l, r - l + 1);
	}
	if(res.find('>') != string::npos && h.find('>') == string::npos)
        res.erase(0, res.find('>') + 1);
    while(res.find('>') != string::npos)
        res.erase(res.find('>'), 1);
	return res;
}

map<string, int> s2i;
vector<pair<string,vector<pair<int,double> > > > dict;
struct T
{
    string url, title, body;
    double tl, bl;
    vector<double> vec;
    vector<pair<int, double> > wtitle;
    vector<pair<int, double> > wbody;
    T(const string &s, int id)
    {
    //    if(id%1000==0)
        cerr << id << endl;

        url = cname(s);

        freopen(("./urls/" + s).c_str(), "r", stdin);
        title = sfind("<title>", "<");
        jieba.extractor.Extract(title, wtitle, s2i, dict, id * 2);
        tl = 0;
        for(auto x:wtitle)
            tl += x.second * x.second;
        tl = pow(tl,0.5);

        string t;
        freopen(("./urls/" + s).c_str(), "r", stdin);
        while((t = sfind("<p","<")) != " ")
            body = body + " " + t;
        freopen(("./urls/" + s).c_str(), "r", stdin);
        while((t = sfind("<!--主体-->", "<!-- 底部 -->")) != " ")
            body = body + " " + t;

        jieba.extractor.Extract(body, wbody, s2i, dict, id*2+1);
        vec.resize(veclen);
        vector<string> tw;
        jieba.Cut(title + body, tw);
        int tws = tw.size();
        vec = getvec(tw);
        jieba.Cut(body, tw);
        body.clear();
        for(int i = 0; i < tw.size() && body.size() < 400; i++)
            body += tw[i];
        if(body.size() >= 400) body += "...";
        while(title.size() > 0 && title[0] == ' ') title.erase(0, 1);
        while(body.size() > 0 && body[0] == ' ') body.erase(0, 1);
        bl = 0;
        for(auto x : wbody)
            bl += x.second * x.second;
        bl = pow(bl, 0.5);
        if(body.size()<100) bl/=3;
        if(s.find("news") != string::npos || s.find("notice") != string::npos || s.find("activity") != string::npos)
        {
            bl *= 3;
            tl *= 3;
        }
    }
};
vector<T> htmls;

void ptf()
{
    freopen("./dict/dict.utf8","w+",stdout);
    cout<<dict.size()<<endl;
    for(int i=0;i<dict.size();i++)
    {
        cout<<dict[i].first<<endl;
        cout<<dict[i].second.size()<<endl;
        for(int j=0;j<dict[i].second.size();j++)
            cout<<dict[i].second[j].first<<' '<<dict[i].second[j].second<<endl;
    }
    fclose(stdout);
    freopen("./dict/htmls.utf8","w+",stderr);
    cerr<<htmls.size()<<endl;
    for(int i=0;i<htmls.size();i++)
    {
        cerr<<htmls[i].url<<endl;
        cerr<<htmls[i].title<<endl;
        cerr<<htmls[i].body<<endl;
        cerr<<htmls[i].tl<<' '<<htmls[i].bl<<endl;
        for(int j=0;j<veclen;j++)
            cerr<<htmls[i].vec[j]<<(j+1==veclen?'\n':' ');
    }
    fclose(stdout);
}

int main()
{
    w2vload();
	DIR* dir = opendir("./urls");
	struct dirent *ptr;
	htmls.clear();
	priority_queue<pair<int, string> >pq1, pq2;
	while((ptr = readdir(dir)) != NULL)
        if(ptr -> d_name[0] != '.')
        {
            if(string(ptr -> d_name).find("index") != string::npos || string(ptr -> d_name).back() == '.')
                pq1.push(make_pair(-ptr -> d_reclen, ptr -> d_name));
            else
                pq2.push(make_pair(-ptr -> d_reclen,ptr -> d_name));
        }
    while(!pq1.empty())
    {
        htmls.push_back(T(pq1.top().second, htmls.size()));
        pq1.pop();
    }
    while(!pq2.empty())
    {
        htmls.push_back(T(pq2.top().second, htmls.size()));
        pq2.pop();
    }
    ptf();
	return 0;
}

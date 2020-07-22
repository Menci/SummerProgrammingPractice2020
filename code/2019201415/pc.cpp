#include<bits/stdc++.h>
#include<unordered_set>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>

using namespace std;

string dir="\"urls\"";
string root="http://info.ruc.edu.cn/";

string sfind(string h, string e)
{
	char c;
	string t;
	while((c=getchar())!=EOF)
	{
		t=t+c;
		if(t.size()>h.size())
			t.erase(0,1);
		if(t==h)
			break;
	}
	if(c==EOF) return " ";
	string res;
	t.clear();
	while((c=getchar())!=EOF)
	{
		res=res+c;
		t=t+c;
		if(t.size()>e.size())
			t.erase(0,1);
		if(t==e)
			break;
	}
	while(!res.empty()&!t.empty())
	{
		t.pop_back();
		res.pop_back();
	}
	return res;
}

string cname(string t)
{
	if(t.find("http://")!=string::npos)
		t.erase(0,7);
	for(int i=0;i<t.size();i++)
		if(t[i]=='/')
			t[i]='.';
    if(t.find('?')!=string::npos)
        t.replace(t.find('?'),1,"");
	if(t.back()=='.')
		t+="index.html";
	return t;
}

int main()
{
	freopen("pc.txt","w",stdout);
	unordered_set<string> us;
	queue<pair<string,string> > q;
	q.push(make_pair(root,root));
	us.insert(root);
	int tot=0;
	while(!q.empty())
	{
		string t=q.front().first;
		string tx=q.front().second;
		q.pop();
		cout<<("wget --output-document=\"" + cname(t) + "\" " + t).c_str()<<endl;
		system(("wget --output-document=\"" + cname(t) + "\" " + t).c_str());
		cerr<<tot<<endl;
		tot++;
		freopen(cname(t).c_str(),"r",stdin);
		while((t = sfind("href=\"","\"")) != " ")
			if(us.count(t)==0)
			{
				cout<<t<<endl;
				string x=tx;
				us.insert(t);
				if(t.find("info.ruc.edu.cn")==string::npos)
				{
					if(t.find("http://")==string::npos&&t.find("https://")==string::npos)
					{
						if(t[0]=='/')
						{
							t.erase(0,1);
							t="http://info.ruc.edu.cn/"+t;
						}
						else if(t[0]=='.')
						{
							if(t[1]=='/')
								t.erase(0,2);
							else
							{
								while(t.find("../")!=string::npos)
								{
									t.erase(0,3);
									x.pop_back();
									while(x.back()!='/') x.pop_back();
								}
							}
							t=x+t;
						}
						else
							t=x+t;
					}
					else
						continue;
				}
				if(t=="http://info.ruc.edu.cn") t=t+"/";
				x=t;
				while(x.back()!='/') x.pop_back();
				cout<<t<<' '<<x<<endl;
				us.insert(t);
				q.push(make_pair(t,x));
			}
	}
	return 0;
}

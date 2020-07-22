#include <iostream>
#include <cstring>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <unordered_map>
#include "include/thulac.h"
using std::cout;
using std::unordered_map;
using std::string;
using std::vector;
using std::pair;
using std::ifstream;
using std::ofstream;
using std::endl;
vector<int> DS[160001];
//标题为<title> 正文为<p>
//对于标题考虑： <title> title=" "
//对于正文考虑： <p> <p class="content">
char rt[551],str[551];
char T1[8]="<title>",T2[7]="title=";
char P1[4]="<p>",P2[25]="<p class=\"content\">";
unordered_map<string,int> tf,sign;
unordered_map<string,int> vis;
unordered_map<unsigned long long,int> QC;
vector<string> T,P;
THULAC Y;
THULAC_result  X;
int sn;
string deal(string x){
	int len = x.length(),i = 0,count = 0;
	for(i = 1; i < len; i++) if( x[i] =='-' && x[i-1] == ' '){ count++; break; }
	i++;
	for(; i < len; i++) if( x[i] =='-' && x[i-1] == ' '){ count++; break; }
	if( count != 2) return x;
	char y[i+1];
	memset(y,0,sizeof(y));
	for(int j = 0; j < i-1; j++) y[j] = x[j];
	string w = y;
	return w;
}
bool check(string x){
	int len = x.length();
	for(int i = 0; i < len; i++) if( x[i] != ' ' && x[i] != '\n' && x[i] != '\t' )  return 1;
	return 0;
}

void cmp(char *now,int len,ifstream &infile){
	string A="";
	char B;

	if(len == 6){
		for(int i = 0; i <= len; i++) if(now[i] != T1[i]) return;
		while( !infile.eof() ){
			infile.get(B);
			if(B == '<') break;
			A = A + B;
		}
		if(check(A))T.push_back(A);
	}
	if(len == 3){	
		if(now[1] != 'h' || now[0] != '<' || now[3] != '>' ) return;
		while( !infile.eof() ){
			infile.get(B);
			if(B == '<') break;
			A = A + B;
		}
		if(check(A))T.push_back(A);
	}
	if(len == 2){	
		for(int i = 0; i <= len; i++) if(now[i] != P1[i]) return;
		while( !infile.eof() ){
			infile.get(B);
			if(B == '<') break;
			A = A + B;
		}
		if(check(A))P.push_back(A);
	}
	if(len == 18){
		for(int i = 0; i <= len; i++) if(now[i] != P2[i]) return;
		while( !infile.eof() ){
			infile.get(B);
			if(B == '<') break;
			A = A + B;
		}
		if(check(A))P.push_back(A);
	}

	

}
string FT[15]={"d","h","k","c","p","u","y","e","o","w","q","mq"};
bool ft(string x)
{
	for(int i = 0; i <= 11; i++) if( x == FT[i] ) return 0;
	return 1;
}
void solve(char *now,int num) {
	ofstream clearfile;
	clearfile.open("data2.txt");
	clearfile.close();
	sprintf(str,"wget -O data2.txt '%s' --timeout=10 --tries 4",now);
	system(str);
	ifstream infile("data2.txt");	
	int st = 0;
	char A,B,S[30];
	while( !infile.eof() ) {
		infile.get(A);
		if( A == '<' ){
			st = 0;
			S[0] = '<';
			while( infile.get(S[++st]) && st <= 28) if(S[st] == '>') break;
			cmp(S,st,infile);
		}
		else if( A == 't'){
			st = 0;
			S[0] = 't';
			while( infile.get(S[++st]) && st <= 10) if(S[st] == '=' || S[st] == '\"' || S[st] == ' ') break;
			cmp(S,st,infile);
		}
	}
	infile.close();


	for(auto i = P.begin(); i != P.end(); i++ )
    	{
		X.clear();
		string W = *i;
        	Y.cut(W,X);
        	for(auto j = X.begin(); j != X.end(); j++)
		{
			pair<string,string> Z = *j;
			if(!(check(Z.first)&&ft(Z.second))) continue;
			if(!sign.count(Z.first))
				sign[Z.first] = ++sn;               
			if(vis[Z.first] != num){
	 			tf[Z.first]++; 
				vis[Z.first] = num;
				DS[ sign[Z.first] ].push_back(num);
			}
		}
	}
	for(auto i = T.begin(); i != T.end(); i++ )
   	{
		X.clear();
		string W = *i;
        	Y.cut(deal(W),X);
        	for(auto j = X.begin(); j != X.end(); j++)
		{
			pair<string,string> Z = *j;
			if( !( check(Z.first)&&ft(Z.second)) )  continue;
			if(!sign.count(Z.first))
				sign[Z.first] = ++sn;              
			if(vis[Z.first] != num){
	 			tf[Z.first]++;
				vis[Z.first] = num;
				DS[ sign[Z.first] ].push_back(num);
			}
		}
	}
}

int main() {
	freopen("url2.txt","r",stdin);
	
	int num;
	Y.init("models/",NULL,0,1,0);
	while( scanf("URL %d: ",&num) != EOF){
			int len = 0;
			memset(rt,0,sizeof(rt));
			while(  rt[len++] = getchar() ) if(rt[len-1] == '\n') break;
			rt[len-1] = '\0';
			solve(rt,num);
			T.clear(),P.clear();
	}
	
	freopen("IDF.txt","w",stdout);
	for(auto i : tf)  {
		
		cout << i.first << endl;
		cout << i.second << endl;
		for(auto j = DS[ sign[i.first ]].begin(); j != DS[ sign[i.first ]].end(); j++)
			cout << *j << " ";
		cout << endl;
	}



}

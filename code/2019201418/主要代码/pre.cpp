
#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cmath>
#include "THULAC-master/include/thulac.h"
#include <map>  
#include <queue>
#include <fstream>
using namespace std;
THULAC Y;
THULAC_result X;
bool check(string x){
	int len = x.length();
	for(int i = 0; i < len; i++) if( x[i] != ' ' && x[i] != '\n' && x[i] != '\t' ) return 1;
	return 0;
}
string FT[18]={"d","h","k","c","p","u","y","e","o","w","q","mq"};
bool ft(string x)
{
	for(int i = 0; i <= 11; i++) if( x == FT[i] ) return 0;
	return 1;
}
int main(){
	freopen("app/name.txt","r",stdin);
	freopen("app/Cutname.txt","w",stdout);
	string str;
	cin >> str;
	Y.init("app/THULAC-master/models/",NULL,0,1,0);
	Y.cut(str,X);
	cout << str <<endl;
	for(auto j = X.begin(); j != X.end(); j++)
    	{
	    pair<string,string> Z = *j;                     
	    if(check(Z.first)&&ft(Z.second)) cout << Z.first << endl;
	}
}

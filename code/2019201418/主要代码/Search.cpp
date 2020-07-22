#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <map>  
#include <queue>
#include <fstream>
using namespace std;
const double eps = 1e-7;
double V[605],S[9500],A[605],T[9500],VB[605],B[605];
int R[605],R2[605],IR[605],TotalTF[9500],TotalPTF[9500];
bool Eps(double a){
	if(fabs(a) > eps) 
		return a > 0? 1 : -1;
	else
		return 0;
}
struct cmp
{
	bool operator() (int a,int b) {
		if(!Eps(T[a] - T[b])) return S[a] > S[b]; 
		return T[a] > T[b];
	}
};
bool check(string x){
	int len = x.length();
	for(int i = 0; i < len; i++) if( x[i] != ' ' && x[i] != '\n' && x[i] != '\t' ) return 1;
	return 0;
}
priority_queue<int,vector<int>,cmp> Q;
int N = 6193,tp,Ans[120],LT[9500];
char ord[605];
string Url[9500],Title[9500];
map<string,int> tf,vis,IDF;
bool ok[9500];
void Add(int num,double score,double Tscore) {
	S[num] = score;
	T[num] = Tscore;
	if(tp < 100){
		tp++;
		Q.push(num);
		return;
	}
	int topone = Q.top();
	if( Eps(T[num] - T[topone]) < 0 ) return;
	if( !Eps(T[num] - T[topone]) && S[num] <= S[topone] ) return;
	Q.pop();
	Q.push(num);
}
void Prt(int cnt){
	freopen("app/index.html","w",stdout);
	printf( "<!DOCTYPE html>\n"
		"<html>\n"
		"<head>\n"
		"<meta charset=\"utf-8\">\n"
		"<title>LeavesSearch3.0</title>\n"
		"</head>\n"
		"\n"
		"<body>\n"
		"<br><br>\n"
		"<center>\n"
		"<div id=\"content\" style=\"width:1000px\">\n"
		"<font size=\"54\" color= \"#FF4500\" >Welcome </font>\n"
		"<font size=\"54\" color= \"orange\" >to </font>\n"
		"<font size=\"54\" color= \"#FFD700\" >Leaves</font>\n"
		"<font size=\"54\" color= \"#98FB98\" >Search </font>\n"
		"<font size=\"54\" color= \"blue\" >3.0</font>\n"
		"<br>\n"
		"<br>\n"
		"<form method='post' action='/submit'>\n"
		"<button style=\"  float:right; width: 100px; height: 100px; border-radius:100%%; overflow:hidden; background: url('static/2.jpg') \"  > </button>\n"
		"<br><br>\n"
		"<input value=\"搜索结果如下\" type=\"test\" name='name2' style=\"width: 800px; height: 40px;\">\n"
		"\n"
		"</form>\n"
		"<br> <br>\n"
	      );
	for(int w = cnt; w ; w--){
		int i = Ans[w];
		printf("<p> <a href=\"");
		cout << Url[ i ];
		printf("\">  <font size=5> ");
		cout << Title[ i ]   << endl;
		printf(" </font> </a>  </p> \n");
		printf("<br> \n");
	}
	printf( "</div>\n"
		"</center>\n"
		"</body>\n"
		"</html>\n");
	return;
}

int main(){
	tf.clear();
	vis.clear();
	IDF.clear();
	freopen("app/Cutname.txt","r",stdin);
	string str,Query;
	int Q_tf = 0;
	getline(cin,Query);
	while(getline(cin,str))
    	{    	
    	    if(!check(str)) continue;             
	    if(!vis.count(str))  vis[str] = 1;
	    tf[str]++;
	    Q_tf++;
	}
	ifstream infile("app/THULAC-master/IDF.txt");
	string Word,NM;
	int num,cnt;
	while(!infile.eof()) {
		getline(infile,Word);
		infile >> num ;
		for(int i = 1; i <= num; i++) infile >> LT[i];
		infile.get();infile.get();
		if(!check(Word))continue;
		if(tf.count(Word) ) {
			IDF[Word] = num;
			for(int i = 1; i <= num; i++) ok[ LT[i] ] = 1;
		}
	}
	infile.close();
	int k = 0;
	
	for(auto i : tf) {
		
		k++;
		pair<string,int> I = i;
		if(!check(I.first))continue;
		if(IDF[I.first] != 0)  V[k] = (1.0+log10(I.second)+1.25*(double)I.second/(double)Q_tf)*log10((double)(2*N-IDF[I.first])/(double)(2*IDF[I.first]));
		if(IDF[I.first] != 0)  VB[k] = (1.0+log10(I.second))*log10((double)(2*N-IDF[I.first])/(double)(2*IDF[I.first]));
		vis[I.first] = k;
		IR[k] = IDF[I.first];
	}
	for(int i = 1; i <= N; i++)  if(ok[i]) {
		bool gt = 0;
		memset(A,0,sizeof(A));
		memset(B,0,sizeof(B));
		memset(R,0,sizeof(R));
		memset(R2,0,sizeof(R2));
		sprintf(ord,"app/THULAC-master/Content/UrlContent %d.txt",i);
		ifstream in(ord),in2; 
		double lenth =0.0,score = 0.0,total = 0.0;
		double Tlenth =0.0,Tscore = 0.0,Ttotal = 0.0;
		getline(in,Url[i]);
		while(!in.eof()) {
			getline(in,Word);
			score = 0.0;
			in >> num;
			in.get();
			if(!check(Word))continue;
			if(tf.count(Word) && IDF[Word] != 0) R[ vis[Word] ] += num;
			TotalPTF[i] += num;
		}
		in.close();
		sprintf(ord,"app/THULAC-master/Title/UrlTitle %d.txt",i);
		in2.open(ord);
		in2 >> num;in2.get();
		//printf("%d %d\n",i,num);
		getline(in2,Url[i]);
		getline(in2,Title[i]);
		string tt;
		
		//cout << Title[i] <<endl;
		for(int j = 2; j <= num; j++){	
			getline(in2,tt);
			if(!check(tt)){ j--; continue;}
			if(Query == tt) gt = 1;
		}
		if(Query == Title[i]) gt = 1;
		while(!in2.eof()) {
			getline(in2,Word);
			score = 0.0;
			in2 >> num;
			in2.get();
			if(!check(Word))continue;
			if(tf.count(Word) && IDF[Word] != 0){
				R[ vis[Word] ] += num;
				R2[ vis[Word] ] += num;
			}
			TotalTF[i] += num;
		}
		in2.close();
		if(!TotalPTF[i]) TotalPTF[i] = 1;
		if(!TotalTF[i]) TotalTF[i] = 1;
		for(int j = 1; j <= k; j++) 
		{
			if(IR[j] && R[j])  A[j] = (1.0+log10(R[j])+0.25*(double)R2[j]/(double)TotalTF[i]+(double)R[j]/(double)TotalPTF[i])*log10((double)(2*N-IR[j])/(double)(2*IR[j]));
			if(IR[j] && R2[j])  B[j] = (1.0+log10(R2[j]))*log10((double)(2*N-IR[j])/(double)(2*IR[j]));
			total += A[j]*V[j];
			lenth += A[j]*A[j];
			Ttotal += B[j]*V[j];
			Tlenth += B[j]*B[j];
		}
		score = 0.0;Tscore = 0.0;
		if(Eps(lenth)) score = total/sqrt(lenth);
		if(Eps(Tlenth)) Tscore = Ttotal/sqrt(Tlenth);
		if(gt) Tscore = 1e8;
		Add(i,score,Tscore);
	}
	cnt = 0; 

	while(!Q.empty()){
		Ans[++cnt] = Q.top();
		Q.pop();
	}

	freopen("app/ans.txt","w",stdout);
	for(int w = cnt; w  ; w--){
		int i = Ans[w];
		cout << Url[ i ] << endl;
	}

	//Prt(cnt);
	return 0;
	
}




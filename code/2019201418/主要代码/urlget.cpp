#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <queue>
#include <map>
#include <iostream>
using namespace std;
queue<char*> Q;
char rt[528],str[528];
char CN[10] = "_convert";
map<unsigned long long ,bool> vis;
int cnt;
unsigned long long Hash(char* now)  
{  
    if(!*now)  return 0;  
    register unsigned long long hash = 2166136261;  
    while (1)  
    {  
    	if( (*now) == '#' )break;
        unsigned long long ch = (unsigned long long)*now++;
        if(!ch)break;
        hash *= 16777619;  
        hash ^= ch;  
    }  
    return hash;  
}
void Deal(char *now) {
	int len=strlen(now),r;
	if(now[4] == ':'){
		if(now[7] != 'i' || now[8] != 'n' || now[9] != 'f' || now[10] != 'o' ||
	   	now[12] != 'r' || now[13] != 'u' || now[14] != 'c' ||
	   	now[16] != 'e' || now[17] != 'd' || now[18] != 'u' ||
	  	 now[20] != 'c' || now[21] != 'n') return;
	  	if( len > 23 && now[23] == 'd')return;
	  	for(int i = 23; i < len ; i++) if(now[i] == '_'){
	  		for( r = 0; i+r < len && r < 8 ; r++) if(now[i+r] != CN[r]) break;
	  		if( r == 8 ){
	  			for(int k = i; k < len-8; k++) now[k] = now[k+8];
	  			for(int k = len-8; k < len; k++) now[k] = '\0';
	  			break;
	  		}
	  	}
	}
	if(now[4] == 's'){
		if(now[8] != 'i' || now[9] != 'n' || now[10] != 'f' || now[11] != 'o' ||
	   	now[13] != 'r' || now[14] != 'u' || now[15] != 'c' ||
	   	now[17] != 'e' || now[18] != 'd' || now[19] != 'u' ||
	  	 now[21] != 'c' || now[22] != 'n') return;
	  	if( len > 24 && now[24] == 'd')return;
	  	for(int i = 24; i < len ; i++) if(now[i] == '_'){
	  		for( r = 0; i+r < len && r < 8 ; r++) if(now[i+r] != CN[r]) break;
	  		if( r == 8 ){
	  			for(int k = i; k < len-8; k++) now[k] = now[k+8];
	  			for(int k = len-8; k < len; k++) now[k] = '\0';
	  			break;
	  		}
	  	}
	}
	if(now[4] != ':' && now[4] != 's') return;
	unsigned long long hashnum = Hash( now );
	if( !vis[hashnum] ) {		
		vis[hashnum] = 1;
		char *X = new char[528];
		strcpy(X,now);
		Q.push(X);
		cnt++;
	}
}
void Solve( char *now ) {
	sprintf(str, "wget -O data.txt '%s'  --timeout=10  --tries 4", now);
	system(str);
	freopen("data.txt","r",stdin);
	char h,r,e,f,sg,A;
	int num = 0;
	char S[528],CP[528];
	while( ( h = getchar() ) != EOF ) {
		if( h == 'h' ) {
			r = getchar();
			e = getchar();
			f = getchar();
			sg = getchar();
			if( r == 'r' && e == 'e' && f == 'f' && sg == '=' ){
				num = 0;
				getchar();
				memset(S,0,sizeof(S));
				memset(CP,0,sizeof(CP));
				while( A = getchar()  ){
					if(A == '"' || A == '\'') break;
					S[num++] = A;
	 				if(num>=280) return;				 
				}
				if(num>=280)continue;
				if(S[num-1] == 's' && S[num-2] == 's' && S[num-3] == 'c') continue;
				if(S[num-1] == '4' && S[num-2] == 'p' && S[num-3] == 'm') continue;
				if(S[num-1] == 'x' && S[num-2] == 's' && S[num-3] == 'l') continue;
				if(S[num-1] == 's' && S[num-2] == 'l' && S[num-3] == 'x') continue;
				if(S[num-1] == 'c' && S[num-2] == 'o' && S[num-3] == 'd') continue;
				if(S[num-1] == 'x' && S[num-2] == 'c' && S[num-3] == 'o') continue;
				if(S[num-1] == 'r' && S[num-2] == 'a' && S[num-3] == 'r') continue;
				if(S[num-1] == 'f' && S[num-2] == 'd' && S[num-3] == 'p') continue;
				if(S[num-1] == 't' && S[num-2] == 'x' && S[num-3] == 't') continue;
				if(S[num-1] == 'v' && S[num-2] == 'l' && S[num-3] == 'f') continue;
				if(S[num-1] == 'g' && S[num-2] == 'n' && S[num-3] == 'p') continue;
				if(S[num-1] == 'g' && S[num-2] == 'p' && S[num-3] == 'j') continue;
				if( S[0] == 'h' && S[1] == 't' && S[2] == 't' && S[3] == 'p' )
				{
					Deal(S);

				}	
				else {
 					int len = strlen(now); 
					strcpy(CP,now);
					if(S[0] == '/'){
 						strcpy(CP,rt);
						int len = strlen(CP);
					        if(CP[len-1]=='/') CP[len-1] = CP[len];
						strcat(CP,S);
						Deal(CP);
					}
					if(S[0] != '.' && S[0] != '/'){
						int f = strlen(CP),l=f;
                                                while(CP[f-1] != '/'&& f) f--;
                                                for(int i = f; i < l ; i++) CP[i] = CP[l];;
						strcat(CP,S);
						Deal(CP);
						continue;
					}
					if(S[0] == '.' && S[1] == '/'){
						int lenS = strlen(S);
						for(int i = 0; i < lenS ; i++) S[i] = S[i+1];
						int f = strlen(CP),l=f;
                                                while(CP[f-1] != '/'&& f) f--;
                                                for(int i = f-1; i < l ; i++) CP[i] = CP[l];;
						strcat(CP,S);
						Deal(CP);
						continue;
					}
					if(S[0] == '.' && S[1] == '.' && S[2] == '/'){
						int f = strlen(CP),l=f;
						int lenS = strlen(S);
						while(CP[f-1] != '/'&& f) f--;
						f--;
						while(CP[f-1] != '/'&& f > 0) f--;
						for(int i = f-1; i < l ; i++) CP[i] = CP[l];
						for(int i = 0; i < lenS ; i++) S[i] = S[i+2];
						strcat(CP,S);
						Deal(CP);
						continue;
					}	
			
 				}		
			}	
		}
	}

	fclose(stdin);
}
int main()
{
	freopen("url.txt","w",stdout);
	int Num = 0;cnt++;
	scanf("%s",rt);
	Q.push(rt);
	while( !Q.empty() ) {
		char *now = Q.front();
		Q.pop();cnt--;
		vis[Hash(now)] = 1;
		Solve( now );
		Num++;
		printf("URL %d: %s\n",Num,now);
		if(Num != 1) delete []now;
	}
	return 0;
}

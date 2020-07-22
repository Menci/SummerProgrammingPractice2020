#include<bits/stdc++.h>
#include<unordered_map>

using namespace std;

const char* VEC_DIR = "dict/vectors.model";

int wgetint(FILE* f)
{
    bool neg = false;
    char c;
    while(!isdigit(c=getc(f)))
        if(c == '-')
            neg = true;
    int res = c-'0';
    while(isdigit(c = getc(f)))
        res = res * 10 + c - '0';
    if(neg) res = -res;
    return res;
}

double wgetdouble(FILE* f)
{
    bool neg = false;
    char c;
    while(!isdigit(c = getc(f)))
        if(c == '-')
            neg = true;
    double res = c-'0';
    while(isdigit(c = getc(f)))
        res = res * 10 + c - '0';
    if(c == '.')
        for(double t = 0.1; isdigit(c = getc(f)); t /= 10)
            res += t * (c - '0');
    if(c == 'e')
        res *= pow(10.0, wgetdouble(f));
    if(neg) res = -res;
    return res;
}

void wgetstr(FILE* f,string &s)
{
    for(char c = getc(f); c != '\n' && c != '\r' && c != ' '; c = getc(f))
        s.push_back(c);
}

unordered_map<string, int> w2i;
vector<vector<double> > i2v;
int veclen;

void w2vload()
{
    FILE* f = fopen(VEC_DIR,"r");
    int n, l;
    n = wgetint(f);
    l = wgetint(f);
    veclen = l;
    i2v.resize(n);
    for(int i = 0; i < n; i++)
    {
        string s;
        wgetstr(f, s);
        w2i[s] = i;
        i2v[i].resize(veclen);
        double x = 0;
        for(int j = 0; j < l; j++)
        {
            i2v[i][j] = wgetdouble(f);
            x += i2v[i][j] * i2v[i][j];
        }
        getc(f);
        x = pow(x,0.5);
        for(int j = 0; j < l; j++)
            i2v[i][j] /= x;
    }
}

vector<double> getvec(vector<string> &ws)
{
    vector<double> vec(veclen,0);
    for(auto w:ws)
        if(w2i.count(w))
            for(int i = 0, id = w2i[w]; i < veclen; i++)
                vec[i] += i2v[id][i];
    double len = 0;
    for(int i = 0; i<veclen; i++)
        len += vec[i]*vec[i];
    len = pow(len,0.5);
    for(int i = 0; i < veclen; i++)
        vec[i] /= len;
    return vec;
}

#include<fstream>
#include<iostream>
#include<cstdlib>
//#include"include/thulac.h"
using namespace std;
void CWS() {                //Chinese Word Segmentation
	char str[128];
	char sstr[128];
	char ssstr[128];
	int num = { 1 };
	sprintf(str, "/home/cpp/Content/%d/title.txt", num);
	//sprintf(str, "/home/cpp/Content/Content/3/title.txt");
	sprintf(sstr, "./thulac -filter -seg_only -input /home/cpp/Content/%d/title.txt -output /home/cpp/Content/%d/otitle.txt",num,num);
	sprintf(ssstr, "./thulac -filter -seg_only -input /home/cpp/Content/%d/content.txt -output /home/cpp/Content/%d/ocontent.txt",num,num);
	fstream in(str);
	in.close();
	while (in) {
		system(sstr);
		system(ssstr);
		cout << num << endl;
		num++;
		sprintf(str, "/home/cpp/Content/%d/title.txt", num);
		sprintf(sstr, "./thulac -filter -seg_only -input /home/cpp/Content/%d/title.txt -output /home/cpp/Content/%d/otitle.txt",num,num);
		sprintf(ssstr, "./thulac -filter -seg_only -input /home/cpp/Content/%d/content.txt -output /home/cpp/Content/%d/ocontent.txt",num,num);
		in.open(str);
		in.close();
	}
}
int main() {
	CWS();
	return 0;
}

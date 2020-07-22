#include <bits/stdc++.h>

const int N = 6896;
const int K = 100;

static int term_cnt = 0;
std::vector<std::vector<int> > Index;
std::map<std::pair<int, int>, double> tf;
std::map<int, int> df;
std::map<std::string, int> id;

static char str[256];
//static double length[N + 5];
static std::string url[N + 5];

int tf_init(int docID)
{
	std::cin >> url[docID];
	while (true) {
		std::string term;
		std::cin >> term;
		if (strstr(term.c_str(), "__sum")) return -1;
		if (strstr(term.c_str(), "txt~.cut")) return atoi(term.c_str());

		if (!id.count(term)) {
			id[term] = term_cnt++;
		}
//		length[docID] ++;

		int times = 0; scanf("%d", &times);
		tf[std::make_pair(id[term], docID)] = times;
		assert(times != 0);
	}
	return -2;
}

int df_init()
{
	int times = 0;
	std::string term = "";

	while (true) {
		std::cin >> term;
		if (term == "list->>") return -1;
		scanf("%d", &times);
		df[id[term]] = times;
		assert(times != 0);
	}

	return 0;
}

std::vector<int> qry;
std::map<int, double> fq;

bool cut_query() 
{
	system("python cut_query.py");

	std::ifstream in;
	in.open("query.txt.cut");
	if (!in.is_open()) return false;

	std::string term;
	while (in>>term) {
		int term_id = id[term];
		if (!fq.count(term_id)) fq[term_id] = 1.0;
		else fq[term_id] += 1;
		qry.push_back(id[term]);
		in >> term;
	}

	in.close();
	return true;
}

struct TRI
{
	int doc;
	std::pair<double, double> value;
	bool operator < (const TRI& rhs) const{
		return value > rhs.value;
	}
};

int main()
{
	freopen("data", "r", stdin);

	scanf("%s", str);
	int docID = atoi(str);

	while ((docID = tf_init(docID)) >= 0);

	df_init();

	for (int i = 0; i < term_cnt; ++i) {
		std::vector<int> vec;
		Index.push_back(vec);
	}

	std::string term = "";
	int n;
	while (std::cin >> term >> n) {
		int term_id = id[term];
		for (int i = 0, docID; i < n; ++i) {
			scanf("%d", &docID);
			Index[term_id].push_back(docID);
		}
		std::sort(Index[term_id].begin(), Index[term_id].end());
	}

	for (auto iter = tf.begin(); iter != tf.end(); ++iter) {
		std::pair<int, int> td = iter->first;
		double& w = iter->second;
		w = (1 + log10(w)) * log10(1.0*N/df[td.first]);
	}

	fclose(stdin);

	std::cerr << "INDEX_BUILD COST : " << (double) clock()/CLOCKS_PER_SEC << std::endl;

	freopen("query.res", "w", stdout);
	cut_query();

	std::vector<int> uDoc;
	std::vector<int> temp;
	for (int term_id : qry) {
		uDoc.clear();
		set_union(temp.begin(), temp.end(), Index[term_id].begin(), Index[term_id].end(), back_inserter(uDoc));
		temp = uDoc;
	}

	for (auto iter = fq.begin(); iter != fq.end(); ++iter) {
		int term_id = iter->first;
		double& w = iter->second;
		w = (1 + log10(w)) * log10(1.0*N/df[term_id]);
//		std::cerr << w << std::endl;
	}

	std::vector<TRI> docScores;
	for (int doc : uDoc) {
		double score = 0, length = 0, extra = 0;
		for (int term : qry) {
			std::pair<int, int> td = std::make_pair(term, doc);
			if (tf.count(td)) {
				score += tf[td] * fq[term];
				length += tf[td] * tf[td];
				extra += tf[td];
			}
		}
//		std::cout << score << " " << length << " " << doc << std::endl;
		length = sqrt(length);
		score /= length;
//		if (doc == 4736) fprintf(stderr, "%.5f\n", score);
		docScores.push_back(TRI{doc, std::make_pair(score, 0)});
	}

	std::sort(docScores.begin(), docScores.end());
//	std::cerr << -docScores[0].value.first << std::endl;
	for (int i = 0; i < std::min(K, (int)docScores.size()); ++i) {
		std::cout << url[docScores[i].doc] << std::endl;
	}

	fclose(stdout);
	std::cerr << "TOPK_GET COST : " << (double) clock()/CLOCKS_PER_SEC << std::endl;
	qry.clear();
	fq.clear();

	Index.clear();
	tf.clear();
	df.clear();
	id.clear();

	return 0;
}


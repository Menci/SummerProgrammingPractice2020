objects = bfs.o crawl_page.o get_href_set.o normalizer.o

gen: $(objects)
	g++ -std=c++17 -O2 -o gen $(objects)

bfs.o: bfs.cpp
	g++ -std=c++17 -O2 -c bfs.cpp

crawl_page.o: crawl_page.cpp
	g++ -std=c++17 -O2 -c crawl_page.cpp

get_href_set.o: get_href_set.cpp
	g++ -std=c++17 -O2 -c get_href_set.cpp

normalizer.o: normalizer.cpp
	g++ -std=c++17 -O2 -c normalizer.cpp

clean:
	rm $(objects)

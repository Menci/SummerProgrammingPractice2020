# IR Grader
This grader program will help us grading your search engine program.

You need to start a web server and handle a GET request to a URL (specfied by yourself). Our request will have `?query=关键词` appended to the URL and your response body is expected to be a string with one url in each line.

The usage of the submit client is:

```bash
$ ./client.py student_id your_url
```

For example:

```bash
$ ./client.py 2019114514 http://127.0.0.1:1234/abc
```

# Running the server
You need three files to put into `server_data` directory to run the grader server.

* `urls.bin`
* `sim.bin`
* `student_id_list`
* `testdata`

You can download `urls.bin` and `sim.bin` from the [releases](https://github.com/Menci/SummerProgrammingPractice2020/releases). The `urls.bin` is a URL list of ALL pages in the [website](http://info.ruc.edu.cn/) crawled with [web-crawler](https://github.com/Menci/web-crawler). The `sim.bin` is the [Jaccard Similarity](https://en.wikipedia.org/wiki/Jaccard_index) of all the pages, two URLs are considered the same if their Jaccard Similarity is larger than 0.9.

The `student_id_list` file includes a list of allowed student IDs to submit, each line is a student ID. The `student_id_list` file we used is provided in the directory.

The `testdata` file includes the queries to run and the expected URL. Each line is a URL, a space and its query text followed. Unfortunately, we don't provide our final test data. The sample `testdata` file is provided in the directory.

The `server.py` will load data and start a HTTP server on `0.0.0.0:54321`. You just need to set the `client.py` to connect to it. For testing purpose, you can set a environment variable `SUBMIT_SERVER=http://127.0.0.1:54321` to tell the client to connect to the locally running server. You can also change the default server URL in `client.py`.

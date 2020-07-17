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

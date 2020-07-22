## Basic Information and Functions

The project is written totally in python 3, and the frontend part uses the python web framework Django.

The task of the course is to build a tiny search engine that is able to analyze, index, retrieve and mine the collected webpage pool. So of course this project has to support some functions including crawling webpages, analyzing information on them, and build up inverted index according to that.

This project **CANNOT** deal with fuzzy searches, which is more complex and difficult, and optional to this course.

In specific, in this course, we are just dealing with all the webpages under the domain [http://info.ruc.edu.cn/](http://info.ruc.edu.cn/).

## Usage

### Prerequisites

To build and use this project, you should have the following software installed on your computer:

+ `python 3.6+`
+ `redis`

And also the following packages of python 3:

+ `bs4` (for parsing HTML)
+ `django`
+ `jieba` (for dealing with content on the webpages)
+ `redis`
+ `zhon`

all the packages above are in the latest version.

### Build

We have already created a script `./build.sh` for building this project. So you can simply open a terminal in the project directory and execute it. 

```
sudo ./build.sh
```

If nothing wrong happens, you can try to access `http://localhost:8000` to search something you are interested in.

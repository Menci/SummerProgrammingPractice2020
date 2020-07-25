from flask import request , render_template
from app import app
import os,sys

@app.route("/", methods=["GET"])
def query():
	X = request.args["query"]
	f = open("app/name.txt","w")
	f.write(X)
	f.close()
	os.system('app/pre')
	os.system('app/Search')
	sz = os.path.getsize('app/ans.txt')
	fd = os.open("app/ans.txt",os.O_RDWR)
	ret = os.read(fd,sz)
	os.close(fd)
	return ret

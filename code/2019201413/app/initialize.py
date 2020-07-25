import parser
import crawler

target = open("target_website.txt", "r").read()[:-1]
crawler.getpages(target)
parser.parse_all()
print("parse finished")
parser.calculate()
print("calculate finished")
parser.save_data()
print("save finished")

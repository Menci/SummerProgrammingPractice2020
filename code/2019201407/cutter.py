import os
import jieba
from ess import *
from arguments import *
import jieba.posseg as pseg
import crawler_mt

def cut_to_file(text, filename):
    f = open(filename, mode = "w")
    for sentence in text.lower().split(): # lower_case
        words = jieba.cut_for_search(sentence)
        for word in words:
            f.write("%s\n" %word)
    f.close()

if __name__ == "__main__":

    print("Now start cutter.py")
    jieba.load_userdict("./userdict.txt")
    
    chkDir(dicttextDir)
    chkDir(dicttitleDir)
    arr = [(rawtextDir, dicttextDir), (rawtitleDir, dicttitleDir)]
    
    for IN, OUT in arr:
        
        i = 0
        print("Now resolving: %s -> %s" % (IN, OUT))
        for filename in os.listdir(IN):
            # read
            try:
                f = open(IN + filename, mode = "r")
                text = f.read()
                f.close()
            except:
                print("Error found in:", filename, decrypt(filename))  
                
            # write
            cut_to_file(text = text, filename = OUT + filename)
            
            i += 1
            if(i % 100 == 0):
                print("%s%d"%("." * (40 - len(str(i))), i))
        
        print("Total: %d" % i)

print("[INFO] Loading LAC")
from LAC import LAC
lac = LAC(mode = 'seg')
lac.load_customization('../my_dict.txt', sep = '\n')
print("[INFO] LAC Loaded")
import pkuseg
tokenizer = pkuseg.pkuseg(model_name = 'medicine', user_dict= '../my_dict.txt')
print("[INFO] pkuseg Loaded")

# jieba
print("[INFO] Loading jieba")
import jieba
jieba.enable_paddle()
jieba.load_userdict('../my_dict.txt')
print("[INFO] Jieba loaded")

while True:
    s = input()
    a1 = lac.run(s)
    a2 = tokenizer.cut(s)
    a3 = jieba.lcut(s)
    a4 = jieba.lcut_for_search(s)
    print("lac:",a1)
    print("pku:",a2)
    print("jb1:",a3)
    print("jb2:",a4)
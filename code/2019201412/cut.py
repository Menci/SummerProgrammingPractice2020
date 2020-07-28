import jieba
import jieba.posseg as pseg

St = 1
End = 6883
while St <= End:
	T = ""
	filename = str(St) + 'ext.txt'
	print (St)
	with open(filename, "r") as f:
		words = pseg.cut(f.read(),use_paddle=False) #paddle模式
		for word, flag in words:
			if flag == 'x':
				continue
			if flag == "eng":
				continue
			T = T + '[' + word + ' ' + flag + ']'
#print('%s %s' % (word, flag))

		filename = str(St) + 'cut.txt';
		with open(filename, "w") as fw:
			fw.write(T)
	St = St + 1

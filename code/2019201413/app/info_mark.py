import re

punct = [",", ".", "?", "!", "\n" , "。", "，", "！", "？", " "]
file_path = 'app/source/'
debug_flag = 0

def cmp(x):
    return x[1]

def grab_single(stp, edp, data, maxlen):
    sp = stp
    ep = edp
    clen = ep - sp
    while sp > 0 and sp < len(data) and data[sp] not in punct:
        sp -= 1
    while ep > 0 and ep < len(data) and data[ep] not in punct:
        ep += 1
    if ep - sp > maxlen:
        sp = stp - maxlen // 2 + clen // 2
        ep = stp + maxlen // 2 - clen // 2
    if sp < 0:
        sp = 0
    while ep - sp < maxlen and ep - sp < len(data):
        if(ep < len(data)):
            ep += 1
        else:
            sp -= 1
    return data[sp:ep] + '...'

def split_by_str(src, cstr):
    result = []
    for i in range(len(src)):
        if i % 2 == 0:
            try:
                tmp = re.split(cstr, src[i])
                for j in range(len(tmp)):
                    result.append(tmp[j])
                    if j != len(tmp) - 1:
                        result.append(cstr)
            except:
                continue
        else:
            result.append(src[i])

    return result

def merge(clist):
    result = []
    flag = 0
    for i in range(len(clist)):
        if flag == 1:
            result[-1] += clist[i]
            flag = 0
        elif len(clist[i]) == 0:
            if i == 0:
                result.append(clist[i])
            else:
                flag = 1
        else:
            result.append(clist[i])
    return result


def mark_info(src, words, idf):
    result = []
    occur = {}
    page = open(file_path + 'parse_data/' + src, mode = 'r')
    data = page.read()
    
    datas = data.splitlines(keepends = False)
    data = ""
    for i in range(1, len(datas)):
        data += datas[i] + " "
    title = datas[0]
   
    stack = []
    words = sorted(set(words), key=len, reverse = True)
    for word in words:
        occur[word] = []
        try:
            for pos in re.finditer(word, data):
                occur[word].append(pos.span())
            if len(occur[word]) > 0:
                stack.append((word, idf.setdefault(word, 0)))
        except:
            continue

    position = []

    if len(stack) == 1:
        target = stack[0][0]
        for i in range(min(len(occur[word]), 3)):
            position.append(occur[word][i])
    else:
        stack.sort(key = cmp)
        if len(stack) >= 3:
            position.append(occur[stack[0][0]][0])
            position.append(occur[stack[1][0]][0])
            position.append(occur[stack[2][0]][0])
        elif len(stack) == 2:
            position.append(occur[stack[0][0]][0])
            position.append(occur[stack[1][0]][0])
            if len(occur[stack[0][0]]) >= 2:
                position.append(occur[stack[0][0]][1])
            elif len(occur[stack[1][0]]) >= 2:
                position.append(occur[stack[1][0]][1])
        elif len(stack) == 1:
            for i in range(min(3, len(occur[stack[0][0]]))):
                position.append(occur[stack[0][0]][i])
        else:
            print("[ERROR] No Positions")

    if debug_flag == 1:
        print("positions:")
        for i in position:
            print("(" + str(i[0]) + "," + str(i[1]) + ":" + data[i[0]:i[1]] + ")")

    if len(position) == 1:
        result.append(grab_single(position[0][0], position[0][1], data, 85))
        result = split_by_str(result, data[position[0][0]:position[0][1]])
    elif len(position) == 2:
        if abs(position[0][0] - position[1][0]) < 90:
            result.append(grab_single(min(position[0][0], position[1][0]), max(position[0][1], position[1][1]), data, 85))
        else:
            tmp = grab_single(position[0][0], position[0][1], data, 40)
            tmp += grab_single(position[1][0], position[1][1], data, 40)
            result.append(tmp)
    elif len(position) == 3:
        edp = max(position[0][1], max(position[1][1], position[2][1]))
        stp = min(min(position[0][0], position[1][0]), position[2][0])

        if edp - stp < 60:
            result.append(grab_single(stp, edp, data, 85))
        else:
            tmp = grab_single(position[0][0], position[0][1], data, 25)
            tmp += grab_single(position[1][0], position[1][1], data, 25)
            tmp += grab_single(position[2][0], position[2][1], data, 25)
            result.append(tmp)
    else:
        print("[ERROR] No Positions")

    titles = [title]
    for word in words:
        titles = split_by_str(titles, word)
        result = split_by_str(result, word)

    merge(titles)
    merge(result)

    return (titles, result, len(titles), len(result))

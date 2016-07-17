def average(l):
    if len(l) == 0:
        return 0
    else:
        s = l[0]
        for i in l:
            s += i
        return s / float(len(l))

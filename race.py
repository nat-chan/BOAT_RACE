import re

def is_num(s):
    return s.replace(',', '').replace('.', '').replace('-', '').isnumeric()

def to_time(s: str):
    tseq = s.split('.')
    i = 0.1
    t = 0
    for ti in reversed(tseq):
        t += int(ti) * i
        if i == 0.1:
            i *= 10
        else:
            i *= 60
    return t

def get_race_info(s: str):
    """
    example
    file-encoding = utf-8
    res = get_race_info("../race/2015/K150101.TXT")
    """
    with open(s, encoding='utf-8') as f:
        lines = f.readlines()
        i = -1
        res = []
        while True:
            i = i + 1
            if (i >= len(lines)):
                break
            if (lines[i].startswith('--------------')):
                r = []
                while True:
                    i = i + 1
                    if lines[i].startswith("  0"):
                        if  lines[i].endswith(" .  . "):
                            r = []
                            break
                        else:
                            base = lines[i].strip().replace('\u3000',
                                                            '_').split()
                            idx = base[2].strip()
                            time = base[-1].strip()
                            if idx.isdecimal() and is_num(time):
                                r.append([int(idx), to_time(time)])
                            else:
                                break
                    else:
                        break
                if (len(r) == 6):
                    res.append(r)
    return res

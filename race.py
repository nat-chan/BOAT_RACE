import re
from pathlib import Path

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
    ;; => res[0]
    ;; => [{'player_id': 4718, 'time': 106.6},
              {'player_id': 4661, 'time': 108.5},
              {'player_id': 4072, 'time': 110.3},
              {'player_id': 3471, 'time': 111.4},
              {'player_id': 3459, 'time': 112.6},
              {'player_id': 4724, 'time': 113.3}]
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
                        if lines[i].endswith(" .  . \n"):
                            r = []
                            break
                        else:
                            base = lines[i].strip().replace('\u3000',
                                                            '_').split()
                            idx = base[2].strip()
                            time = base[-1].strip()
                            if idx.isdecimal() and is_num(time):
                                r.append({"player_id": int(idx),
                                          "time":  to_time(time)})
                            else:
                                break
                    else:
                        break
                if (len(r) == 6):
                    res.append(r)
    return res


def __get_race_info_with_nan(s: str):
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
                        if lines[i].endswith(" .  . \n"):
                            r = []
                            base = lines[i].strip().replace('\u3000',
                                                            '_').split()
                            idx = base[2].strip()
                            if idx.isdecimal():
                                r.append([int(idx), -1.0])
                            else:
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


def get_race_info_with_dir(s: str, with_nan=False):
    """
    example
    files-encoding = utf-8
    res_nan = get_race_info_with_dir("../race/2015/", with_nan=False)
    """
    parent = Path(s)
    res = []
    for f in parent.iterdir():
        if with_nan:
            r = __get_race_info_with_nan(f)
            res.append(r)
        else:
            r = get_race_info(f)
            res.append(r)
    return res

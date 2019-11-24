import re
from pathlib import Path
import numpy as np
import pprint

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
    ;; => [[1, 106.6],
              [2, 108.5],
              [3, 110.3],
              [4, 111.4],
              [5 112.6],
              [6, 113.3]]

    ;; means:
    ;; => [{'rane': 1, 'time': 113.3}
               ...]
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
                            lane_idx = base[1].strip()
                            time = base[-1].strip()
                            if lane_idx.isdecimal() and is_num(time):
                                r.append([int(lane_idx), to_time(time)])
                            else:
                                break
                    else:
                        break
                if (len(r) == 6):
                    res.append(sorted(r, key=lambda x: x[0]))
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
            print("not implenmented")
            break
        else:
            r = get_race_info(f)
            res += r
    return res



def get_race_time_statics(res):
    arr = np.array(np.stack(res))
    assert arr.shape[1] == 6, 'race num is invalid'
    assert arr.shape[2] == 2, 'res size is invalid'
    return {"mean": np.mean(arr, axis=0)[:, 1],
            "var": np.var(arr, axis=0)[:, 1]}

def main(path: str = "../race/2015/"):
    res_year = get_race_info_with_dir(path)
    print("example information:")
    print("[[sorted_lane, time] x 6]")
    print(res_year[0])
    print("mean and variance")
    pprint.pprint(get_race_time_statics(res_year))
    return get_race_time_statics(res_year)

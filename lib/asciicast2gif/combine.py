import sys
import json
from os import listdir
from os.path import isfile, join


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def gen_metadata():
    lns = open("output.txt").readlines()[-2]
    b = lns.split(" ")[2:]
    prefix = b[:3]
    ending = b[-13:]
    x = b[3:-13]
    res = []
    for [a, b, c] in chunks(x, 3):
        pos = c.rindex("/")
        res.append([a, b, c[pos + 1 :]])
    delays = []
    for [_, delay, pos] in res:
        delays.append((delay, pos))

    print(
        json.dumps(
            {
                "prefix": prefix,
                "ending": ending,
                "delays": delays,
            }
        )
    )


def main():
    # todo: refactor!!!
    if len(sys.argv[1:]) < 1:
        print("At least one directory is required")
        sys.exit(1)

    _prefix_raw = open(f"{sys.argv[1:][0]}.cast_gif/output.json").read()
    first_data = json.loads(_prefix_raw)
    prefix = first_data["prefix"]
    ending = first_data["ending"]
    file_name = "-".join(sys.argv[1:])
    ending[-2] = f"./{file_name}.cast.gif"
    all_delays = []
    for f in sys.argv[1:]:
        mypath = f"{f}.cast_gif/"
        png_files = [
            int(f[:-4])
            for f in listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".png")
        ]
        png_files.sort()
        delays = open(f"{mypath}output.json").read()
        delays = json.loads(delays)["delays"]
        delays_origin = {int(png[:-4]): int(d) for [d, png] in delays}
        delays = update_delays(delays_origin, png_files)
        delays = [
            ["-delay", str(delays[pngf]), f"{f}.cast_gif/{pngf}.png"]
            for pngf in png_files
        ]
        if len(sys.argv[1:]) > 1 and delays[0][1] == 0:
            delays[0][
                1
            ] = 200  # delay of the first frame when there are multiple gif being combined
        all_delays.extend(delays)

    ending[-1] = ending[-1][:-1]  # removing the last \n character
    res = [prefix] + all_delays + [ending]
    flat_list = [item for sublist in res for item in sublist]
    print(" ".join(flat_list))


# print(delays)
def update_delays(l, n):
    res = [(n[0], l[n[0]])]
    i = 1
    while i < len(n):
        # es n[i] el siguiente a n[i-1]?
        if n[i] == n[i - 1] + 1:
            res.append((n[i], l[n[i]]))
        else:
            next_index = n[i - 1] + 1
            # print(f"i: {i}, next index: {next_index}")
            res.append((n[i], l[next_index]))
        i += 1
    return {a: b for (a, b) in res}

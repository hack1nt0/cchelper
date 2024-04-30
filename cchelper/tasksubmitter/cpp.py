from cchelper import *
from subprocess import run, Popen, PIPE


def extract_includes(cmd):
    I = []
    for i in range(len(cmd)):
        c = cmd[i]
        if c.startswith("-I"):
            if c == "-I":
                I.append(c[i + 1])
            else:
                I.append(c[2:])
    return I


def preprocess(
    fn,
):
    PP_CMD = File(fn).compile_cmd
    if isinstance(PP_CMD, str):
        PP_CMD = PP_CMD.split(' ')
    INCLUDES = extract_includes(PP_CMD)
    PP_CMD = [PP_CMD[0]]
    for I in INCLUDES:
        PP_CMD.append(f"-I{I}")
    PP_CMD += ["-E", "-x", "c++", "-"]
    logger.debug(' '.join(PP_CMD))
    lines = []
    std_headers = set()
    import re

    pat_header = re.compile(r'[ \t]*#include[ \t]*["<]([\w\\/\._]+)[>"]')

    def concat(fn):
        with open(fn, "r") as f:
            for line in f.readlines():
                m = pat_header.match(line)
                if m:
                    header = m.group(1)
                    is_custome_header = False
                    for i in INCLUDES:
                        nfn = os.path.join(i, *header.split("/"))
                        if os.path.exists(nfn) and os.path.isfile(nfn):
                            concat(nfn)
                            is_custome_header = True
                            break
                    # std headers
                    if is_custome_header == False:
                        std_headers.add(header)
                else:
                    line = line.replace('\t', ' '*4)
                    lines.append(line)
                    # Last line of file may not ends with newline
                    if not line.endswith("\n"):
                        lines.append("\n")

    concat(fn)

    # macro substitution (aka. after preprocessing)
    p = Popen(PP_CMD, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    p.stdin.writelines(lines)
    p.stdin.close()
    if p.wait():
        logger.exception(p.stderr.read())
        return
    raw = p.stdout.readlines()

    lines = []
    lines += map(lambda h: f"#include <{h}>\n", std_headers)
    i = 0
    n = len(raw)
    while i < n:
        if raw[i].strip() == "":
            while i < n:
                if raw[i].lstrip() == "":
                    i += 1
                    continue
                if raw[i].lstrip().startswith("//"):
                    i += 1
                    continue
                if raw[i].lstrip().startswith("#"):
                    i += 1
                    continue
                if raw[i].lstrip().startswith("/*"):
                    while i < n and raw[i].strip() != "*/":
                        i += 1
                    i += 1
                    continue
                break
            lines.append("\n")
            continue
        if raw[i].lstrip().startswith("//"):
            i += 1
            continue
        if raw[i].lstrip().startswith("#"):
            i += 1
            continue
        if raw[i].lstrip().startswith("/*"):
            while i < n and raw[i].strip() != "*/":
                i += 1
            i += 1
            continue
        lines.append(raw[i])
        i += 1
    return lines, raw

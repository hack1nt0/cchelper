import os
import shutil
import random, string

def data(*args) -> str:
    dn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    return os.path.join(dn, *args)

def img(img: str):
    return data('img', img)

def stash_dir(*args):
    return data('stash', *args)

def test(task, *args):
    return data('stash', task.name, 'T', *map(str, args))

def file(task, *args):
    return data('stash', task.name, 'F', *map(str, args))

def verdict(task, *args):
    return data('stash', task.name, 'V', *map(str, args))

def graph(*args):
    return data('graph', *args)
    
def clear(dn: str):
    if os.path.isdir(dn):
        for fn in os.listdir(dn):
            if os.path.isdir(fn):
                shutil.rmtree(fn)
            else:
                os.remove(fn)
    else:
        with open(dn, 'w') as w:
            pass #TODOa

def remove_symlink(link: str):
    try:
        if os.path.islink(link):
            os.unlink(link)  # TODO
        else:
            shutil.rmtree(link)
    except:
        pass

def random_dirname(parent: str, k=16):
    dns = {dn for dn in os.listdir(parent) if os.path.isdir(dn)}
    while True:
        dn = ''.join(random.choices(string.digits, k=k))
        if dn not in dns:
            return os.path.join(parent, dn)

def random_filename(parent: str, suffix: str='.txt', k=16):
    fns = {dn for dn in os.listdir(parent) if os.path.isfile(dn)}
    while True:
        fn = ''.join(random.choices(string.digits, k=k)) + suffix
        if fn not in fns:
            return os.path.join(parent, fn)


import requests
from bs4 import BeautifulSoup as bs
import re
from cchelper import *
from urllib.parse import urlparse
import os

session = requests.session()

parsers = {}


def parse(url):
    domain = urlparse(url).netloc
    return parsers[domain](url)


def remove_spaces(s):
    return "".join(filter(lambda c: not c.isspace(), s))


def parse_leetcode(raw_url) -> List[Task]:
    URL_FORMAT = "https://leetcode.(com|cn)/problems/xxx"
    API_URL = "https://leetcode.com/graphql"
    task = Task()
    # problem_page = session.get(url)
    # soup = bs(problem_page.text, "html.parser")
    # title = remove_spaces(soup.find("title").text.split("-")[0])
    # task.name = f"LeetCode-{title}"
    # desc = soup.find("meta", {"name": "description"}).attrs["content"]
    # task.tests = []
    # sample_pattern = r"输入：`(.+?)`.*?输出：`(.+?)`"
    # for id, m in enumerate(re.finditer(sample_pattern, desc)):
    #     I, O = map(lambda s: s.strip(), m.groups())
    #     tst = Test(
    #         id=id,
    #         status=VS.QUE,
    #         input_type=IT.MANUAL,
    #         input=I,
    #         answer_type=AT.MANUAL,
    #         answer=O,
    #     )
    #     task.tests.append(tst)
    url = urlparse(raw_url)
    path = [x for x in url.path.split("/") if x]
    if len(path) < 2:
        logger.error(f"Url format error: {URL_FORMAT}")
        return
    title_inurl = path[1]
    payload = (
        '{"query":"query xx($titleSlug: String!) {\\n            question(titleSlug: $titleSlug) {\\n                questionId\\n                title\\n                exampleTestcaseList\\n                codeSnippets {\\n                    lang\\n                    code\\n        }\\n    }\\n}","variables":{"titleSlug":"'
        + title_inurl
        + '"}}'
    )
    headers = {
        "Content-Type": "application/json",
        # "Cookie": "csrftoken=7GSbE6RgfaFUuwNMtkKAvlXZibvtdwcBGObPsIyXz3tSxQIRY2gC7Zot56Clxtzd",
    }
    r = session.post(API_URL, headers=headers, data=payload, timeout=conf.crawl_timeout)
    r = r.json()
    title = (
        "LeetCode/"
        + r["data"]["question"]["questionId"]
        + "."
        + "".join(r["data"]["question"]["title"].split())
    )
    tests = r["data"]["question"]["exampleTestcaseList"]
    codes = r["data"]["question"]["codeSnippets"]
    task.name = title
    task.url = f"{url.scheme}://{url.netloc}/{'/'.join(path[:2])}"

    for idx, old in enumerate(tests):
        new = Test()
        new.id = idx
        new.checked = True
        new.status = VS.QUE
        new.input_type = IT.MANUAL
        new.input = old
        new.answer_type = AT.MANUAL
        new.answer = ""
        task.tests.append(new)
    prefer_lang = conf.prefer_lang.name
    task.solver = [code["code"] for code in codes if code["lang"] == prefer_lang][0]
    return [task]


# pat = r'输入：`(.+?)`.*?输出：`(.+?)`'
# txt = '输入：`1`.*输出：`1`  输入：`2`.*输出：`2`   输入：`2`.*输出：`2`   '
# for m in re.finditer(pat, txt):
#     print(m.groups())
parsers["leetcode.com"] = parse_leetcode
parsers["leetcode.cn"] = parse_leetcode

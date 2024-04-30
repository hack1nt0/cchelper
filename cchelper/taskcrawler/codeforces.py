import requests
from bs4 import BeautifulSoup as bs
import argparse
import os

CF_DOMAIN = 'https://codeforces.com'
session = requests.session()

def parse_contest(contest_id):
    contest_page = session.get(f'{CF_DOMAIN}/contest/{contest_id}')
    soup = bs(contest_page.text, "html.parser")
    contest_name = cc.str_shrink(soup.find('table', class_='rtable').find('a').text)
    print(contest_name)
    contest_dir = os.path.join(os.path.dirname(cc.__file__), 'codeforces', contest_id)
    os.makedirs(contest_dir, exist_ok=True)
    os.chdir(contest_dir)
    problems = soup.find('table', class_='problems').find_all('tr')[1:]
    
    for p in problems:
        cols = p.find_all('td')
        problem_link = CF_DOMAIN + cols[0].a.get('href')
        problem_name = cc.str_shrink(cols[0].a.text.strip() + ' ' + cols[1].a.text.strip())
        problem_id = cc.str_shrink(cols[0].a.text.strip()).lower()
        problem_dir = os.path.join(contest_dir, problem_id)
        os.makedirs(problem_dir, exist_ok=True)
        print(problem_name)
        parse_problem(problem_dir, problem_link)
    print(f'Total {len(problems)} probs.')

def parse_problem(problem_dir, problem_link):
    problem_page = session.get(problem_link)
    soup = bs(problem_page.text, "html.parser")
    sample = soup.find('div', class_='sample-test')
    def parse_sample(tags):
        txts = []
        for tag in tags:
            txt = '\n'.join(map(lambda div: div.text.strip(), tag.pre.find_all('div')))
            if len(txt) == 0:
                txt = tag.pre.text.strip()
            txts.append(txt)
        txts = '\n\n'.join(txts)
        return txts
    
    sample_in = parse_sample(sample.find_all('div', class_='input'))
    sample_out = parse_sample(sample.find_all('div', class_='output'))
    
    source_file = cc.cpp_source_file(problem_dir)
    if os.path.exists(source_file):
        return False
    with open(source_file, 'w') as f:
        f.write('''
#include "allinone.h"

void run(int it) {
}

int main() {
    int nt; cin >> nt;
    for (int it = 1; it <= nt; ++it) run(it);
}

        '''.strip())
    with open(cc.sample_in_file(source_file), 'w') as f:
        f.write(sample_in)
    with open(cc.sample_out_file(source_file), 'w') as f:
        f.write(sample_out)
    return True

# if __name__ == '__main__':
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('contest_id')
    args = parser.parse_args()
    parse_contest(args.contest_id)

'''get origin pubmed article text according to its pubmed id'''

import requests
import json
import codecs


def get_text_by_id(idx):
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term= %s &report=xml&format=text' % idx
    r = requests.get(url)
    data = r.text
    data = data.replace('&lt;', '<')
    data = data.replace('&gt;', '>')
    title_begin_index = data.find('<ArticleTitle>')
    title_end_index = data.find('</ArticleTitle>')
    title = ''
    abstract = ''
    if title_begin_index != -1 and title_end_index != -1:
        title = data[title_begin_index + len('<ArticleTitle>') : title_end_index]
    abstract_begin_index = data.find('<AbstractText')
    abstract_end_index = data.find('/AbstractText>')
    if abstract_begin_index != -1 and abstract_end_index != -1:
        abstract = data[abstract_begin_index + len('<AbstractText') : abstract_end_index - 1]
    return title + abstract


def load_json_data(file_name):
    with open (file_name, 'r') as f:
        data = json.load(f)
    return data


def generate_file(in_file, out_file, json_data):
    temp_dict = {}
    for i in range(len(json_data['questions'])):
        idx = json_data['questions'][i]['id']
        text = json_data['questions'][i]['body']
        temp_dict[idx] = text

    of = codecs.open(out_file, 'w', encoding='utf8')
    with codecs.open (in_file, 'r', encoding='utf8') as f:
        for line in f:
            if not line:
                break
            line = line.split('\t')
            if len(line) == 3:
                doc_id = line[2].strip('\n')
                qtext = temp_dict[line[1]]
                dtext = get_text_by_id(doc_id)
                dtext = dtext.strip('\n')
                of.write(line[0] + '<<-->>' + line[1] + '<<-->>' + qtext + '<<-->>' + doc_id + '<<-->>' + dtext + '\n')
            print(line[1])
    of.close()


if __name__ == '__main__':
   src_dir = './'
   dst_dir = './'
   input_json_file = 'phaseA_6b_05.json'
   input_file = 'relation_6b_05_trec.txt'
   out_file = dst_dir + 'temp6b05.txt'
   json_data = load_json_data(src_dir + 'source_data/' + input_json_file)
   print("begin to generate relation file...")
   generate_file(input_file, out_file, json_data)
   print("Done...")

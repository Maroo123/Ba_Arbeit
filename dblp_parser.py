from lxml import etree
from datetime import datetime
import csv
import codecs
import ujson
import re
import json
# all of the element types in dblp
all_elements = {"article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www"}
# all of the feature types in dblp
all_features = {"address", "author", "booktitle", "cdrom", "chapter", "cite", "crossref", "editor", "ee", "isbn",
                "journal", "month", "note", "number", "pages", "publisher", "school", "series", "title", "url",
                "volume", "year"}


def log_msg(message):
    """Produce a log with current time"""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)


def context_iter(dblp_path):
    """Create a dblp data iterator of (event, element) pairs for processing"""
    return etree.iterparse(source=dblp_path, dtd_validation=True, load_dtd=True, events=('end',))  # required dtd


def clear_element(element):
    """Free up memory for temporary element tree after processing the element"""
    element.clear()
    while element.getprevious() is not None:
        del element.getparent()[0]



def parse_entity(dblp_path, save_path, type_name, features=None, save_to_csv=False, include_key=False):
    """Parse specific elements according to the given type name and features"""
    log_msg("PROCESS: Start parsing for {}...".format(str(type_name)))
    assert features is not None, "features must be assigned before parsing the dblp dataset"
    results = []
    attrib_count, full_entity, part_entity = {}, 0, 0
    for _, elem in context_iter(dblp_path):
        if elem.tag in type_name:
            attrib_values = extract_feature(elem, features, include_key)  # extract required features
            results.append(attrib_values)  # add record to results array
            for key, value in attrib_values.items():
                attrib_count[key] = attrib_count.get(key, 0) + len(value)
            cnt = sum([1 if len(x) > 0 else 0 for x in list(attrib_values.values())])
            if cnt == len(features):
                full_entity += 1
            else:
                part_entity += 1
        elif elem.tag not in all_elements:
            continue
        clear_element(elem)
    if save_to_csv:
        f = open(save_path, 'w', newline='', encoding='utf8')
        writer = csv.writer(f, delimiter=',')
        writer.writerow(features)  # write title
        for record in results:
            # some features contain multiple values (e.g.: author), concatenate with `::`
            row = ['::'.join(v) for v in list(record.values())]
            writer.writerow(row)
        f.close()
    else:  # default save to json file
        with codecs.open(save_path, mode='w', encoding='utf8', errors='ignore') as f:
            ujson.dump(results, f)
    return full_entity, part_entity, attrib_count

def parse_author2(dblp_path):
    type_name = ['article', 'book', 'incollection', 'inproceedings']
    documents = []

    for event, elem in context_iter(dblp_path):
        if elem.tag in type_name:
            key = elem.get('key')
            year = elem.findtext('year')
            if key and year:  # Überprüfen Sie, ob key und year vorhanden sind
                document_dict = {'key': key, 'year': year}
                documents.append(document_dict)

            # Bereinigen Sie das Element, um Speicher freizugeben
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    json_file_path = 'year_dataset.json'
    with open(json_file_path, 'w', encoding='utf8') as json_file:
        json.dump(documents, json_file, ensure_ascii=False)

    log_msg("PROCESS: Completed parsing and saved to JSON.")

def parse_author(dblp_path):
    type_name = ['article', 'book', 'incollection', 'inproceedings','year']
    log_msg("PROCESS: Start parsing for {}...".format(str(type_name)))
    authors = set()
    step = 0
    list = []
    document_dict={}
    for _, elem in context_iter(dblp_path):
        if elem.tag in type_name:
            #authors.update(a.text for a in elem.findall('author'))
            document_dict = {
                'key': elem.get('key'),
                #'authors': [author.text for author in elem.findall('author')]
                'year': elem.findtext('year')
            }
                # Add other fields as needed
        elif elem.tag not in all_elements:
            document_dict={}
            continue
        list.append(document_dict)
        clear_element(elem)
    #print(list)
    json_file_path = 'year_dataset.json'
    with open(json_file_path, 'w', encoding='utf8') as json_file:
        json.dump(list, json_file, ensure_ascii=False)
    """if save_to_csv:
        f = open(save_path, 'w', newline='', encoding='utf8')
        writer = csv.writer(f, delimiter=',')
        writer.writerows([a] for a in authors)
        f.close()
    else:
        with open(save_path, 'w', encoding='utf8') as f:
            f.write('\n'.join(sorted(authors)))"""
    log_msg("FINISHED...")
"""def parse_author(dblp_path, save_path, save_to_csv=True):
    type_name = ['article', 'book', 'incollection', 'inproceedings']
    log_msg("PROCESS: Start parsing for {}...".format(str(type_name)))
    authors = set()
    step = 0
    for _, elem in context_iter(dblp_path):
        if step >= 20:
            break
        elif elem.tag in type_name:
            #authors.update(a.text for a in elem.findall('author'))
            list=[]
            for a in elem.findall('author'):
                list.extend([a.text])
                authors.update(a.text)
                step += 1
            print(list)
        elif elem.tag not in all_elements:
            continue
        clear_element(elem)
    if save_to_csv:
        f = open(save_path, 'w', newline='', encoding='utf8')
        writer = csv.writer(f, delimiter=',')
        writer.writerows([a] for a in authors)
        f.close()
    else:
        with open(save_path, 'w', encoding='utf8') as f:
            f.write('\n'.join(sorted(authors)))
    log_msg("FINISHED...")"""
"""def parse_author_list(dblp_path, save_path, save_to_csv=True):
    type_name = ['article', 'book', 'incollection', 'inproceedings']
    log_msg("PROCESS: Start parsing for {}...".format(str(type_name)))
    authors = set()
    step = 0
    for _, elem in context_iter(dblp_path):
        if step >= 100:
            break
        elif elem.tag in type_name:
            authors.update(a.text for a in elem.findall('author'))
            print(authors)
            step += 1
        elif elem.tag not in all_elements:
            continue
        clear_element(elem)
    if save_to_csv:
        f = open(save_path, 'w', newline='', encoding='utf8')
        writer = csv.writer(f, delimiter=',')
        writer.writerows([a] for a in authors)
        f.close()
    else:
        with open(save_path, 'w', encoding='utf8') as f:
            f.write('\n'.join(sorted(authors)))
    log_msg("FINISHED...")"""





def main():
    dblp_path = 'dataset/dblp.xml'
    save_path = 'dataset/article.json'
    try:
        context_iter(dblp_path)
        log_msg("LOG: Successfully loaded \"{}\".".format(dblp_path))
    except IOError:
        log_msg("ERROR: Failed to load file \"{}\". Please check your XML and DTD files.".format(dblp_path))
        exit()
    parse_article(dblp_path, save_path, save_to_csv=False)


if __name__ == '__main__':
    main()

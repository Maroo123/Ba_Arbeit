# This is a sample Python script.
from dblp_parser import log_msg, context_iter, parse_article, parse_author, parse_author2

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import xml.etree.ElementTree as ET

import networkx as nx
import matplotlib.pyplot as plt
import community  # Dies ist die python-louvain Bibliothek

xml_file_path = "Bachelorarbeit\DBLP\dblp.xml"

# Path to your local DTD file
dtd_file_path = "Bachelorarbeit\DBLP\dblp.dtd"
import json


def main():
    """  dblp_path = 'dblp.xml'
    save_path = 'article.json'
    try:
        context_iter(dblp_path)
        log_msg("LOG: Successfully loaded \"{}\".".format(dblp_path))
    except IOError:
        log_msg("ERROR: Failed to load file \"{}\". Please check your XML and DTD files.".format(dblp_path))
        exit()
    parse_article(dblp_path, save_path, save_to_csv=False)"""

    dblp_path = 'dblp.xml'
    # save_path = 'author.json'
    save_path = 'article.csv'
    # Open the CSV file in write mode, which will clear its content
    with open(save_path, 'w', newline='') as csv_file:
        pass
    try:
        context_iter(dblp_path)
        log_msg("LOG: Successfully loaded \"{}\".".format(dblp_path))
    except IOError:
        log_msg("ERROR: Failed to load file \"{}\". Please check your XML and DTD files.".format(dblp_path))
        exit()
    parse_author2(dblp_path, save_path, save_to_csv=True)


if __name__ == '__main__':
    main()

# main()
# Parse the DBLP XML file

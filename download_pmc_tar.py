import requests
import re
import wget
import os

def download_PMC_OA_file(pmc_id):
    response = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id="+pmc_id)
    response = response.text
    tar_href = re.search(r'<link\sformat=\"tgz\"\supdated=\".+?\"\shref=\"(.+?)\"', response)
    tar_href = tar_href.group(1)
    if(tar_href):
        print(pmc_id, tar_href)
        wget.download(tar_href)
    else:
        print(pmc_id, "Not Found")

def execute_download(ids_list_filename):
    ids_list_file = open(ids_list_filename, "r")
    os.mkdir("PMC_downloads")
    os.chdir("PMC_downloads")
    for line in ids_list_file:
        line = line.rstrip()
        download_PMC_OA_file(line)
    ids_list_file.close()

execute_download("PMC_ids_list.txt")





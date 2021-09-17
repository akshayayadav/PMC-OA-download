import requests
import re
import wget
import os
import time
from ftplib import FTP

def download_PMC_OA_file(pmc_id):
    response = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id="+pmc_id)
    response = response.text
    tar_href = re.search(r'<link\sformat=\"tgz\"\supdated=\".+?\"\shref=\"(.+?)\"', response)
    if (tar_href):
        tar_href = tar_href.group(1)
        print(pmc_id, tar_href)
        dir_path, file_name = process_tar_href(tar_href)
        while 1:
            return_flag = write_local_ftp_file(dir_path, file_name)
            if return_flag == 0:
                break
            print(file_name, "Error encountered in writing file. Trying again ...")
            time.sleep(5)

        #wget.download(tar_href)
    else:
        print(pmc_id, response)

def process_tar_href(href):
    href_arr = re.split(r'/', href)
    dir_path = '/'.join(href_arr[3:8])
    file_name = href_arr[8]
    return [dir_path, file_name]

def write_local_ftp_file(dir_path, file_name):
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    ftp.cwd(dir_path)
    file_name_ftp_size = ftp.size(file_name)
    print(file_name, file_name_ftp_size)
    attempt_counter = 1
    while 1:
        print(file_name, "Downloading attempt ", str(attempt_counter))
        try:
            with open(file_name, 'wb') as fp:
                ftp.retrbinary('RETR '+file_name, fp.write)
            fp.close()
        except:
            os.remove(file_name)
            return 1
        file_name_download_size = os.path.getsize(file_name)
        if file_name_download_size == file_name_ftp_size:
            break
        os.remove(file_name)
        attempt_counter += 1
        time.sleep(5)
    ftp.quit()
    return 0


def execute_download(ids_list_filename):
    ids_list_file = open(ids_list_filename, "r")

    if not os.path.isdir("PMC_downloads"):
        os.mkdir("PMC_downloads")
    os.chdir("PMC_downloads")
    for line in ids_list_file:
        line = line.rstrip()
        download_PMC_OA_file(line)
        time.sleep(5)

    ids_list_file.close()

execute_download("PMC_ids_list.txt")

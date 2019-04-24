# Modified from this StackOverflow answer: https://stackoverflow.com/a/39225039
import os
import requests
import time
import zipfile

import gdc19

def _download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    _save_response_content(response, destination)

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def _save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)



def download_data():
    # https://drive.google.com/file/d/1imG1OKlgBYEMb6p-T5mdUH76mGyNdHsE
    file_id = '1imG1OKlgBYEMb6p-T5mdUH76mGyNdHsE'
    destination = os.path.join(gdc19.USER_DATA_PATH, 'data_archive.zip')
    if os.path.exists(destination):
        print('Data already downloaded to: {}'.format(gdc19.USER_DATA_PATH))
    else:
        print('Download data package... ')
        start = time.time()
        _download_file_from_google_drive(file_id, destination)
        end = time.time()
        print('Done.')
        print('Downloaded data in {:.3f} seconds'.format(end - start))
        # Decompress data
        print('Decompressing data package... ')
        start = time.time()
        zip_ref = zipfile.ZipFile(destination, 'r')
        zip_ref.extractall(gdc19.USER_DATA_PATH)
        zip_ref.close()
        end = time.time()
        print('Done.')
    return gdc19.set_data_directory(os.path.join(gdc19.USER_DATA_PATH, 'PUBLIC_DATA'))

import requests
import threading
import urllib.parse
import os
import time
def concatenate_parts(filename):
    part_files = [f"{filename}.part{i}" for i in range(6)]
    with open(filename, 'wb') as f:
        for part_file in part_files:
            with open(part_file, 'rb') as pf:
                f.write(pf.read())

def download_part(url, start, end, filename):
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
def download_file(url):
    filename = urllib.parse.urlparse(url).path.split('/')[-1]
    num_threads = 6

    file_size = int(requests.head(url).headers['Content-Length'])
    part_size = file_size // num_threads
    threads = []
    file_size = int(requests.head(url).headers['Content-Length'])
    part_size = file_size // num_threads

    start_time = time.time()
    for i in range(num_threads):
        start = i * part_size
        end = start + part_size - 1
        if i == num_threads - 1:
            end = file_size - 1
        thread_args = {
            'url': url,
            'start': start,
            'end': end,
            'filename': f'{filename}.part{i}'
        }

        thread = threading.Thread(target=download_part, kwargs=thread_args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    concatenate_parts(filename)
    print("Download complete!")

    end_time = time.time()
    download_time = end_time - start_time
    print(f"Download complete! Download time: {download_time:.2f} seconds, File Size: {file_size:.2f} megabytes")


    part_files = [f"{filename}.part{i}" for i in range(num_threads)]
    for part_file in part_files:
        os.remove(part_file)

if "__name__" == "__main__":
    url = input("Enter the URL: ")
    download_file(url)
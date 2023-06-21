from typing import List
from Watcher import Watcher
import os

"""
Define a key that unique identifies a filename of a certain type. 
For example: *youtube*.csv, the word youtube defines a file of type youtube 
and no other type of file will contain youtube in the name
"""


proc_dirs = {
    'spark_master': 'spark://spark-master:7077',
    'spotify': {
        'hdfs': 'hdfs://namenode:9000/user/data/spotify',
        'pyspark_file': './watcher/upload/spotify.py'
    },

    'youtube': {
        'hdfs': 'hdfs://namenode:9000/user/data/youtube',
        'pyspark_file': './watcher/upload/youtube.py'
    }
}

redirect = '>/dev/null'


def cmd_return_val(cmd: str) -> bool:
    # If command executed successfully then return val is 0
    return os.system(cmd) == 0


def upload_to_hdfs2(file: str, local_path: str, hdfs_path: str) -> bool:
    cmd = f'hdfs dfs -mv {local_path}/{file} {hdfs_path}/{file}'
    print(f'Executing: {cmd}')
    return cmd_return_val(f'{cmd} {redirect}')


def upload_to_hdfs(file: str, local_path: str, hdfs_path: str) -> bool:
    cmd = f'hdfs dfs -copyFromLocal {local_path}/{file} {hdfs_path}/{file}'
    print(f'Executing: {cmd}')
    return cmd_return_val(f'{cmd} {redirect}')


def remove_from_local(file: str, path: str) -> bool:
    cmd = f'rm {path}/{file}'
    print(f'Executing: {cmd}')
    return cmd_return_val(f'{cmd} {redirect}')


def save_to_hive(hdfs_dir: str, filename: str, pyfile: str, master_url: str) -> bool:
    cmd = f'spark-submit --master {master_url} {pyfile} {hdfs_dir} {filename}'
    print(f'Executing: {cmd}')
    return cmd_return_val(f'{cmd} {redirect}')


def process_files(files: List[str], path: str):
    for file in files:
        print(f'Processing file: {file}')
        has_key = False
        for key in proc_dirs:
            if key in file:
                has_key = True
                if upload_to_hdfs(file, path, proc_dirs[key]['hdfs']) and \
                        remove_from_local(file, path) and \
                        save_to_hive(proc_dirs[key]['hdfs'], file, proc_dirs[key]['pyspark_file'], proc_dirs['spark_master']):
                    print(f'File {file} processed correctly')
                else:
                    print(f'Unable to process: {file}')
                break

        if not has_key:
            print(f'There are any key associated for the file: {file}')


if __name__ == "__main__":
    file_watcher = Watcher(sleep_time=5, callback=process_files)
    file_watcher.watch()

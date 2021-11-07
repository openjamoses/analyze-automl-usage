import csv
import json
import os
import glob
import sys

INPUT_FILE_SEARCH = "./data/imports/imports@*.json"
OUTPUT_FILE_PATH = "./data/csv/imports.csv"
IMPORT_FIELD_NAMES = [
    "file",
    "file_in_repo",
    "repo",
    "repo_version",
    "name",
    "asname",
    "module"
]
def load_file(file_path):
    with open(file_path, 'r') as f:
        json_contents = json.load(f)
    return json_contents

class ImportJson:
    def __init__(self, ROOT_DIR):
        path_output = ROOT_DIR + '/data/csv/'
        if not os.path.exists(ROOT_DIR + '/data/csv'):
            os.makedirs(ROOT_DIR + '/data/csv')

        print ('System version: ', sys.version_info[0])
        if not os.path.exists(path_output + 'imports_details.csv'):

            if sys.version_info[0] < 3:
                data_file = open(path_output + 'imports_details.csv', mode='w')
            else:
                data_file = open(path_output + 'imports_details.csv', mode='w', newline='', encoding='utf-8')
            self.data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.data_writer.writerow(['repos', 'repo_version','file', 'file_in_repo', 'name', 'asname', 'module'])
        else:
            if sys.version_info[0] < 3:
                data_file = open(path_output + 'imports_details.csv', mode='a+')
            else:
                data_file = open(path_output + 'imports_details.csv', mode='a+', newline='', encoding='utf-8')
            self.data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    def export(self, file_path):
        result = list()
        contents = load_file(file_path)
        #print ('Imports:', contents)
        #file_name = contents['file']
        repo = contents['repo']
        repo_version = contents['repo_version']
        for obj in contents['imports']:
            #i['file'] = contents['file']
            #i['file_in_repo'] = contents['file_in_repo']
            #i['repo'] = contents['repo']
            #i['repo_version'] = contents['repo_version']
            obj = eval(str(obj))
            row = [repo, repo_version, contents['file'], contents['file_in_repo'], obj['name'], obj['asname'], obj['module']]
            self.data_writer.writerow(row)
            result.append(row)
        #print ('Almost DONE...!!!!')
        #for row in result:
        #    self.data_writer.writerow(row)
        return result
class FunctionCallsJson:
    def __init__(self, ROOT_DIR):
        path_output = ROOT_DIR + '/data/csv/'
        if not os.path.exists(ROOT_DIR + '/data/csv'):
            os.makedirs(ROOT_DIR + '/data/csv')
        if not os.path.exists(path_output + 'function_calls_details.csv'):
            if sys.version_info[0] < 3:
                data_file = open(path_output + 'function_calls_details.csv', mode='w')
            else:
                data_file = open(path_output + 'function_calls_details.csv', mode='w', newline='', encoding='utf-8')
            self.data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.data_writer.writerow(['repos', 'repo_version','file', 'file_in_repo', 'name', 'parent_function'])
        else:
            if sys.version_info[0] < 3:
                data_file = open(path_output + 'function_calls_details.csv', mode='a+')
            else:
                data_file = open(path_output + 'function_calls_details.csv', mode='a+', newline='', encoding='utf-8')
            self.data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    def export(self, file_path):
        result = list()
        contents = load_file(file_path)
        #print ('Import function calls:', type(contents), contents)
        for obj in contents:
            '''result.append({
                "file": c['file'],
                "file_in_repo": c['file_in_repo'],
                "repo": c['repo'],
                "repo_version": c['repo_version'],
                "name": c['name'],
                "parent_function": c['parent_function']
            })'''
            obj = eval(str(obj))
            self.data_writer.writerow([obj['repo'], obj['repo_version'], obj['file'], obj['file_in_repo'], obj['name'], obj['parent_function']])
        #print ('DONE...!!!!')
        return result

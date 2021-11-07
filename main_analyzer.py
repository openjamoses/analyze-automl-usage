import argparse
import csv
import os

from utils.export_json_to_csv import ImportJson, FunctionCallsJson
from utils.file_manager import FileManager
from parser.parse_functioncall import CollectFunctionCalls
from parser.parse_import import ParseImports

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', help="search directory")
parser.add_argument('-r', '--repo', help="repo org/name")
parser.add_argument('-v', '--repoversion', help="repo version")
parser.add_argument('-t', '--testing', help="run as testing", nargs="?", const="tangent")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main_analyzer(repo_dir, repo_name, repo_version, automl_configs, save_json=True):
    if not os.path.exists(ROOT_DIR+'/data'):
        os.makedirs(ROOT_DIR+'/data')
    OUTPUT_DIR = ROOT_DIR+'/data/'

    py_files = FileManager.list_project_py_files(repo_dir)
    ml_library_py_files = FileManager.list_files_that_import_automl_configs(py_files, repo_dir, repo_name, repo_version, automl_config_list=automl_configs)
    #print ('Success!')
    importJson = ImportJson(ROOT_DIR=ROOT_DIR)
    functionCallsJson = FunctionCallsJson(ROOT_DIR)
    for file in ml_library_py_files:
        file_path_in_repo = file[len(repo_dir) + 1:]
        source = FileManager.read_file_source(file)
        try:
            imports_parser = ParseImports(
                source,
                file,
                repo_name,
                repo_version,
                OUTPUT_DIR,
                file_path_in_repo,
                automl_configs=None
            )
            imports_parser.parse()
            json_path = imports_parser.write_to_json()
            try:
                importJson.export(json_path)
            except Exception as e:
                print ('Error in exporting: ', e)
        except Exception as e:
            print("Error Parsing Imports {}--{}--{}, Error name={} ".format(repo_name, repo_version, file_path_in_repo, e))

        try:
            collector = CollectFunctionCalls(
                file,
                repo_name,
                repo_version,
                source,
                OUTPUT_DIR,
                file_path_in_repo
            )
            collector.find_all()
            json_path = collector.export_to_json()
            try:
                functionCallsJson.export(json_path)
            except Exception as e:
                print ('Error in exporting: ', e)

        except Exception as e:
            print("Error Parsing Imports {}--{}--{}, Error name={}".format(repo_name, repo_version, file_path_in_repo, e))
    if save_json == False:
        FileManager.remove_clone(OUTPUT_DIR+'imports')
        FileManager.remove_clone(OUTPUT_DIR + 'fcalls')
def exit_if_invalid_args(args):
    if args.dir is None or os.path.isfile(args.dir):
        raise SystemExit("ERROR: -d --dir arg should be directory.")
    if args.repo is None:
        raise SystemExit("ERROR: -r --repo arg should be repo org/name.")
    if args.repoversion is None:
        raise SystemExit("ERROR: -v --repoversion arg should be repo release version.")
def main():
    args = parser.parse_args()
    exit_if_invalid_args(args)
    repo_dir = os.path.abspath(args.dir)
    repo_name = args.repo
    repo_version = args.repoversion
    main_analyzer(repo_dir, repo_name, repo_version)
if __name__ == "__main__":
    main()
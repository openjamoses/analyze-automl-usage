import os
import shutil

from parser.find_automl_config_imports import FindAutomlImports


class FileManager:
    @staticmethod
    def list_project_py_files(directory):
        directory = os.path.abspath(directory)
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(directory):
            docker_files = list()
            for file in filenames:
                if file.endswith('.py'):
                    docker_files.append(os.path.join(dirpath, file))
            list_of_files.extend(docker_files)
        return list_of_files

    @staticmethod
    def read_file_source(file):
        try:
            source = open(file, "r")
            return source.read()
        except Exception:
            print("The file doesn't exist or it isn't a Dockerfile ...", file)
            #raise SystemExit("The file doesn't exist or it isn't a Dockerfile ...", file)

    @staticmethod
    def get_file_contents(files):
        dict_file_contents = {}
        for file in files:
            try:
                source = open(file, "r").read()

                dict_file_contents[file] = source
            except Exception:
                print("The file doesn't exist or it isn't a Dockerfile...", file)
                #raise SystemExit("The file doesn't exist or it isn't a Dockerfile...", file)

            #docker_parser = Parser()

            #docker_parser.content = source.read()
            #result.extend(docker_parser.json)
        return dict_file_contents
    @staticmethod
    def list_files_that_import_automl_configs(py_files, repo_dir, repo_name, repo_version, automl_config_list=['automl']):
        result = list()
        for file in py_files:
            try:
                source = open(file, "r")
            except Exception:
                #raise SystemExit("The file doesn't exist or it isn't a Python script ...", file)
                print("The file doesn't exist or it isn't a Python script ...", file)

            try:
                imports_finder = FindAutomlImports(source.read(), file, automl_config_list)
                imports_finder.parse()
                if imports_finder.imports_automl_config:
                    result.append(file)
            except Exception as e:
                file_path_in_repo = file[len(repo_dir) + 1:]
                print("Error Parsing {}--{}--{}. error: {}".format(repo_name, repo_version, file_path_in_repo, e))
        return result

    @staticmethod
    def remove_clone(repo_root):
        ## Try to remove tree; if failed show an error using try...except on screen
        try:
            shutil.rmtree(repo_root)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
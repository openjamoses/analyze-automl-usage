import ast
import os
import json

class ParseImports:
    def __init__(self, source, file, repo, version, output_dir, file_path_in_repo, automl_configs=None):
        self.source = source
        self.abs_file = file
        self.file_path_in_repo = file_path_in_repo
        self.file = os.path.basename(self.abs_file)
        self.repo = repo
        self.version = version
        self.output_dir = output_dir
        self.automl_configs = automl_configs
        self.imports = list()
        self.list_of_automl_related_imports=[]
        self.list_of_all_imports = []

        if not os.path.exists(self.output_dir+'imports'):
            os.makedirs(self.output_dir+'imports')
    # def parse(self):
    #     tree = ast.parse(self.source)
    #     tree_body = tree.body
    #     for item in tree_body:
    #         if isinstance(item, ast.Import):
    #             for i in item.names:
    #                 if self.automl_configs is None or i.name in self.automl_configs:
    #                     new_import = dict()
    #                     new_import['name'] = i.name
    #                     new_import['asname'] = i.asname
    #                     new_import['module'] = None
    #                     self.imports.append(new_import)
    #         if isinstance(item, ast.ImportFrom):
    #             if item.level > 0:
    #                 # Relative imports
    #                 continue
    #             if self.automl_configs is None or item.module in self.automl_configs:
    #                 for i in item.names:
    #                     new_from_import = dict()
    #                     new_from_import['name'] = i.name
    #                     new_from_import['asname'] = i.asname
    #                     new_from_import['module'] = item.module
    #                     self.imports.append(new_from_import)

    def parse(self):
        tree = ast.parse(self.source)
        tree_body = tree.body
        self.list_of_all_imports = []
        for item in tree_body:
            # get the names after import
            if isinstance(item, ast.Import):
                for i in item.names:
                    all_imports = dict()
                    all_imports['name'] = i.name
                    # print("i.name is:",i.name)
                    all_imports['asname'] = i.asname
                    # print("asname: ", i.asname)
                    all_imports['module'] = self.get_module(item)
                    self.list_of_all_imports.append(all_imports)
                    if "." in i.name:
                        for splitted_name in i.name.split("."):
                            if splitted_name in self.automl_configs:
                                new_import = dict()
                                new_import['name'] = i.name
                                # print("i.name is:",i.name)
                                new_import['asname'] = i.asname
                                # print("asname: ", i.asname)
                                new_import['module'] = self.get_module(item)
                                self.list_of_automl_related_imports.append(new_import)
                    elif i.name in self.automl_configs:
                        new_import = dict()
                        new_import['name'] = i.name
                        # print("i.name is:",i.name)
                        new_import['asname'] = i.asname
                        # print("asname: ", i.asname)
                        new_import['module'] = self.get_module(item)
                        self.list_of_automl_related_imports.append(new_import)

    def get_module(self,item):
        if isinstance(item, ast.ImportFrom):
            # split the first part
            if "." in item.module:
                for splitted_module in item.module.split("."):
                    if splitted_module in self.automl_configs:
                        # new_import = dict()
                        # new_import['module'] = item.module
                        return item.module
            elif item.module in self.automl_configs:
                return item.module
        return None
    def write_to_json(self):
        if not os.path.exists(self.output_dir+'imports/'+self.repo.split('/')[1]):
            os.makedirs(self.output_dir+'imports/'+self.repo.split('/')[1])
        file_path = self.output_dir+'imports/'+self.repo.split('/')[1]
        output_file = file_path+"/imports_{}_{}.json".format(self.file, self.version)
        with open(output_file, 'w') as f:
            json.dump(self.as_json(), f)
        return output_file

    def as_json(self):
        result = dict()
        result['file'] = self.file
        result['file_in_repo'] = self.file_path_in_repo
        result['repo'] = self.repo
        result['repo_version'] = self.version
        result['imports'] = self.imports
        return result
import ast
import os
import json
from parser.finder import FunctionCallsFinder

class CollectFunctionCalls:
    def __init__(self, file, repo, version, source, output_dir, file_path_in_repo):
        self.source = source
        self.abs_file = file
        self.file_path_in_repo = file_path_in_repo
        self.file = os.path.basename(self.abs_file)
        self.repo = repo
        self.version = version
        self.output_dir = output_dir
        self.fcf = FunctionCallsFinder()
        self.function_calls = list()
        if not os.path.exists(self.output_dir+'fcalls'):
            os.makedirs(self.output_dir+'fcalls')
    def find_all(self):
        tree = ast.parse(self.source)
        self.fcf.visit(tree)
        self.function_calls = list()
        for call in self.fcf.calls:
            self.function_calls.append(self._add_file_data(call))

    def export_to_json(self):
        if not os.path.exists(self.output_dir+'fcalls/'+self.repo.split('/')[1]):
            os.makedirs(self.output_dir+'fcalls/'+self.repo.split('/')[1])
        file_path = self.output_dir+'fcalls/'+self.repo.split('/')[1]
        output_file = file_path + "/fcalls_{}_{}.json".format(self.file, self.version)
        with open(output_file, 'w') as f:
            json.dump(self.function_calls, f)
        return output_file

    def _add_file_data(self, call):
        call['file'] = self.file
        call['file_in_repo'] = self.file_path_in_repo
        call['repo'] = self.repo
        call['repo_version'] = self.version
        return call
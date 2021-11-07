import ast
class FindAutomlImports:

    def __init__(self, source, file_name, auto_ml_config):
        self.source = source
        self.file_name = file_name
        self.imports_automl_config = False
        self.auto_ml_config = auto_ml_config

    def parse(self):
        tree = ast.parse(self.source)
        tree_body = tree.body
        for item in tree_body:
            try:
                if isinstance(item, ast.Import):
                    if item.names[0].name in self.auto_ml_config:
                        self.imports_automl_config = True
                        return
                if isinstance(item, ast.ImportFrom):
                    if item.level > 0:
                        # Relative imports
                        continue
                    for ml_lib in self.auto_ml_config:
                        if ml_lib in item.module:
                            self.imports_automl_config = True
                            return
            except Exception as e:
                print("Error on {}: {}. error: {}".format(self.file_name, item, e))
                continue
        self.imports_automl_config = False

    def file_imports_automl_configs(self):
        return self.imports_automl_config
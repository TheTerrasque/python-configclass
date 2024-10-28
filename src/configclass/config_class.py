from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from dacite import from_dict

from pprint import pprint

# https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python/18472142#18472142
def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

def _load_yaml(yaml_file):
    import yaml
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data

def _load_json(json_file):
    import json
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

class EnvVarLoader:
    def __init__(self, prefix, cls):
        self.prefix = prefix
        self.cls = cls

    def load(self):
        return self.load_section([self.prefix], self.cls)

    def load_section(self, env_path, cls):
        import os
        data = {}
        for field in fields(cls):
            pfn = env_path + [field.name]
            if is_dataclass(field.type):
                r = self.load_section(pfn, field.type)
                if r:
                    data[field.name] = r
            else:
                name = "_".join(pfn).upper()
                if name in os.environ:
                    data[field.name] = os.environ[name]
                    if field.type == bool:
                        data[field.name] = strtobool(data[field.name])
        return data

class ArgumentParser:
    def __init__(self, description, cls):
        import argparse
        self.parser = argparse.ArgumentParser(description=description, fromfile_prefix_chars='@', epilog="Arguments can also be read from a file using @file as argument, one argument per line")
        self.cls = cls
        self.translate = {}
        self.make_argparse(self.parser, [], cls)

    def make_argparse(self, parser, path, cls):
        for field in fields(cls):
            if is_dataclass(field.type):
                self.make_argparse(parser, path + [field.name], field.type)
            else:
                name = field.name
                if path:
                    name = "-".join(path) + "-" + name
                self.translate[name.replace("-", "_")] = {"path": path, "field": field}
                fieldtype = field.type == bool and strtobool or field.type    
                parser.add_argument(f"--{name}", type=fieldtype, help=f"Set {name} [Default: {field.default}]")
    
    def get_result(self):
        args = self.parser.parse_args()
        data = {}
        for name, value in vars(args).items():
            if value is None:
                continue
            field = self.translate[name]["field"]
            path = self.translate[name]["path"]
            if path:
                data[path[0]] = data.get(path[0], {})
                current = data[path[0]]
                for p in path[1:]:
                    current[p] = current.get(p, {})
                    current = current[p]
                current[field.name] = value
            else:
                data[name] = value
        return data

def configclass(yaml_file="config.yaml", json_file="config.json", 
                argparse_text="Program configuration command line arguments", 
                env_prefix="CONFIG"):
    def inner(cls):
        c = dataclass(cls)
        c.from_dict = classmethod(from_dict)

        def load(c, data=None):
            data = data or {}

            if yaml_file:
                yaml_fil = Path(yaml_file)
                if yaml_fil.exists():
                    data.update(_load_yaml(yaml_fil))
            
            if json_file:
                json_fil = Path(json_file)
                if json_fil.exists():
                    data.update(_load_json(json_fil))

            if env_prefix:
                evl = EnvVarLoader(env_prefix, c)
                data.update(evl.load())

            if argparse_text:
                ap = ArgumentParser(argparse_text, c)
                data.update(ap.get_result())

            return c.from_dict(data)
        
        c.load = classmethod(load)
        return c
    return inner
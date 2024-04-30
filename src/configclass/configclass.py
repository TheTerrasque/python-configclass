from dataclasses import dataclass
from pathlib import Path
from dacite import from_dict

def configclass(cls, yaml_file="config.yaml", json_file="config.json"):
    c = dataclass(cls)
    c.from_dict = classmethod(from_dict)
    def load(c, **kwargs):
        yaml_fil = Path(yaml_file)
        json_fil = Path(json_file)
        if yaml_fil.exists():
            import yaml
            with open(yaml_fil, 'r') as f:
                data = yaml.safe_load(f)
            return c.from_dict(data)
        elif json_fil.exists():
            import json
            with open(json_fil, 'r') as f:
                data = json.load(f)
            return c.from_dict(data)
        return c(**kwargs)
    c.load = classmethod(load)
    return c
# Config Class

## Introduction
Config Class is a simple package for managing configuration settings in Python projects.

## Features
- **Easy Configuration**: The Config Class simplifies the process of managing configuration settings in your Python projects.
- **File-based Configuration**: The Config Class can load configuration settings from a yaml or json file, making it easy to switch between different configurations.
- **Support command line**: Automatically generates command-line switches for the configuration options.
- **Env vars support**: Configuration can also be set via environment variables.

## Installation
To use the Config Class in your Python project, you can install it via pip:

`pip install git+https://github.com/TheTerrasque/python-configclass`

## Examples

### Quick start

settings_test.py
```python
from dataclasses import dataclass, field
from configclass import configclass

@dataclass
class Test:
    test: str = "test"

@configclass()
class Settings:
    foo: bool = False
    url: str = ""
    footoo: bool = True
    my_model: str = "model.pt"
    test: Test = field(default_factory=Test)


setting = Settings.load()

print(setting.foo, setting.footoo, setting.test.test, settings.my_model)
```

```
$ python setting_test.py --foo true --footoo false --test-test "Test me" --my_model "model2.pt"
```

config.yaml:
```yaml
foo: true
test:
    test: "Hello world"
```

config.json:
```json
{
    "foo": true, 
    "test" {
        "test": "Hello world"
    }
}
```

Environment variables:
```
$ CONFIG_FOO="true" python settings_test.py
$ CONFIG_TEST_TEST="Hey mate" python settings_test.py
```
### Overriding defaults

```python

@configclass(yaml_file="config.yaml", 
    json_file="config.json", 
    argparse_text="Program configuration command line arguments", 
    env_prefix="CONFIG")
```

Setting any of these to `None` will disable that part as a config source.

## TODO

- Add optional documentation to fields for use in argparse, most likely via field() metadata
- Make config file used settable via command line or env vars

## Backstory

Most of my python projects are fairly small scripts, but they still have parts I want to configure. I usually use a dataclass for it, and use yaml or json to load from file and populate it. Later on I tend to add some command line arguments and/or env variables (for docker / kubernetes deployments).

After writing the same kind of code for the nth time, I decided to put together a small package for handling just that. I searched a bit online, but couldn't find a simple solution I liked. OmegaConf is a bit too heavy for my small projects, and I never really liked hydra.
# Config Class

## Introduction
This README provides an overview of the Config Class, a utility for managing configuration settings in Python projects.

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
    model: str = "model.pt"
    test: Test = field(default_factory=Test)


setting = Settings.load()

print(setting.foo, setting.footoo, setting.test.test)
```

```
python setting_test.py --foo true --footoo false --test-test "Test me"
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
CONFIG_FOO="true" python settings_test.py
CONFIG_TEST_TEST="Hey mate" python settings_test.py
```
### Overriding defaults

```python

@configclass(yaml_file="myfile.yml", json_file="myconfig.json", argparse_text="Program for testing configclass", env_prefix="MYTESTPROGRAM")
```

Setting any of these to `None` will disable that part as a config source.
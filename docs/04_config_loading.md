# Loading the configuration

When using external tools like gulp, fabric or deployer it might be necessary to
load the b5 configuration inside these tools. As b5 uses multiple configuration files
(by default: `config.yml` and `config.local.yml`) it would be very complicated to
do the merging of the configuration inside your code - while needing to match your
code to the way b5 does the merging.

Thus b5 will store it's internal state for external usage, including the merged
configuration. The full path to the file where the state is stored is provided
inside the environment as `B5_STATE_FILE`. The state is stored using the YAML file
format.
 
In general when needing to you should use the following patter:
* Test if `B5_STATE_FILE` exists in ENV, if so load and return "config" key
* Test if "config.yml" exists in path, if so load and return  
  (fallback config loading when called without b5)
* Just return an empty configuration

## Example code

**Note:** The following examples try to be as minimal as possible and thus
do not include any error handling.

### Javascript

```javascript
let
    fs = require("fs"),
    yaml = require("js-yaml");


function load_config() {
    if (!!process.env.B5_STATE_FILE) {
        return yaml.load(fs.readFileSync(process.env.B5_STATE_FILE, 'utf8')).config
    } else if (fs.existsSync('config.yml')) {
        return yaml.load(fs.readFileSync('config.yml', 'utf8'))
    } else {
        return {};
    }
}
```

### Python

```python
import os
import yaml


def load_config():
    if 'B5_STATE_FILE' in os.environ:
        with open(os.environ['B5_STATE_FILE'], 'r') as fh:
            return yaml.load(fh)['config']
    elif os.path.exists('config.yml'):
        with open('config.yml', 'r') as fh:
            return yaml.load(fh)
    else:
        return {}
```

**Note:** You need to install PyYAML for this to work.

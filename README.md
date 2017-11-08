# Dev install

```bash
virtualenv --python=python3 ENV  
source ENV/bin/activate  
pip install -e .  
```

Then you will be able to call the new python `b5` command.

## Notes

The current functionality does not allow older Taskfile's to be run (for now). Create a file like this in build/Taskfile:

```bash
task:test() {
    echo "test"
    for i in "$@"
    do
        echo $i
    done
    test:test "$@"
}
```

In addition add a build/config.yml with this contents:

```yaml
modules:
  test:
```

Then call `b5 test` or `b5 test foo "bar bla"`




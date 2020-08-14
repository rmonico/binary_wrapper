# binary_wrapper

A python generic binary wrapper

*Example:*

```Python
    from binary_wrapper import BinaryWrapper

    git = BinaryWrapper('git') # Find git in PATH

    git.init() # Run 'git init'
    git.add('README') # Run 'git add README'
    git.commit(m='First commit') # Run 'git commit -m "First commit"
    git.config(get='core.pager') # Run 'git config --get core.pager  # << notice the -- instead -
```

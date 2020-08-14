# binary_wrapper

A python generic binary wrapper

*Example:*
    from binary_wrapper import BinaryWrapper

    git = Binary('git') # Find git in PATH

    git.init() # Run 'git init'
    git.add('README') # Run 'git add README'
    git.commit(m='First commit') # Run 'git commit -m "First commit"
    git.config(get='core.pager') # Run 'git config --get core.pager  # << notice the -- instead -

import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess, sys
def after_install(options, home_dir):
    if sys.platform == 'win32':
        bin = 'Scripts'
    else:
        bin = 'bin'
    # Install package example:
    #subprocess.call([join(home_dir, bin, 'easy_install'),
    #                 'MyPackage'])
    # Run script example:
    #subprocess.call([join(home_dir, bin, 'my-package-script'),
    #                 'setup', home_dir])
    if os.path.exists('bootstrap.py'):
        logger.notify('Running buildout bootstrap')
        subprocess.call([os.path.join(home_dir, bin, 'python'),
                        'bootstrap.py'])
"""))
f = open('bootstrap_virtualenv_.py', 'w').write(output)

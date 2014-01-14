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
    if not os.path.exists(os.path.join(home_dir, 'buildout.cfg')):
        shutil.copy(os.path.join(home_dir, 'buildout.cfg.example'),
                    os.path.join(home_dir, 'buildout.cfg'))
    if os.path.exists('buildout-bootstrap.py'):
        logger.notify('Running buildout bootstrap')
        subprocess.call([os.path.join(home_dir, bin, 'python'),
                        'buildout-bootstrap.py', '-v 2.2.1'])
"""))
f = open('bootstrap_virtualenv_.py', 'w').write(output)

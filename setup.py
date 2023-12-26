from setuptools import setup
from setuptools.command.install import install

# Custom installation class
class CustomInstallCommand(install):
    def run(self):
        # Your custom code to be executed during installation
        print("Attempting to install a local xtb binary ...")
        from pathlib import Path
        from urllib.request import urlretrieve

        _LOCAL_BIN_XTB = (Path(__file__).parent / "bin" / "xtb")

        def install_local_xtb():
            import platform
            import tarfile
            import shutil
            import os
            os_name = platform.system()
            os_name = os_name.lower()

            def install_manually():
                print("="*80)
                print("failed to install xtb via conda package manager")
                print("="*80)
                if 'linux' in os_name:
                    print("attempting local install")
                    url = "https://github.com/grimme-lab/xtb/releases/download/v6.6.1/xtb-6.6.1-linux-x86_64.tar.xz"
                    temp_tar = "/tmp/_xtbf_temp_bins.tar.xz"
                    temp_untar = "/tmp/xtbf_xtb_temp/"
                    urlretrieve(url,temp_tar)
                    with tarfile.open(temp_tar) as f:
                        f.extractall(temp_untar)

                    fle = Path(temp_untar)
                    fle = list(fle.iterdir())
                    if len(fle) == 1:
                        fle = fle[0]
                        fle = fle / "bin" / "xtb"
                        shutil.copy(fle, str(_LOCAL_BIN_XTB.resolve()))
                        print("successfully installed local xtb binary.")
                        return True

                print("automatic installation of local xtb copy failed.")
                return False

            try:
                print("="*80)
                print("attempting to install xtb via conda package manager")
                print("="*80)
                rslt = os.system("conda install -y -c conda-forge xtb")
                if not rslt:
                    return True
                else:
                    return install_manually()
            except:
                return install_manually()
        try:
            install_local_xtb()
        except:
            print("failed to install local xtb binary automatically.")
            print("refer to the official documentation to install xtb manually")
        
        # Call the parent class's run method
        install.run(self)

setup(
    name='pyexample',
    version='0.1.0',    
    description='A minimal, functional interface to the semiempirical extended tight-binding (xtb) program',
    url='https://github.com/Bayer-Group/xtbf',
    author='Jan Wollschläger',
    author_email='janmwoll@gmail.com',
    license='BSD 3-clause',
    packages=['xtbf'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        'joblib', 'tqdm','numpy', 'pandas',
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
    ],
)
from setuptools.command.install import install


class Installer(install):
    """ A class used to perform bespoke installation following a package install.

    """
    def run(self):
        # Run the standard installation process
        install.run(self)

        # Custom post-installation logic to download the weights
        print("Installation complete")
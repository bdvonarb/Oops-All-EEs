################################################################################
#
# python-pycryptodome
#
################################################################################

PYTHON_PYCRYPTODOME_VERSION = 3.14.1
PYTHON_PYCRYPTODOME_SOURCE = pycryptodome-$(PYTHON_PYCRYPTODOME_VERSION).tar.gz
PYTHON_PYCRYPTODOME_SITE = https://files.pythonhosted.org/packages/32/09/41ea2633fea5b973dac9829de871b417ff3ce2963d07fd92e3f2d2a9ee9b
PYTHON_PYCRYPTODOME_SETUP_TYPE = setuptools
PYTHON_PYCRYPTODOME_LICENSE = FIXME: license id couldn't be detected
PYTHON_PYCRYPTODOME_LICENSE_FILES = LICENSE.rst Doc/src/license.rst

$(eval $(python-package))

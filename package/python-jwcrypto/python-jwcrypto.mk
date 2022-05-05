################################################################################
#
# python-jwcrypto
#
################################################################################

PYTHON_JWCRYPTO_VERSION = 1.0
PYTHON_JWCRYPTO_SOURCE = jwcrypto-$(PYTHON_JWCRYPTO_VERSION).tar.gz
PYTHON_JWCRYPTO_SITE = https://files.pythonhosted.org/packages/06/3d/5b9ee0232c05f4b461da9e6a844a9cc9d6a70a80ef5a2a99947d53f1f5f1
PYTHON_JWCRYPTO_SETUP_TYPE = setuptools
PYTHON_JWCRYPTO_LICENSE = LGPL-3.0
PYTHON_JWCRYPTO_LICENSE_FILES = LICENSE

$(eval $(python-package))

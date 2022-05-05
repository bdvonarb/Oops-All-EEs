################################################################################
#
# python-deprecated
#
################################################################################

PYTHON_DEPRECATED_VERSION = 1.2.13
PYTHON_DEPRECATED_SOURCE = Deprecated-$(PYTHON_DEPRECATED_VERSION).tar.gz
PYTHON_DEPRECATED_SITE = https://files.pythonhosted.org/packages/c8/d1/e412abc2a358a6b9334250629565fe12697ca1cdee4826239eddf944ddd0
PYTHON_DEPRECATED_SETUP_TYPE = setuptools
PYTHON_DEPRECATED_LICENSE = MIT, FIXME: license id couldn't be detected
PYTHON_DEPRECATED_LICENSE_FILES = LICENSE.rst docs/source/license.rst

$(eval $(python-package))

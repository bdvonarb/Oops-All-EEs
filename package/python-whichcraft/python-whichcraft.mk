################################################################################
#
# python-whichcraft
#
################################################################################

PYTHON_WHICHCRAFT_VERSION = 0.6.1
PYTHON_WHICHCRAFT_SOURCE = whichcraft-$(PYTHON_WHICHCRAFT_VERSION).tar.gz
PYTHON_WHICHCRAFT_SITE = https://files.pythonhosted.org/packages/67/f5/546c1494f1f8f004de512b5c9c89a8b7afb1d030c9307dd65df48e5772a3
PYTHON_WHICHCRAFT_SETUP_TYPE = setuptools
PYTHON_WHICHCRAFT_LICENSE = BSD-3-Clause
PYTHON_WHICHCRAFT_LICENSE_FILES = LICENSE

$(eval $(python-package))

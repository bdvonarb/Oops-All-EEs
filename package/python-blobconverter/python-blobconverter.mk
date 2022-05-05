################################################################################
#
# python-blobconverter
#
################################################################################

PYTHON_BLOBCONVERTER_VERSION = 1.2.8
PYTHON_BLOBCONVERTER_SOURCE = blobconverter-$(PYTHON_BLOBCONVERTER_VERSION).tar.gz
PYTHON_BLOBCONVERTER_SITE = https://files.pythonhosted.org/packages/03/40/54a6bcdd1cc4f5ce0531bb5fd62f64ca9966f3c541f6aec130e6dbaab18e
PYTHON_BLOBCONVERTER_SETUP_TYPE = setuptools

$(eval $(python-package))

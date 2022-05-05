################################################################################
#
# python-eel
#
################################################################################

PYTHON_EEL_VERSION = 0.14.0
PYTHON_EEL_SOURCE = Eel-$(PYTHON_EEL_VERSION).tar.gz
PYTHON_EEL_SITE = https://files.pythonhosted.org/packages/b3/c2/7dc22cc9ea23f0339316d6d249392d3ce67190430f2b05a316f3471ae15d
PYTHON_EEL_SETUP_TYPE = setuptools

$(eval $(python-package))

################################################################################
#
# python-v
#
################################################################################

PYTHON_V_VERSION = 0.0.0
PYTHON_V_SOURCE = v-$(PYTHON_V_VERSION).tar.gz
PYTHON_V_SITE = https://files.pythonhosted.org/packages/24/ba/eec746ccd4a6967465df49e3098b6c3c9435274aa5e6947dd6c1ee5dca49
PYTHON_V_SETUP_TYPE = setuptools

$(eval $(python-package))

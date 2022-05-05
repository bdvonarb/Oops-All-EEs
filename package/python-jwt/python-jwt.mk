################################################################################
#
# python-jwt
#
################################################################################

PYTHON_JWT_VERSION = 3.3.2
PYTHON_JWT_SOURCE = python_jwt-${PYTHON_JWT_VERSION}.tar.gz
PYTHON_JWT_SITE = https://files.pythonhosted.org/packages/f7/f1/6cce1d70788591595bf24c4dbc47af91bdf5f06fc9a0f3d2e19d77ca9d37
PYTHON_JWT_SETUP_TYPE = setuptools
PYTHON_JWT_LICENSE = MIT
PYTHON_JWT_LICENSE_FILES = LICENCE

$(eval $(python-package))

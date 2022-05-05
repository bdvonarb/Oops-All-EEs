################################################################################
#
# python-depthai
#
################################################################################

PYTHON_DEPTHAI_VERSION = 2.14.1.0
PYTHON_DEPTHAI_SOURCE = depthai-$(PYTHON_DEPTHAI_VERSION).tar.gz
PYTHON_DEPTHAI_SITE = https://files.pythonhosted.org/packages/a2/58/00746fd6e3282e4a37445eefd45702bc3a426f2e34768e1b0b57a957a9fd
PYTHON_DEPTHAI_SETUP_TYPE = setuptools
PYTHON_DEPTHAI_LICENSE = MIT
PYTHON_DEPTHAI_LICENSE_FILES = LICENSE depthai-core/LICENSE depthai-core/shared/depthai-shared/LICENSE depthai-core/shared/depthai-bootloader-shared/LICENSE
PYTHON_DEPTHAI_DEPENDENCIES = libusb

$(eval $(python-package))

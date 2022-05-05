################################################################################
#
# python-gevent
#
################################################################################

PYTHON_GEVENT_VERSION = 21.12.0
PYTHON_GEVENT_SOURCE = gevent-$(PYTHON_GEVENT_VERSION).tar.gz
PYTHON_GEVENT_SITE = https://files.pythonhosted.org/packages/c8/18/631398e45c109987f2d8e57f3adda161cc5ff2bd8738ca830c3a2dd41a85
PYTHON_GEVENT_SETUP_TYPE = setuptools
PYTHON_GEVENT_LICENSE = FIXME: license id couldn't be detected
PYTHON_GEVENT_LICENSE_FILES = LICENSE deps/libuv/LICENSE deps/c-ares/LICENSE.md deps/libev/LICENSE

$(eval $(python-package))

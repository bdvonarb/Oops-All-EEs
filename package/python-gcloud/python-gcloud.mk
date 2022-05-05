################################################################################
#
# python-gcloud
#
################################################################################

PYTHON_GCLOUD_VERSION = 0.18.3
PYTHON_GCLOUD_SOURCE = gcloud-$(PYTHON_GCLOUD_VERSION).tar.gz
PYTHON_GCLOUD_SITE = https://files.pythonhosted.org/packages/11/ab/d0cee58db2d8445c26e6f5db25d9b1f1aa14a3ab30eea8ce77ae808d10ef
PYTHON_GCLOUD_SETUP_TYPE = setuptools

$(eval $(python-package))

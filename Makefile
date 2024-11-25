# Top-level Makefile

# Purpose: Docker-ized build of the Shibboleth SP and its siblings
#	for a set of supported operating systems
# Author: John W. O'Brien <john@saltant.com>, Saltant Solutions LLC
# Sponsor: Internet2

# Targets:
#
# all			Build all components on each supported platform
# distfiles		Download tarball sources for each component
# images		Build Docker images for each supported platform
#
# <plat>-image		Build Docker image for platform <plat>
#
# <plat>		Build all components on platform <plat> that are
#			supported on that platform.
#
# <comp>		Build component <comp> on each supported platform
#			<comp> is a virtual component name the actual
#			products of which are a set of RPMs and SRPMs.
#
# <comp>_<plat>		Build component <comp> on platform <plat>
#
# run_container_<comp>_<plat>
# 			Run an interactive build environment container
# 			for component <comp> on platform <plat>
#
# Platform-specific notes:
#
# The following platforms are only enabled for all of the above
# targets when the variable HOST_IS_RHEL_QUALIFIED is defined
# (the value is not inspected).
#
# 	rhel7
# 	rhel8
# 	rhel9

# Constants and utility variables

makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
srcdir := $(dir $(makefile_path))

DEFAULT_DIST_EXT=tar.bz2
SOURCEDIR=$(srcdir)common/SOURCES
SPECDIR=$(srcdir)common/SPECS

BASETAG=base


# All components

COMPONENTS=\
	CURLOPENSSL \
	LOG4SHIB \
	OPENSAML \
	SHIBBOLETH \
	SHIBEDS \
	SHIBRESOLVER \
	XERCESC \
	XMLSECURITYC \
	XMLTOOLING

# Per-component variables

# *_COMPNAME	Component name. This is the name by which the component
#		is referred to in virtual targets.
# *_DISTNAME	Base name of the source distibution, if different from
#		the component's main name.
#		Default: $(*_COMPNAME)
# *_DISTNAME	Full filename of the source distribution.
# *_VERSION	Component's current version.
# *_URL		URL from which to retreive the component's source code.
#		Passed to curl or equivalent (i.e. not git, svn, etc).
# *_DEPENDS	A list of other components on which this component depends.
# *_DEPENDS_<plat>
#		A list of other components on which this component depends
#		when built on platform <plat>.
# *_VALID_PLATFORMS
#		A list of platforms on which it is valid to build this
#		components.
#		Default: $(PLATFORMS)


SHIBEDS_COMPNAME=shibboleth-embedded-ds
SHIBEDS_VERSION=1.3.0
SHIBEDS_DISTFILE=$(SHIBEDS_COMPNAME)-$(SHIBEDS_VERSION).tar.gz
SHIBEDS_URL=https://shibboleth.net/downloads/embedded-discovery-service/$(SHIBEDS_VERSION)/$(SHIBEDS_DISTFILE)

LOG4SHIB_COMPNAME=log4shib
LOG4SHIB_VERSION=2.0.1
LOG4SHIB_DISTFILE=$(LOG4SHIB_COMPNAME)-$(LOG4SHIB_VERSION).$(DEFAULT_DIST_EXT)
LOG4SHIB_URL=https://shibboleth.net/downloads/$(LOG4SHIB_COMPNAME)/$(LOG4SHIB_VERSION)/$(LOG4SHIB_DISTFILE)

XERCESC_COMPNAME=xerces-c
XERCESC_VERSION=3.3.0
XERCESC_MAJORVER=3
XERCESC_DISTFILE=$(XERCESC_COMPNAME)-$(XERCESC_VERSION).$(DEFAULT_DIST_EXT)
XERCESC_URL=https://downloads.apache.org/xerces/c/3/sources/$(XERCESC_DISTFILE)

XMLSECURITYC_COMPNAME=xml-security-c
XMLSECURITYC_VERSION=3.0.0
XMLSECURITYC_DISTFILE=$(XMLSECURITYC_COMPNAME)-$(XMLSECURITYC_VERSION).$(DEFAULT_DIST_EXT)
XMLSECURITYC_URL=https://shibboleth.net/downloads/$(XMLSECURITYC_COMPNAME)/$(XMLSECURITYC_VERSION)/$(XMLSECURITYC_DISTFILE)
XMLSECURITYC_DEPENDS=XERCESC

CURLOPENSSL_COMPNAME=curl-openssl
CURLOPENSSL_DISTNAME=curl
CURLOPENSSL_VERSION=8.10.1
CURLOPENSSL_DISTFILE=$(CURLOPENSSL_DISTNAME)-$(CURLOPENSSL_VERSION).$(DEFAULT_DIST_EXT)
CURLOPENSSL_URL=https://curl.haxx.se/download/$(CURLOPENSSL_DISTFILE)
CURLOPENSSL_VALID_PLATFORMS=amazonlinux2 centos7 rhel7

# Look closely: these variables refer to the OPENSAML variables
XMLTOOLING_COMPNAME=xmltooling
XMLTOOLING_VERSION=3.3.0
XMLTOOLING_DISTFILE=$(XMLTOOLING_COMPNAME)-$(XMLTOOLING_VERSION).$(DEFAULT_DIST_EXT)
XMLTOOLING_URL=https://shibboleth.net/downloads/c++-opensaml/$(OPENSAML_VERSION)/$(XMLTOOLING_DISTFILE)
XMLTOOLING_DEPENDS=LOG4SHIB XERCESC XMLSECURITYC
XMLTOOLING_DEPENDS_centos7=CURLOPENSSL
XMLTOOLING_DEPENDS_amazonlinux2=CURLOPENSSL
XMLTOOLING_DEPENDS_rhel7=CURLOPENSSL

OPENSAML_COMPNAME=opensaml
OPENSAML_VERSION=3.3.0
OPENSAML_DISTFILE=$(OPENSAML_COMPNAME)-$(OPENSAML_VERSION).$(DEFAULT_DIST_EXT)
OPENSAML_URL=https://shibboleth.net/downloads/c++-$(OPENSAML_COMPNAME)/$(OPENSAML_VERSION)/$(OPENSAML_DISTFILE)
OPENSAML_DEPENDS=LOG4SHIB XERCESC XMLSECURITYC XMLTOOLING

SHIBBOLETH_COMPNAME=shibboleth
SHIBBOLETH_DISTNAME=shibboleth-sp
SHIBBOLETH_VERSION=3.5.0
SHIBBOLETH_DISTFILE=$(SHIBBOLETH_DISTNAME)-$(SHIBBOLETH_VERSION).$(DEFAULT_DIST_EXT)
SHIBBOLETH_URL=https://shibboleth.net/downloads/service-provider/$(SHIBBOLETH_VERSION)/$(SHIBBOLETH_DISTFILE)
SHIBBOLETH_DEPENDS=LOG4SHIB OPENSAML XERCESC XMLSECURITYC XMLTOOLING
SHIBBOLETH_DEPENDS_centos7=CURLOPENSSL
SHIBBOLETH_DEPENDS_amazonlinux2=CURLOPENSSL
SHIBBOLETH_DEPENDS_rhel7=CURLOPENSSL

SHIBRESOLVER_COMPNAME=shibresolver
SHIBRESOLVER_DISTNAME=shibboleth-resolver
SHIBRESOLVER_VERSION=3.5.0
SHIBRESOLVER_DISTFILE=$(SHIBRESOLVER_DISTNAME)-$(SHIBRESOLVER_VERSION).$(DEFAULT_DIST_EXT)
SHIBRESOLVER_URL=https://shibboleth.net/downloads/service-provider/extensions/$(SHIBRESOLVER_COMPNAME)/$(SHIBRESOLVER_VERSION)/$(SHIBRESOLVER_DISTFILE)
SHIBRESOLVER_DEPENDS=LOG4SHIB OPENSAML SHIBBOLETH XERCESC XMLSECURITYC XMLTOOLING


#
# Platform-neutral variables and rules
#

# Define a set of virtual targets, one per component
TARGETS=$(foreach component,$(COMPONENTS),$($(component)_COMPNAME))
.PHONY: all $(TARGETS)
all: $(TARGETS)

# Retreive the tarball for each component from its distfile URL
define curl-distfile-component
$$(SOURCEDIR)/$$($(1)_DISTFILE):
	mkdir -p $$(SOURCEDIR)
	(cd $$(SOURCEDIR) && curl -L -O $$($(1)_URL))
endef

$(foreach component,$(COMPONENTS),$(eval $(call curl-distfile-component,$(component))))

# Convenience target to retreive all source tarballs
.PHONY: distfiles
distfiles: $(foreach component,$(COMPONENTS),$(SOURCEDIR)/$($(component)_DISTFILE))


#
# Supported platforms
#

PLATFORMS=\
	amazonlinux2 \
	amazonlinux2023 \
	centos7 \
	centos8 \
	rockylinux8 \
	rockylinux9 \
	fedora39 \
	fedora40

# Red Hat Enterprise Linux (RHEL) builds, which run inside
# Universal Base Image (UBI) containers, can only be performed
# on a RHEL host (8 or higher, suggested) that is registered
# with an active Red Hat account and attached to a valid
# subscription that makes the necessary RPM package
# repositories available inside each container. Ensure that:
# /etc/rhsm/rhsm.conf:manage_repos = 1
ifdef HOST_IS_RHEL_QUALIFIED
PLATFORMS:=$(PLATFORMS) \
	rhel7 \
	rhel8 \
	rhel9
endif

# To add a new platform, create the following
#	os/$OS/
#		image/
#			Dockerfile

# Platform-specific variables and rules

# By default, each component is valid on all platforms
# Factored out of the following macro because the meta, lazy, layered
# syntax got to be too much to wrap my head around.
$(foreach component,$(COMPONENTS),$(eval $(component)_VALID_PLATFORMS ?= $(PLATFORMS)))

# Each virtual component depends on being built on all valid platforms
define validity-component
$$($(1)_COMPNAME): $(foreach platform,$($(1)_VALID_PLATFORMS),$(if $(filter $(platform), $(PLATFORMS)), $$($(1)_COMPNAME)_$(platform)))
endef

$(foreach component,$(COMPONENTS),$(eval $(call validity-component,$(component))))

# Building for each platform depends on all components valid on that platform
define validity-platform
$(1): $(foreach component,$(COMPONENTS),$(if $(filter $(1),$($(component)_VALID_PLATFORMS)),$($(component)_COMPNAME)_$(1)))
endef

$(foreach platform,$(PLATFORMS),$(eval $(call validity-platform,$(platform))))

# Each component may depend on other components, generally or on
# specific platforms
define dependencies-component-platform
$($(1)_COMPNAME)_$(2): $(foreach depend,$($(1)_DEPENDS),$($(depend)_COMPNAME)_$(2)) $(foreach component,$($(1)_DEPENDS_$(2)),$($(component)_COMPNAME)_$(2))
endef

$(foreach platform,$(PLATFORMS),$(foreach component,$(COMPONENTS),$(eval $(call dependencies-component-platform,$(component),$(platform)))))

# Prepare each supported platform
define prepare-platform
$(1)_token = $$(srcdir).$(1)_image
$(1)_products = $(srcdir)os/$(1)/products
$$($(1)_token): $(srcdir)os/$(1)/image/Dockerfile
	mkdir -p $$($(1)_products)/{RPMS,SRPMS}
	@echo "==> Building base Docker image for $(1)"
	docker build -t shibboleth/$(1):$(BASETAG) $(srcdir)os/$(1)/image
	touch $$($(1)_token)
$(1)-image: $$($(1)_token)
endef

$(foreach platform,$(PLATFORMS),$(eval $(call prepare-platform,$(platform))))

# Convenience target to build Docker images for all supported platforms
.PHONY: images
images: $(foreach platform,$(PLATFORMS),$(platform)-image)


# Build RPMs and SRPMs for each component on each platform
define build-component-platform
$(1)_$(2)_token = $(srcdir).$(1)_$(2)_products
$$($(1)_$(2)_token): $$($(2)_token) $(SOURCEDIR)/$$($(1)_DISTFILE) $(SPECDIR)/$$($(1)_COMPNAME).spec
	@echo "==> Sanity checking $(1) on $(2)"
	grep -E "^Version:[[:space:]]+$$($(1)_VERSION)$$$$" $(SPECDIR)/$$($(1)_COMPNAME).spec
	@echo "==> Building $(1) on $(2)"
	docker run -it --rm \
		-v $$($(2)_products):/opt/build/external/out:z \
		-v $(srcdir)common:/opt/build/external/in:z \
		shibboleth/$(2):$(BASETAG) \
		/bin/sh -e /opt/build/external/in/build.sh $($(1)_COMPNAME)
	touch $$($(1)_$(2)_token)
$$($(1)_COMPNAME)_$(2): $$($(1)_$(2)_token)
endef

$(foreach platform,$(PLATFORMS),$(foreach component,$(COMPONENTS),$(eval $(call build-component-platform,$(component),$(platform)))))

# Run an interactive build environment container for each component on each platform
define run-container-component-platform
.PHONY: run_container_$($(1)_COMPNAME)_$(2)
run_container_$($(1)_COMPNAME)_$(2): $$($(1)_$(2)_image_token) $(SOURCEDIR)/$$($(1)_DISTFILE)
	docker run -it --rm \
		-v $$($(2)_products):/opt/build/external/out:z \
		-v $(srcdir)common:/opt/build/external/in:z \
		shibboleth/$(2):$($(1)_COMPNAME) \
		/bin/bash
endef

$(foreach platform,$(PLATFORMS),$(foreach component,$(COMPONENTS),$(eval $(call run-container-component-platform,$(component),$(platform)))))


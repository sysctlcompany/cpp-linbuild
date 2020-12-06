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
# <comp>		Build component <comp> on each supported platform
#			<comp> is a virtual component name the actual
#			products of which are a set of RPMs and SRPMs.
# <comp>_<plat>		Build component <comp> on platform <plat>
#

# Constants and utility variables

makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
srcdir := $(dir $(makefile_path))

DEFAULT_DIST_EXT=tar.bz2
SOURCEDIR=$(srcdir)common/SOURCES
SPECDIR=$(srcdir)common/SPECS


# All components

COMPONENTS=\
	LOG4SHIB \
	XERCESC \
	XMLSECURITYC \
	CURLOPENSSL \
	XMLTOOLING \
	OPENSAML \
	SHIBBOLETH

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


LOG4SHIB_COMPNAME=log4shib
LOG4SHIB_VERSION=2.0.0
LOG4SHIB_DISTFILE=$(LOG4SHIB_COMPNAME)-$(LOG4SHIB_VERSION).$(DEFAULT_DIST_EXT)
LOG4SHIB_URL=https://shibboleth.net/downloads/$(LOG4SHIB_COMPNAME)/$(LOG4SHIB_VERSION)/$(LOG4SHIB_DISTFILE)

XERCESC_COMPNAME=xerces-c
XERCESC_VERSION=3.2.1
XERCESC_MAJORVER=3
XERCESC_DISTFILE=$(XERCESC_COMPNAME)-$(XERCESC_VERSION).$(DEFAULT_DIST_EXT)
XERCESC_URL=https://archive.apache.org/dist/xerces/c/$(XERCESC_MAJORVER)/sources/$(XERCESC_DISTFILE)

XMLSECURITYC_COMPNAME=xml-security-c
XMLSECURITYC_VERSION=2.0.2
XMLSECURITYC_DISTFILE=$(XMLSECURITYC_COMPNAME)-$(XMLSECURITYC_VERSION).$(DEFAULT_DIST_EXT)
XMLSECURITYC_URL=https://downloads.apache.org/santuario/c-library/$(XMLSECURITYC_DISTFILE)
XMLSECURITYC_DEPENDS=XERCESC

CURLOPENSSL_COMPNAME=curl-openssl
CURLOPENSSL_DISTNAME=curl
CURLOPENSSL_VERSION=7.63.0
CURLOPENSSL_DISTFILE=$(CURLOPENSSL_DISTNAME)-$(CURLOPENSSL_VERSION).$(DEFAULT_DIST_EXT)
CURLOPENSSL_URL=https://curl.haxx.se/download/$(CURLOPENSSL_DISTFILE)
CURLOPENSSL_VALID_PLATFORMS=centos7

# Look closely: these variables refer to the OPENSAML variables
XMLTOOLING_COMPNAME=xmltooling
XMLTOOLING_VERSION=3.0.4
XMLTOOLING_DISTFILE=$(XMLTOOLING_COMPNAME)-$(XMLTOOLING_VERSION).$(DEFAULT_DIST_EXT)
XMLTOOLING_URL=https://shibboleth.net/downloads/c++-opensaml/$(OPENSAML_VERSION)/$(XMLTOOLING_DISTFILE)
XMLTOOLING_DEPENDS=LOG4SHIB XERCESC XMLSECURITYC
XMLTOOLING_DEPENDS_centos7=CURLOPENSSL

OPENSAML_COMPNAME=opensaml
OPENSAML_VERSION=3.0.1
OPENSAML_DISTFILE=$(OPENSAML_COMPNAME)-$(OPENSAML_VERSION).$(DEFAULT_DIST_EXT)
OPENSAML_URL=https://shibboleth.net/downloads/c++-$(OPENSAML_COMPNAME)/$(OPENSAML_VERSION)/$(OPENSAML_DISTFILE)
OPENSAML_DEPENDS=LOG4SHIB XERCESC XMLSECURITYC XMLTOOLING

SHIBBOLETH_COMPNAME=shibboleth
SHIBBOLETH_DISTNAME=shibboleth-sp
SHIBBOLETH_VERSION=3.0.4
SHIBBOLETH_DISTFILE=$(SHIBBOLETH_DISTNAME)-$(SHIBBOLETH_VERSION).$(DEFAULT_DIST_EXT)
SHIBBOLETH_URL=https://shibboleth.net/downloads/service-provider/$(SHIBBOLETH_VERSION)/$(SHIBBOLETH_DISTFILE)
SHIBBOLETH_DEPENDS=LOG4SHIB XERCESC XMLSECURITYC XMLTOOLING OPENSAML
SHIBBOLETH_DEPENDS_centos7=CURLOPENSSL


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
	(cd $$(SOURCEDIR) && curl -O $$($(1)_URL))
endef

$(foreach component,$(COMPONENTS),$(eval $(call curl-distfile-component,$(component))))

# Convenience target to retreive all source tarballs
.PHONY: distfiles
distfiles: $(foreach component,$(COMPONENTS),$(SOURCEDIR)/$($(component)_DISTFILE))


#
# Supported platforms
#

PLATFORMS=\
	centos7 \
	centos8

# XXX took centos6 out because it just went EoL and the upstream repos broke

# To add a new platform, create the following
#	os/$OS/
#		image/
#			Dockerfile
#			build-<comp>.sh  # one per valid component
#		products/
#			RPMS/
#			SRPMS/

# Platform-specific variables and rules

# By default, each component is valid on all platforms
# Factored out of the following macro because the meta, lazy, layered
# syntax got to be too much to wrap my head around.
$(foreach component,$(COMPONENTS),$(eval $(component)_VALID_PLATFORMS ?= $(PLATFORMS)))

# Each virtual component depends on being built on all valid platforms
define validity-component
$$($(1)_COMPNAME): $(foreach platform,$($(1)_VALID_PLATFORMS),$$($(1)_COMPNAME)_$(platform))
endef

$(foreach component,$(COMPONENTS),$(eval $(call validity-component,$(component))))

# Each component may depend on other components, generally or on
# specific platforms
define dependencies-component-platform
$$($(1)_COMPNAME)_$(2): $(foreach depend,$$($(1)_DEPENDS),$$($(depend)_COMPNAME)_$(1)) $(foreach component,$$($(1)_DEPENDS_$(2)),$$($(component)_COMPNAME)_$(1))
endef

$(foreach platform,$(PLATFORMS),$(foreach component,$(COMPONENTS),$(eval $(call dependencies-component-platform,$(platform),$(component)))))

# Build a docker image for each supported platform
define build-docker-image-platform
$(1)_token = $$(srcdir).$(1)_image
$$($(1)_token): $(srcdir)os/$(1)/image/Dockerfile
	docker build -t shibboleth/$(1):latest $(srcdir)os/$(1)/image
	touch $$($(1)_token)
$(1)-image: $$($(1)_token)
endef

$(foreach platform,$(PLATFORMS),$(eval $(call build-docker-image-platform,$(platform))))

# Convenience target to build Docker images for all supported platforms
.PHONY: images
images: $(foreach platform,$(PLATFORMS),$(platform)-image)


# Build RPMs and SRPMs for a each component on each platform
define build-component-platform
$(1)_$(2)_token = $(srcdir).$(1)_$(2)_products
$$($(1)_$(2)_token): $$($(2)_token) $(SOURCEDIR)/$$($(1)_DISTFILE) $(SPECDIR)/$$($(1)_COMPNAME).spec
	mkdir -p $(srcdir)os/$(2)/products/{RPMS,SRPMS}
	docker run -it --rm \
		--mount type=bind,source=$(srcdir)os/$(2)/products,target=/opt/build/external/out \
		--mount type=bind,source=$(srcdir)common,target=/opt/build/external/in \
		shibboleth/$(2):latest \
		/bin/sh /opt/build/build-$($(1)_COMPNAME).sh
	touch $$($(1)_$(2)_token)
$$($(1)_COMPNAME)_$(2): $$($(1)_$(2)_token)
endef

$(foreach platform,$(PLATFORMS),$(foreach component,$(COMPONENTS),$(eval $(call build-component-platform,$(component),$(platform)))))

# TODO:
#  update components to latest versions (opensaml 3.1.0, xerces-c 3.2.3, sp 3.1.0.2)
#  add a clean target
#  teach each image to depend on the build scripts for that image
#  refresh an affected image in the event one of its dependencies changes
#  save build logs to the host
#  auto-generate build-scripts (maybe)
#  template %packager

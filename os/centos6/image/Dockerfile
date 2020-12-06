FROM centos:6.10

MAINTAINER John W. O'Brien <john@saltant.com>

RUN yum -y update \
    && yum -y install \
        autoconf automake boost-devel chrpath doxygen gcc-c++ git groff \
        httpd-devel libidn-devel libmemcached-devel libtool make \
        openldap-devel openssl-devel pkgconfig \
        rpm-build stunnel systemd-devel unixODBC-devel zlib-devel \
    && yum clean all

# internal and external are w.r.t. a container, where external locations
# are expected to be mounted and pre-populated with required inputs
ENV BUILD_BASE=/opt/build
ENV INT_BASE=${BUILD_BASE}/internal
ENV EXT_BASE=${BUILD_BASE}/external

RUN mkdir -p \
    ${INT_BASE}/{BUILD,BUILDROOT} \
    ${EXT_BASE}/{in,out}

RUN echo "%_topdir ${EXT_BASE}" > ~/.rpmmacros
RUN echo "%_builddir ${INT_BASE}/BUILD" >> ~/.rpmmacros
RUN echo "%_buildrootdir ${INT_BASE}/BUILDROOT" >> ~/.rpmmacros
RUN echo "%_specdir ${EXT_BASE}/in/SPECS" >> ~/.rpmmacros
RUN echo "%_sourcedir ${EXT_BASE}/in/SOURCES" >> ~/.rpmmacros
RUN echo "%_rpmdir ${EXT_BASE}/out/RPMS" >> ~/.rpmmacros
RUN echo "%_srcrpmdir ${EXT_BASE}/out/SRPMS" >> ~/.rpmmacros
RUN echo "%packager PLACE HOLDER <USER@EXAMPLE.COM>" >> ~/.rpmmacros

COPY . ${BUILD_BASE}

WORKDIR ${EXT_BASE}/in/SPECS

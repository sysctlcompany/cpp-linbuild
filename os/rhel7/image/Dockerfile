FROM registry.access.redhat.com/ubi7/ubi:7.9-1328

COPY *.repo /etc/yum.repos.d/

RUN yum-config-manager \
        --enable rhel-7-server-optional-rpms \
    && yum -y update \
    && yum -y install \
        autoconf automake boost-devel chrpath doxygen gcc-c++ git groff \
        httpd-devel libidn-devel libmemcached-devel libtool make \
        openldap-devel openssl-devel pkgconfig \
        rpm-build stunnel systemd-devel unixODBC-devel zlib-devel \
        createrepo \
    && yum clean all

# internal and external are w.r.t. a container, where external locations
# are expected to be mounted and pre-populated with required inputs
ENV BUILD_BASE=/opt/build
ENV INT_BASE=${BUILD_BASE}/internal
ENV EXT_BASE=${BUILD_BASE}/external

RUN mkdir -p \
    ${INT_BASE}/{BUILD,BUILDROOT} \
    ${EXT_BASE}/{in,out} \
    && ln -s ${EXT_BASE}/in/macros/macros.shibboleth /etc/rpm/

WORKDIR ${EXT_BASE}/in/SPECS

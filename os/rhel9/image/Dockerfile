FROM registry.access.redhat.com/ubi9/ubi:9.3-1610

COPY *.repo /etc/yum.repos.d/

RUN dnf \
        config-manager \
        --enable codeready-builder-for-rhel-9-x86_64-rpms \
    && dnf -y update \
    && dnf -y install \
        autoconf automake boost-devel chrpath curl-devel doxygen \
        gcc-c++ gdb git groff httpd-devel \
        libmemcached-devel libtool make openldap-devel openssl-devel \
        pkgconfig rpm-build stunnel systemd-devel unixODBC-devel \
        zlib-devel createrepo_c yum-utils \
    && dnf clean all

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

FROM centos:8.4.2105

COPY *.repo /etc/yum.repos.d/

RUN sed -i "s/enabled=0/enabled=1/" /etc/yum.repos.d/CentOS-Linux-PowerTools.repo \
    && sed -i \
        -e "s/^mirrorlist/#mirrorlist/" \
        -e "s|^#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|" \
        /etc/yum.repos.d/CentOS-Linux-*.repo \
    && yum -y update \
    && yum -y install \
        autoconf automake boost-devel curl-devel doxygen \
        gcc-c++ gdb git groff httpd-devel \
        libmemcached-devel libtool make openldap-devel openssl-devel \
        pkgconfig rpm-build stunnel systemd-devel unixODBC-devel \
        zlib-devel createrepo_c yum-utils \
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

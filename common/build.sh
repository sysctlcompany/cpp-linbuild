#!/bin/sh -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 component"
    exit 1
fi

component=$1
machine_arch=$(rpm -E '%{_arch}')
spec_arch=$(awk '$1=="BuildArch:" {print $2}' ${component}.spec)

if [ -n "$spec_arch" ]; then
    arch=$spec_arch
else
    arch=$machine_arch
fi

localrepo=${EXT_BASE}/out/RPMS/${arch}

if [ ! -e ${localrepo}/repodata/repomd.xml ]; then
    # Initialize empty local RPM repository
    mkdir -p ${localrepo}
    createrepo ${localrepo}
fi

# Install dependencies
yum-config-manager --enable local
yum-builddep -y ${component}.spec

# Produce RPMs and SRPMs
rpmbuild -ba --clean ${component}.spec

# Produce manifests
rpmspec -q --rpms ${component}.spec > ${EXT_BASE}/out/${component}.rpms
rpmspec -q --srpm ${component}.spec > ${EXT_BASE}/out/${component}.srpm

# Generate/update local RPM repository
createrepo ${localrepo}

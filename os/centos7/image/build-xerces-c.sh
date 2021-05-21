arch=$(rpm -E '%{_arch}')
rpmbuild -ba --clean xerces-c.spec
rpmspec -q --rpms xerces-c.spec > ${EXT_BASE}/out/xerces-c.rpms
rpmspec -q --srpm xerces-c.spec > ${EXT_BASE}/out/xerces-c.srpm
createrepo_c ${EXT_BASE}/out/RPMS/${arch}

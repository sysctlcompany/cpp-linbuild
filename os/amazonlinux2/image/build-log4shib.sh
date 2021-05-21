arch=$(rpm -E '%{_arch}')
rpmbuild -ba --clean log4shib.spec
rpmspec -q --rpms log4shib.spec > ${EXT_BASE}/out/log4shib.rpms
rpmspec -q --srpm log4shib.spec > ${EXT_BASE}/out/log4shib.srpm
createrepo_c ${EXT_BASE}/out/RPMS/${arch}

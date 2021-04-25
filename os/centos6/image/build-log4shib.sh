rpmbuild -ba --clean log4shib.spec
rpmspec -q --rpms log4shib.spec > ${EXT_BASE}/out/log4shib.rpms
rpmspec -q --srpm log4shib.spec > ${EXT_BASE}/out/log4shib.srpm

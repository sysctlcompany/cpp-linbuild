arch=$(rpm -E '%{_arch}')
rpmbuild -ba --clean curl-openssl.spec
rpmspec -q --rpms curl-openssl.spec > ${EXT_BASE}/out/curl-openssl.rpms
rpmspec -q --srpm curl-openssl.spec > ${EXT_BASE}/out/curl-openssl.srpm
createrepo_c ${EXT_BASE}/out/RPMS/${arch}

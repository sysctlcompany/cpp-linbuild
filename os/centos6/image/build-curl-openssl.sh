rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpmbuild -ba --clean curl-openssl.spec
rpmspec -q --rpms curl-openssl.spec > ${EXT_BASE}/out/curl-openssl.rpms
rpmspec -q --srpm curl-openssl.spec > ${EXT_BASE}/out/curl-openssl.srpm

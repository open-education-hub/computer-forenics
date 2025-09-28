FROM debian:bookworm AS base

RUN set -xe; \
    apt-get -yqq update; \
    apt-get -yqq install vsftpd \
    ;

RUN set -xe; \
    useradd -m -d /home/galilei -s /bin/bash galilei; \
    echo 'galilei:epursimove' | chpasswd \
    ;

RUN set -xe; \
    echo "local_enable=YES" >> /etc/vsftpd.conf; \
    echo "write_enable=YES" >> /etc/vsftpd.conf \
    ;

WORKDIR /
COPY run.sh /usr/local/bin/
CMD ["/usr/local/bin/run.sh"]

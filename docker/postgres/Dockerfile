FROM postgres:17
ENV TZ=Asia/Seoul
COPY docker/postgres/conf/postgres.conf /etc/postgres/postgres.conf
CMD ["postgres", "-c", "config_file=/etc/postgres/postgres.conf"]
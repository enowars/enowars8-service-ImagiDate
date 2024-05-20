FROM php:8.2-apache

RUN apt update -y && apt upgrade -y && apt install -y sqlite3 default-mysql-client
RUN docker-php-ext-install mysqli
COPY www /var/www/html

COPY run.sh /root
RUN chmod +x /root/run.sh

WORKDIR /var/www/html
ENTRYPOINT /root/run.sh
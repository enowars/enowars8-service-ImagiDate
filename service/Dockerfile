FROM php:8.2-apache

RUN apt update -y && apt upgrade -y && apt install -y sqlite3 default-mysql-client
RUN docker-php-ext-install mysqli
COPY www /var/www/html

COPY run.sh /root
COPY cleaner.sh /root
RUN chmod +x /root/run.sh
RUN chmod +x /root/cleaner.sh

WORKDIR /var/www/html

RUN mkdir uploads
RUN chmod -R 755 .
RUN chown -R root:www-data /var/www/html/
RUN chown -R www-data:www-data /var/www/html/uploads/

ENTRYPOINT /root/run.sh
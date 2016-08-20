FROM php:5.6-apache
RUN apt-get update
RUN apt-get install -y python python-pip
RUN pip install itsdangerous
RUN useradd snekuser
COPY ./*.php /var/www/html/
COPY ./secret_key /var/www/html/
COPY ./.htaccess /var/www/html/
COPY ./sneks /sneks
RUN gcc -o /sneks/read_file /sneks/read_file.c
RUN rm /sneks/read_file.c
RUN chmod 111 /var/www/html/secret_key
RUN chown -R snekuser:snekuser /sneks
RUN chmod 400 /sneks/*
RUN chmod 555 /sneks/read_file /sneks/straya.py
RUN chmod +s /sneks/read_file
RUN chmod 111 /var/www/html/secret_key

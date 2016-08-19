FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y xinetd python
RUN useradd -m whatsyourname
COPY ./whatsyourname.py /home/whatsyourname/whatsyourname.py
COPY ./flag /home/whatsyourname/flag
COPY ./nameservice /etc/xinetd.d/nameservice
RUN chown -R root:whatsyourname /home/whatsyourname
RUN chmod -R 750 /home/whatsyourname
RUN chown root:whatsyourname /home/whatsyourname/flag
RUN chmod 440 /home/whatsyourname/flag
EXPOSE 31337
CMD ["/usr/sbin/xinetd", "-d"]

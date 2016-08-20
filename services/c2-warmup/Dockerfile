FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y xinetd
RUN useradd -m warmup1
COPY ./warmup1 /home/warmup1/warmup1
COPY ./flag /home/warmup1/flag
COPY ./warmup1service /etc/xinetd.d/warmup1service
RUN chown -R root:warmup1 /home/warmup1
RUN chmod -R 750 /home/warmup1
RUN chown root:warmup1 /home/warmup1/flag
RUN chmod 440 /home/warmup1/flag
EXPOSE 31337
CMD ["/usr/sbin/xinetd", "-d"]

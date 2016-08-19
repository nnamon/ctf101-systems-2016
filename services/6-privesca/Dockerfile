FROM ubuntu:latest
ENV user=privesca
RUN apt-get update
RUN apt-get install -y openssh-server python
RUN useradd -m $user
RUN useradd -d /home/$user/ -M escalate
RUN echo "escalate:escalate" | chpasswd
RUN echo "$user     hard    nproc       20" >> /etc/security/limits.conf
RUN echo "escalate     hard    nproc       20" >> /etc/security/limits.conf
COPY ./flag /home/$user/flag
COPY ./escalate /home/$user/escalate
RUN chown -R root:$user /home/$user
RUN chmod -R 750 /home/$user
RUN chmod o+rx /home/$user
RUN chown root:$user /home/$user/flag
RUN chmod 440 /home/$user/flag
RUN chmod 2755 /home/$user/escalate
EXPOSE 1342
COPY entry.sh /entry.sh
RUN mkdir -p ~root/.ssh && chmod 700 ~root/.ssh/ && \
    cp -a /etc/ssh /etc/ssh.cache
RUN printf "Port 1342\n" >> /etc/ssh/sshd_config
ENTRYPOINT ["/entry.sh"]
CMD ["/usr/sbin/sshd", "-D", "-f", "/etc/ssh/sshd_config"]

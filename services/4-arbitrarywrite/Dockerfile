FROM ubuntu:latest
ENV user=arbitrarywrite
RUN apt-get update
RUN apt-get install -y xinetd python
RUN useradd -m $user
RUN echo "$user     hard    nproc       20" >> /etc/security/limits.conf
COPY ./arbitrarywrite.py /home/$user/arbitrarywrite.py
COPY ./flag /home/$user/flag
COPY ./writeservice /etc/xinetd.d/writeservice
RUN mkdir /home/$user/accounts
RUN mkdir /home/$user/secrets
RUN chown -R root:$user /home/$user
RUN chmod -R 750 /home/$user
RUN chown root:$user /home/$user/flag
RUN chmod 440 /home/$user/flag
RUN chmod g+rwx /home/$user/accounts
RUN chmod g+rwx /home/$user/secrets
EXPOSE 31337
CMD ["/usr/sbin/xinetd", "-d"]

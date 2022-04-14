FROM ubuntu:latest

RUN apt-get update -y ; apt-get install -y tzdata
ENV TZ=Asia/Tokyo
RUN apt-get update -y ; apt-get upgrade -y
RUN apt-get install -y apache2 --no-install-recommends; apt-get install -y libapache2-mod-wsgi-py3 --no-install-recommends
RUN a2enmod wsgi

RUN mkdir /var/www/app
COPY . /var/www/app

RUN cd /usr/local/bin ; ln -s /usr/bin/python3 python

RUN apt-get install -y wget --no-install-recommends
RUN adduser --system --group --disabled-login worker ; cd /home/worker/
RUN apt-get update -y ; apt-get upgrade -y
RUN apt-get install -y python3-pip --no-install-recommends
RUN wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py' ; python get-pip.py --disable-pip-version-check --no-cache-dir
RUN pip --version ; rm -f get-pip.py

RUN pip install -r /var/www/app/requirements.txt

RUN chown -R worker:www-data /var/www/app

COPY cafe.conf /etc/apache2/sites-available/cafe.conf
RUN a2ensite cafe

RUN rm -rf /etc/apache2/sites-available/000-default.conf
RUN rm -rf /etc/apache2/sites-enabled/000-default.conf

RUN rm -rf /var/www/app/cafe.conf
RUN rm -rf /var/www/app/Dockerfile
RUN rm -rf /var/www/app/requirements.txt

RUN service apache2 start
RUN sleep 10

RUN chown -R worker:www-data /var/www/app

RUN service apache2 stop
RUN sleep 10

RUN service apache2 start
RUN sleep 4

EXPOSE 80

RUN apt-get clean

ENTRYPOINT ["/bin/bash", "/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

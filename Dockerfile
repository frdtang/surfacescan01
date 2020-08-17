############################################################
# Dockerfile to build Flask App
############################################################

# Set the base image
FROM raspbian/stretch:latest

ENV TZ=Europe/Oslo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
##############################################
# apache2, python, vim, graphviz, and latex #
#############################################

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python-dev\
    python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip3 install -r /var/www/apache-flask/app/requirements.txt
RUN a2enmod headers

# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi
# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf

COPY ./run.py /var/www/apache-flask/run.py
COPY ./app /var/www/apache-flask/app/
COPY ./ports.conf /etc/apache2/ports.conf

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf
RUN a2enmod rewrite

EXPOSE 8000

WORKDIR /var/www/apache-flask

RUN mkdir -p /home/winston
RUN chmod 777 /home/winston


RUN mkdir -p /data
RUN chmod 777 /data

# CMD ["/bin/bash"]
CMD  /usr/sbin/apache2ctl -D FOREGROUND
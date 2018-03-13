FROM plone:4.3.7

SHELL ["/bin/bash", "-c"]
USER root
RUN apt-get update && apt-get install -y git gcc subversion
USER plone

#USER zope
# Buildout pulls stuff from github via mr.developer, so pass a
# git read key in base 64
# docker build --build-arg github_key="$github_key"
# set github_key (cat id_rsa | base64 )
ARG github_key

COPY locales /plone/instance/locales
COPY profiles /plone/instance/profiles
COPY resources /plone/instance/resources
COPY src /plone/instance/src

USER root
RUN mkdir -p ~plone/.ssh && echo "$github_key" | base64 -d > ~plone/.ssh/id_rsa && \
  chmod 600 ~plone/.ssh/id_rsa && ssh-keyscan -t rsa github.com >> ~plone/.ssh/known_hosts && \
  chown -R plone ~plone/.ssh/ && chown -R plone /plone/instance
USER plone

COPY site-eggs.cfg /plone/instance/
RUN bin/buildout -vc site-eggs.cfg

COPY site.cfg /plone/instance/
RUN bin/buildout -vc site.cfg
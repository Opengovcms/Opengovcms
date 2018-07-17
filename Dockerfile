FROM python:2.7-slim-stretch

RUN useradd --system -m -d /plone -U -u 500 plone && \
    mkdir -p /root/.ssh /plone/instance

WORKDIR /plone/instance

RUN buildDeps="swig git-core ssh-client wget build-essential libc6-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-turbo-dev libtiff5-dev libopenjp2-7-dev zlib1g-dev virtualenv" && \
    apt-get update && \
    apt-get install -y --no-install-recommends $buildDeps

ADD profiles/base/base.cfg profiles/base/base.cfg
ADD profiles/versions profiles/versions

RUN runDeps="pdftohtml poppler-utils wv rsync lynx netcat libxml2 libxslt1.1 libjpeg62 libtiff5 libopenjp2-7" && \
    apt-get install -y --no-install-recommends $runDeps && \
    ssh-keyscan github.com > /root/.ssh/known_hosts && \
    pip install pip setuptools==1.3 zc.buildout==2.2.1 && \
    echo "[buildout]\nextends = profiles/base/base.cfg" > buildout.cfg && \
    buildout bootstrap && \
    bin/buildout && \
    rm -rf buildout.cfg profiles /var/lib/apt/lists/* && \
    apt-get purge -y --auto-remove $buildDeps

ADD . .

RUN echo "[buildout]\nextends = profiles/production.cfg\n[instance]\neffective-user = plone" > buildout.cfg && \
    bin/buildout && \
    chmod +x *.sh && \
    ./runless.sh && \
    chown -R plone:plone .

USER plone

HEALTHCHECK --interval=1m --timeout=5s --start-period=1m \
  CMD nc -z -w5 127.0.0.1 50000 || exit 1

CMD ["bin/instance", "console"]

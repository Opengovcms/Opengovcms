Opengovcms
=================================

Contains a buildout which installs a plone site with the opengovcms extension packages.

Run
----

$ docker build -t opengovcms .
$ docker run opengovcms

Development
-----------
$ docker-compose -f docker-compose-dev.yml up

Populate dev container with data from test/prod
$ docker cp filestorage opengovcms_plonedev_1:/data/
$ docker cp blobstorage opengovcms_plonedev_1:/data/
$ docker exec -it -u root opengovcms_plonedev_1 /bin/bash -c "chown -R plone:plone /data/*storage"

Then restart container to load new Data.fs

Production (on a docker swarm server)
----------
$ docker deploy -c docker-compose.yml

## docker connection to mariadb
```shell
docker run --detach --name itam-mariadb --env MARIADB_USER=user --env MARIADB_PASSWORD=123+aze --env MARIADB_DATABASE=itamweb --env MARIADB_ROOT_PASSWORD=rootpass  mariadb:latest
```
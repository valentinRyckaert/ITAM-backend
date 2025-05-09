## packages required
- python
- python-dev / python3-devel
- gcc
- openssl

## docker connection to mariadb
```shell
docker run --detach --name itam-mariadb -p 3306:3306 --env MARIADB_USER=user --env MARIADB_PASSWORD=123+aze --env MARIADB_DATABASE=itamweb --env MARIADB_ROOT_PASSWORD=rootpass  mariadb:latest

docker exec -it itam-mariadb mariadb -u root -p itamweb
```
```sql
INSERT INTO user VALUES (0, 'admin', '$2b$12$/GVZxPEYmhCT3MpY/uS8R.l3dXhpA5fBqzUIa9lESLMXgoVs6s2J2', 0, true);
```

## .env
```txt
DB_USER=user
DB_PASS=123456
DB_HOST=127.0.0.1:3306
DB_NAME=itam_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


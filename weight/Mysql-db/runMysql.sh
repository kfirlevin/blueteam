
mkdir ~/datafiles
docker build -t mysql-ganshmoael .
docker run -d -p 3306:3306 --restart unless-stopped -v ~/datafiles:/var/lib/mysql --name mysql-ganshmoael mysql-ganshmoael
docker exec -it mysql-ganshmoael bash
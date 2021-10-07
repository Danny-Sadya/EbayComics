# EbayComics
### Quick deploy
```
##make sure that you add your server ip in allowed hosts!!!
cd /opt/
sudo mkdir ebayScraping && cd ebayScraping
sudo git clone <rep:url>
cd EbayComics
sudo docker-compose build
sudo docker-compose up
##after start reopen terminal
sudo docker ps
##res will be like this one: 
CONTAINER ID   IMAGE                COMMAND                  CREATED        STATUS          PORTS                                                                                            NAMES
af52b4bf369c   trafic_web        "sh -c 'celery -A tr…"   7 hours ago    Up 48 minutes                                                                                                    trafic_worker_1
...
sudo docker exec -it <container:id> python manage.py makemigrations
sudo docker exec -it <container:id> python manage.py migrate
sudo docker exec -it <container:id> python manage.py collectstatic
```

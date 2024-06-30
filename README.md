- to stop the containers
docker-compose down

- to start the containers
docker-compose up --build

- in case getting errors with the laravel permissions run this command
sudo chown -R $(whoami):www-data backend/storage backend/bootstrap/cache
sudo chmod -R 775 backend/storage backend/bootstrap/cache

npm install in FE

delete all images
docker-compose down --rmi all
npm install wavefile

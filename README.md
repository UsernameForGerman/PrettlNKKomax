# tiktune

How to run server locally:
1. cat packages.txt | xargs sudo apt-get install
2. Get all requirements and run command:
"python -m pip install git+https://github.com/acrcloud/acrcloud_sdk_python" 
3. Install Redis:

4. Run Redis-server on localhost:6379
5. Run command "celery -A tiktune worker --loglevel=info" from project root
6. Run command "python manage.py migrate"
7. Run command "python manage.py runserver"

How to run frontend server:
1. Install Node.js 12(for Ubuntu see below):
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
2. Install all dependencies via command : "npm i"
3. Run server by command : "npm run dev"
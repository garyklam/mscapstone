sudo docker build -t civic_test .

sudo docker run --rm -it -p 80:5000 -v ${PWD}:/data civic_test:latest python3 /data/app.py 

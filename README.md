# Faiss Web Service

### Getting started
The fastest way to get started is to use [the docker hub image](https://hub.docker.com/r/plippe/faiss-web-service/) with the following command:
```sh
docker run --rm -it -p 5000:5000 plippe/faiss-web-service:[FAISS_RELEASE]
```

Once the container is running, you should be able to ping the service:
```sh
# Healthcheck
curl 'localhost:5000/ping'

# Faiss search for ids 1, 2, and 3
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "ids": [1, 2, 3]}'

# Faiss search for a vector
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "vectors": [[54.7, 0.3, 0.6, 0.4, 0.1, 0.7, 0.2, 0.0, 0.6, 0.5, 0.3, 0.2, 0.1, 0.9, 0.3, 0.6, 0.2, 0.9, 0.5, 0.0, 0.9, 0.1, 0.9, 0.1, 0.5, 0.5, 0.8, 0.8, 0.5, 0.2, 0.6, 0.2, 0.2, 0.7, 0.1, 0.7, 0.8, 0.2, 0.9, 0.0, 0.4, 0.4, 0.9, 0.0, 0.6, 0.4, 0.4, 0.6, 0.6, 0.2, 0.5, 0.0, 0.1, 0.6, 0.0, 0.0, 0.4, 0.7, 0.5, 0.7, 0.2, 0.5, 0.5, 0.7]]}'
```

### Custom index
By default, the faiss web service will use the files in the `resources` folder. Those can be overwritten by mounting new ones.

```sh
docker run \
    --rm \
    -it \
    -p 5000:5000 \
    -v [PATH_TO_RESOURCES]:/opt/faiss-web-service/resources \
    plippe/faiss-web-service:[FAISS_RELEASE]
```

Another solution would be to create a new docker image [from `plippe/faiss-web-service`](https://docs.docker.com/engine/reference/builder/#from), that [adds your resources](https://docs.docker.com/engine/reference/builder/#add).


### Production
The application runs with Flask's build in server. Flask's documentation clearly states [it is not suitable for production](http://flask.pocoo.org/docs/1.1.x/deploying/).


### Run from Python

```python
import requests
import json

# Check functionality
result = requests.get('http://localhost:5000/ping')
print(result.content)
print('=' * 50)

# Check the NN search of existing vectors
result = requests.post('http://localhost:5000/faiss/search', 
                       json={"k": 5, "ids": [15795]})
content = json.loads(result.content)[0]
for data in content['neighbors']:
    print(data['id'], data['score'])
print('=' * 50)
     
# Check the NN search for a query vector (query is a list of lists)
result = requests.post('http://localhost:5000/faiss/search', 
                       json={"k": 6, "vectors": query})
content = json.loads(result.content)[0]
for data in content['neighbors']:
    print(data['id'], data['score'])
```

```
b'pong'
==================================================
31068 0.717127799987793
31131 0.7389295101165771
94802 0.7552334070205688
12955 0.7998499274253845
42838 0.8059492707252502
==================================================
15795 0.19295963644981384
31068 0.717127799987793
31131 0.7389295101165771
94802 0.7552334070205688
12955 0.7998499274253845
42838 0.8059492707252502
```

For now, this only works with a pre-trained index and vectors pickle in the *resources* folder.
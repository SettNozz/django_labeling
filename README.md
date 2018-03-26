Django Labeling


- Usage
=====
Start docker:
```{r, engine='bash'}
$ sudo docker run -p 6379:6379 -d redis:2.8
```

Start app:
```{r, engine='bash'}
$ python3.6 manage.py runserver
```

Run worker:
```{r, engine='bash'}
$ python3.6 manage.py runworker thumbnails-generate
```


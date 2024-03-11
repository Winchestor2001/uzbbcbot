# uzbbcbot


### FontAwasome
https://fontawesome.com/v5/icons


### Celery run

```bash
celery -A core worker -l INFO -P eventlet
```

### Celery Beat run

```bash
celery -A core beat -l INFO
```
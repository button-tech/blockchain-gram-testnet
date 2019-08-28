# About
TON Testner Wrapper that allow to use TON via REST api 

Implementation for BUTTON Wallet Bot

## Build

- Worker 

Build and run 

```

# docker build -f Dockerfile.worker -r username/imagename .
# sudo docker run -v /mnt/filedir/masterchain:/app/wrappers/scripts/masterchain -v /mnt/filedir/basechain:/app/wrappers/scripts/basechain -e WORKDIR=/app/wrappers/scripts -e API=.. -d -p 80:80 username/imagename .
```
env API - it is endpoint for get info about status of generate account



- Load balancer (Round Robin)

1) Add addresses of hosts with workers (instance of api - wrappers/main.go). You should edit [this](https://github.com/button-tech/ton-grams-testnet/blob/master/rr_load_balancer/main.go#L89) line before build

2) Then you can build build and run

```

# docker build -f Dockerfile.rr_lb -t username/imagename .
# docker run username/imagename

```

## Warning
Do not use that in production. Demo purposes only.

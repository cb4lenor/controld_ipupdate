# controld_ipupdate
automatic update of ip to current ip via controlD API

if IP changes it deletes all ips and adds the new one. Script checks the IPs every 10min.


Install in a docker container on a server with the same external WAN IP to automatically update your IP if you can only use legacy DNS.

clone the repo
```bash
git clone https://github.com/cb4lenor/controld_ipupdate/
docker build -t controld_ipupdate .
docker run -d -e CONTROL_D_API_KEY='yourAPIKeyfromControlD' -e DEVICE_NAME='yourDeviceNameInControlD' controld_ipupdate
```


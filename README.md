# controld_ipupdate
automatic update of ip to current ip via controlD API


Install in a docker container on a server with the same external WAN IP to automatically update your IP if you can only use legacy DNS.

clone the repo
"""bash
docker build -t controld_ipupdate .
docker run -d -e CONTROL_D_API_KEY='yourAPIKeyfromControlD' -e DEVICE_NAME='yourDeviceNameInControlD' controld_ipupdate
"""

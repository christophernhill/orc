# Open Research Computing (ORC)

For more information about ORC project: https://notebooks.gesis.org/about/

## Technical Details

This ORC instance is deployed on kubernetes on bare metal machines with Ubuntu 18.04.
And kubernetes cluster is created with [kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/) 
(v1.14.1).
[Flannel](https://github.com/coreos/flannel/tree/v0.11.0) is used as pod network.
Docker version 18.06.2-ce is installed on servers.

All docker images of this project can be found in https://hub.docker.com/u/gesiscss/.

To monitor GESIS Notebooks: https://notebooks.gesis.org/grafana/

### [Nginx & Shibboleth](/nginx_shibboleth/)

Nginx is used as reverse proxy and load balancer.
It also handles [Shibboleth](https://www.shibboleth.net/) login and
SSL offloading/termination.

`nginx-shibboleth` service has type `ClusterIP` and all other services in ORC cluster in k8s 
has type `NodePort` and run behind `nginx-shibboleth` service.

[Dockerfile](/nginx_shibboleth/docker/Dockerfile) for `nginx-shibboleth` container
extends [gesiscss/nginx-shibboleth image](https://github.com/gesiscss/jhub_shibboleth_auth/tree/master/docker/shibboleth)
to be used in ORC instance.

[Nginx configuration files](/nginx_shibboleth/nginx)

[Shibboleth configuration files](/nginx_shibboleth/shibboleth/conf)

### [JupyterHub](/jupyterhub)

JupyterHub 0.9.6 runs under https://notebooks.gesis.org/jupyter/. 

Chart version [0.8.2](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/0.8.2).

[Dockerfile](/jupyterhub/docker/k8s_hub) of hub
extends [gesiscss/k8s-hub image](https://github.com/gesiscss/jhub_shibboleth_auth/tree/master/docker/k8s_hub)
in order to use [jhub_shibboleth_auth](https://github.com/gesiscss/jhub_shibboleth_auth)
authenticator in ORC.

[Single user server image](https://github.com/gesiscss/data_science_image)

### [BinderHub](/binderhub)

BinderHub (with `jupyter/repo2docker:d674ecee`) runs under https://notebooks.gesis.org/binder/. 

Chart version [0.2.0-10ac4d8](https://github.com/jupyterhub/binderhub/tree/10ac4d8)

Uses Docker Hub Registry (https://hub.docker.com/u/gesiscss/) to store built images.

### [NFS provisioner](/nfs_provisioner)

NFS provisioner (v2.2.1) is currently set as the default storage provider in k8s cluster.

### [ORC Site](/orc_site)

An app to serve ORC project base pages, such as home, shibboleth login, about...
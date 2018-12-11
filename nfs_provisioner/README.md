Based on [NFS provisioner (v2.2.0)](https://github.com/kubernetes-incubator/external-storage/tree/nfs-provisioner-v2.2.0-k8s1.12/nfs) repo.

There are 2 nfs provisioners in this project:
- `xfs-nfs-sc` is to be used for user PVs (it has project (user PV folder) based xfs quota).
- `nfs-sc` is the default storage class which is used everything except user PVs (e.g. prometheus, grafana data).

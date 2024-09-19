kubectl apply -f replicaset/replicaset.yaml 

### increment replicas
kubectl scale --replicas=3 replicaset myapp-replicaset
kubect edit replicaset myapp-replicaset

### labs replicaset
How many PODs exist on the system?
In the current(default) namespace.
$ kubectl  get pods


$kubectl  create deployment  httpd-frontend --image=httpd:2.4-alpine --repli
cas=3 --dry-run=client -o yaml > prueba.yaml
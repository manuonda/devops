** Profile 
$ minikube profile list

** Create cluster with perfil cluster2
$ minikube -p cluster2 kubectl 

** Create alias  
$ alias k="minikube -p cluster3 kubectl"
$ k get nodes

** Delete profile and cluster
$ minikube delete profile cluster2


** Create deployment imperativa
$ kubectl create deployment --image=nginx:latest --replica=2 pruebas
$ kubectl delete deployment pruebas

** Create pod from file 
$ kubectl apply -f pod_prueba.yaml
$ kubectl get all --> get all 
$ kubectl get pod --> only pods 
$ kubectl get pod -o wide  -> show expands information 
$ kubectl describe pod nginx -> information

** create metada, labels, selectors
```java
apiVersion: v1
kind: Pod
metadata: 
 name: nginx
 labels:
  project: pagina_web
  environment: testing
spec:
 containers:
 - name: nginx
   image: nginx:latest
   ports:
   - containerPort: 80
```
$ kubectl get pods --show-labels
$ kubectl get pods --selector project=pagina_web
$ kubectl get pods --show-labels -l pagina_web

** Exec **
$ kubectl exec nginx ls 
$ kubectl -it exec nginx bash


*** Aumentar number of replics 
$ kubectl scale rc nginx --replicas=10 (create 10 replics)

** crate namespaces 
$ kubectl create ns prueba 

** create file with ns
$ kubectl create ns miespacio --dry-run=client -o yaml

-- create pod in the namespace 
$ kubectl apply -f pod_prueba -n miespacio 

-- show all pods all namespaces
$ kubectl get pods -A

-- delete ns
$ kubectl delete ns miespacio

-- create deployment interactive 
$ kubectl --dry-run=client -o yaml create deploy --image=nginx:latest  nginx-deployment > deployment.yaml


-- increment replicas deployment 
$ kubectl scale deployment nginx-deployment --replicas=6


--rollback
$ kubectl rollout history deployment nginx-deployment 

-- show reivison
$ kubectl rollout history deployment nginx-deployment --revision=1

-- rollback revision
$ kubectl rollout undo deploymeng nginx-deployment --to-revision=2

-- status rollout 
$ kubectl rollout status deployment nginx-deployment 

-- etiquetar deployment
$ kubectl annotate deployment nginx-deployment kubernetes.io/change-cause="Version 1.2

--setear image 
$ kubectl set image deployment nginx-deployment nginx=nginx:1.21

-- config maps create 
$ kubectl create configmap test-cm --from-literal variable1=valor1


-- secrets
$ kubectl get secrets 

-- all secrets space 
$ kubectl get secrets -A

-- create secret 
$ kubectl create secret generic credenciales --from-file=username.txt --from-file=password.txt


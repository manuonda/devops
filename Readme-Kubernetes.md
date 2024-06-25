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
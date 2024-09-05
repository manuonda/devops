

# Crate namespace
k create ns demo 
# Set alias 
alias kn="kubectl -n" 
# Create confimap from file
kn demo create configmap mysql-initdb --from-file=./mysql-initdb.sql
kn demo describe configmap mysql-initdb


# Create a secret for MySQL
 kubectl create secret generic mysql-secret --namespace=demo \
 --type=kubernetes.io/basic-auth \
 --from-literal=password=manu1054 \
 --dry-run=client -o yaml > mysql-secret.yaml

# Display the content of the generated YAML file
echo "Content of mysql-secret.yaml:"
cat mysql-secret.yaml


kn demo apply -f mysql-secret.yaml
kn demo get secret mysql-secret




kubectl create pv mysql-pv-volume --namespace=demo --labels=type=local --capacity=20Gi --access-modes=ReadWriteOnce --storage-class=manual --host-path=/mnt/data --dry-run=client -o yaml > mysql-storage.yaml



# Create PersistentVolume YAML
apiVersion: v1
kind: PersistentVolume 
metadata:
 name: mysql-pv-volume
 namespace: demo 
 labels:
  type: local 
spec:
 storageClassName: manual 
 capacity:
  storage: 20Gi
 accessModes:
  -ReadWriteOnce
 hostPath:
  path: "/mnt/data"

--- 
apiVersion: v1
kind: PersistentVolumeClaim 
metadata:
 name: mysql-pv-clain
 namespace: demo
spec:
 accessModes:
  - ReadWriteOnce
 resources:
  requests:
   storage: 20Gi

# Create file mysql-storage.yaml
$kubectl apply -f mysql-storage.yaml

# Create file mysql-deployment.yaml
kubectl create deployment mysql-deployment --image=mysql-driver --dry-run=client -o yaml > mysql-deployment.yaml 

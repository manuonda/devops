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



Estrategias de Despliegue en Kubernetes

Kubernetes admite principalmente dos tipos de estrategias de despliegue:

    RollingUpdate (actualización gradual):
        Esta es la estrategia por defecto.
        Los pods antiguos se van reemplazando gradualmente por los nuevos pods.
        Asegura que no haya tiempo de inactividad, ya que siempre habrá pods en ejecución durante el proceso de actualización.
        Se controla mediante dos parámetros:
            maxUnavailable: El porcentaje máximo de pods que pueden estar no disponibles durante el despliegue.
            maxSurge: El número o porcentaje de pods adicionales que pueden ser creados temporalmente por encima del número de réplicas deseado.

    Recreate:
        Se detienen todos los pods existentes antes de crear nuevos pods.
        Causa una interrupción temporal en el servicio, ya que no hay pods en ejecución durante la actualización.
        Es útil cuando no se pueden ejecutar múltiples versiones de la aplicación al mismo tiempo.

RollingUpdate vs. Recreate

    RollingUpdate: Asegura disponibilidad continua durante la actualización. Los pods se actualizan en pequeños grupos, minimizando el riesgo de fallas.
    Recreate: Es más simple pero tiene el inconveniente de que provoca tiempo de inactividad, ya que todos los pods antiguos se eliminan antes de crear los nuevos.

Resumen

En tu caso, tienes configurada la estrategia RollingUpdate, lo que significa que, cuando realices una actualización del Deployment, Kubernetes reemplazará los pods antiguos por los nuevos de manera progresiva, manteniendo la disponibilidad del servicio sin interrupciones.

Si quieres ver cómo funciona una estrategia diferente como Recreate, puedes cambiarla, como te expliqué anteriormente.
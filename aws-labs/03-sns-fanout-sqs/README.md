# Lab 03 — SNS Fanout con SQS

**Dificultad:** Intermedio  
**Servicios AWS:** Amazon SNS, Amazon SQS, AWS Lambda  
**Tiempo estimado:** 45–60 min

## Caso de uso

Cuando se genera un nuevo pedido en un e-commerce, el sistema necesita notificar **simultáneamente** a tres servicios independientes:

- El servicio de **Stock** para reservar los productos
- El servicio de **Facturación** para generar la factura
- El servicio de **Logística** para preparar el envío

Cada servicio consume a su propio ritmo sin bloquear a los demás. Si uno falla, los otros no se ven afectados.

---

## Patrón Fanout

El patrón **SNS Fanout** consiste en suscribir múltiples colas SQS a un mismo topic SNS.  
Cuando SNS recibe un mensaje, lo entrega **en paralelo** a todas las colas suscritas.  
Cada cola actúa como buffer independiente para su consumidor.

```
                        ┌─────────────────────────────────────────────────────────┐
                        │                   PATRÓN FANOUT                         │
                        └─────────────────────────────────────────────────────────┘

┌──────────────┐   Publish    ┌──────────────────────────┐
│  Productor   │─────────────▶│      SNS Topic           │
│  (Lambda /   │              │   NuevoPedido-Topic      │
│   Script)    │              └──────────────┬───────────┘
└──────────────┘                             │
                                             │  Distribuye en paralelo
                          ┌──────────────────┼──────────────────┐
                          │                  │                  │
                          ▼                  ▼                  ▼
               ┌─────────────────┐  ┌───────────────┐  ┌──────────────────┐
               │  SQS Cola       │  │  SQS Cola     │  │  SQS Cola        │
               │  stock-queue    │  │  billing-queue│  │  logistics-queue │
               └────────┬────────┘  └───────┬───────┘  └────────┬─────────┘
                        │                   │                   │
                        ▼                   ▼                   ▼
               ┌─────────────────┐  ┌───────────────┐  ┌──────────────────┐
               │ Lambda / Worker │  │ Lambda/Worker │  │ Lambda / Worker  │
               │  stock-service  │  │ billing-svc   │  │ logistics-svc    │
               └─────────────────┘  └───────────────┘  └──────────────────┘
```

---

## Diferencia clave: SNS vs SQS vs Fanout

| Concepto | Comportamiento |
|---|---|
| **SNS solo** | Entrega inmediata. Si el suscriptor no está disponible, el mensaje se pierde |
| **SQS solo** | El mensaje espera en cola hasta que un consumidor lo lea |
| **SNS + SQS (Fanout)** | SNS garantiza la entrega a la cola; SQS retiene el mensaje hasta que el worker lo procese |

---

## Arquitectura del Lab

```
                    ┌─────────────────┐
                    │  Script Python  │
                    │  (productor.py) │
                    └────────┬────────┘
                             │
                    Publica evento JSON
                    { "pedido_id": "123",
                      "producto": "Laptop",
                      "cantidad": 2 }
                             │
                             ▼
                    ┌─────────────────────────────┐
                    │       SNS Topic              │
                    │   arn::NuevoPedido-Topic     │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ┌──────────────────┐  ┌─────────────────┐  ┌──────────────────────┐
   │  stock-queue     │  │  billing-queue  │  │  logistics-queue     │
   │  (SQS Standard) │  │  (SQS Standard) │  │  (SQS Standard)      │
   └────────┬─────────┘  └────────┬────────┘  └──────────┬───────────┘
            │                     │                      │
            ▼                     ▼                      ▼
   ┌──────────────────┐  ┌─────────────────┐  ┌──────────────────────┐
   │  consumidor.py   │  │  consumidor.py  │  │  consumidor.py       │
   │  --queue stock   │  │  --queue billing│  │  --queue logistics   │
   └──────────────────┘  └─────────────────┘  └──────────────────────┘
```

---

## Paso 1 — Crear el SNS Topic

1. Ir a **SNS → Topics → Create topic**
2. Tipo: **Standard**
3. Nombre: `NuevoPedido-Topic`
4. Click **Create topic**
5. Copiar el **Topic ARN** — lo necesitarás en los siguientes pasos

---

## Paso 2 — Crear las tres colas SQS

Repetir estos pasos para cada cola:

### Cola de Stock
1. Ir a **SQS → Create queue**
2. Tipo: **Standard**
3. Nombre: `stock-queue`
4. Visibility timeout: `30 segundos`
5. Click **Create queue**

### Cola de Facturación
1. Nombre: `billing-queue`
2. Misma configuración que arriba

### Cola de Logística
1. Nombre: `logistics-queue`
2. Misma configuración que arriba

> Copiar el **Queue ARN** y **Queue URL** de cada cola — los necesitarás para las suscripciones y el código.

---

## Paso 3 — Suscribir las colas al Topic SNS

Para **cada una** de las tres colas:

1. Ir al **SNS Topic** → **Create subscription**
2. Protocol: **Amazon SQS**
3. Endpoint: ARN de la cola (ej: `arn:aws:sqs:us-east-1:705000191530:stock-queue`)
4. Click **Create subscription**

Resultado esperado: el topic tendrá **3 suscripciones activas**.

---

## Paso 4 — Configurar la política de acceso en cada cola SQS

Cada cola SQS necesita permitir que SNS le envíe mensajes.  
Ir a cada cola → **Access policy** → Editar y agregar este statement:

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:TU_ACCOUNT_ID:NOMBRE_COLA",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:TU_ACCOUNT_ID:NuevoPedido-Topic"
        }
      }
    }
  ]
}
```

Reemplazar `TU_ACCOUNT_ID` y `NOMBRE_COLA` en cada cola.

---

## Paso 5 — Ejecutar el productor

El script [`productor.py`](./productor.py) publica un mensaje de pedido al topic SNS.

```bash
pip install boto3
python productor.py
```

**Qué hace:**
- Construye un evento JSON con los datos del pedido
- Publica el mensaje al topic `NuevoPedido-Topic`
- Imprime el MessageId devuelto por SNS

---

## Paso 6 — Ejecutar los consumidores

El script [`consumidor.py`](./consumidor.py) lee mensajes de una cola específica.

Abrir **tres terminales** y ejecutar una por cola:

```bash
# Terminal 1 — Servicio de Stock
python consumidor.py --queue stock-queue

# Terminal 2 — Servicio de Facturación
python consumidor.py --queue billing-queue

# Terminal 3 — Servicio de Logística
python consumidor.py --queue logistics-queue
```

Los tres deberían recibir el **mismo mensaje** casi simultáneamente.

---

## Paso 7 — Verificar en la consola AWS

1. Ir a **SQS → stock-queue → Send and receive messages**
2. Click **Poll for messages**
3. Deberías ver el mensaje con el JSON del pedido

Hacer lo mismo para `billing-queue` y `logistics-queue`.

---

## Resultado esperado

Al publicar un pedido con `productor.py`, los tres consumidores reciben el mismo evento:

```
[stock-queue]     Procesando pedido: 123 | Producto: Laptop | Cantidad: 2 → Reservando stock...
[billing-queue]   Procesando pedido: 123 | Producto: Laptop | Cantidad: 2 → Generando factura...
[logistics-queue] Procesando pedido: 123 | Producto: Laptop | Cantidad: 2 → Preparando envío...
```

---

## Código

Los scripts están en este mismo directorio:

| Archivo | Descripción |
|---|---|
| [`productor.py`](./productor.py) | Publica un evento de pedido al topic SNS |
| [`consumidor.py`](./consumidor.py) | Lee y procesa mensajes de una cola SQS |

---

## Conceptos reforzados

- **Desacoplamiento:** el productor no sabe quiénes son los consumidores
- **Resiliencia:** si `billing-queue` está caída, `stock-queue` y `logistics-queue` siguen funcionando
- **Escalabilidad:** podés agregar un cuarto suscriptor sin cambiar una línea del productor
- **Durabilidad:** SQS retiene el mensaje hasta 4 días por defecto si nadie lo consume

---

## Cleanup (evitar cargos)

```bash
# Eliminar suscripciones del topic
# Eliminar el topic SNS: NuevoPedido-Topic
# Eliminar las tres colas SQS: stock-queue, billing-queue, logistics-queue
```

---

## Laboratorios relacionados

| Lab | Tema |
|---|---|
| [Lab 01](../01-eda-s3-lambda-sns/README.md) | Event-Driven con S3 + Lambda + SNS |
| [Lab 02](../02-sqs-event-driven/Readme.md) | Cola de mensajes con SQS |
| Lab 04 *(próximamente)* | EventBridge — enrutamiento por reglas con Cognito |

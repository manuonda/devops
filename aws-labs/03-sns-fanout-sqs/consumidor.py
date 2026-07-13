"""
consumidor.py — Lee y procesa mensajes de una cola SQS específica.

Uso:
    python consumidor.py --queue stock-queue
    python consumidor.py --queue billing-queue
    python consumidor.py --queue logistics-queue

Requiere:
    pip install boto3
    AWS credentials configuradas (aws configure)
"""

import json
import argparse
import boto3

# ─── Configuración ────────────────────────────────────────────────────────────
REGION = "us-east-1"
ACCOUNT_ID = "TU_ACCOUNT_ID"

COLAS = {
    "stock-queue": {
        "url": f"https://sqs.{REGION}.amazonaws.com/{ACCOUNT_ID}/stock-queue",
        "servicio": "Stock",
        "accion": "Reservando stock en el almacén",
    },
    "billing-queue": {
        "url": f"https://sqs.{REGION}.amazonaws.com/{ACCOUNT_ID}/billing-queue",
        "servicio": "Facturación",
        "accion": "Generando factura electrónica",
    },
    "logistics-queue": {
        "url": f"https://sqs.{REGION}.amazonaws.com/{ACCOUNT_ID}/logistics-queue",
        "servicio": "Logística",
        "accion": "Preparando orden de envío",
    },
}
# ──────────────────────────────────────────────────────────────────────────────


def procesar_mensaje(mensaje_raw: dict, nombre_servicio: str, accion: str):
    """Extrae el pedido del mensaje SNS envuelto y lo procesa."""
    body = json.loads(mensaje_raw["Body"])

    # SNS envuelve el mensaje original dentro del campo "Message"
    if "Message" in body:
        pedido = json.loads(body["Message"])
    else:
        pedido = body

    print("\n" + "=" * 55)
    print(f"[{nombre_servicio}] Mensaje recibido")
    print("-" * 55)
    print(f"  Pedido ID  : {pedido.get('pedido_id', 'N/A')}")
    print(f"  Cliente    : {pedido.get('cliente', {}).get('nombre', 'N/A')}")
    print(f"  Producto   : {pedido.get('producto', 'N/A')}")
    print(f"  Cantidad   : {pedido.get('cantidad', 'N/A')}")
    print(f"  Total      : ${pedido.get('total', 0):.2f}")
    print(f"  Timestamp  : {pedido.get('timestamp', 'N/A')}")
    print(f"\n  → {accion}...")
    print(f"  ✓ [{nombre_servicio}] Procesado exitosamente")
    print("=" * 55)


def consumir_cola(nombre_cola: str):
    """Escucha mensajes de la cola SQS y los procesa."""
    config = COLAS.get(nombre_cola)
    if not config:
        print(f"Cola desconocida: '{nombre_cola}'")
        print(f"Opciones válidas: {', '.join(COLAS.keys())}")
        return

    sqs = boto3.client("sqs", region_name=REGION)
    queue_url = config["url"]
    servicio = config["servicio"]
    accion = config["accion"]

    print(f"\n[{servicio}] Escuchando mensajes en: {nombre_cola}")
    print("Presioná Ctrl+C para detener.\n")

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,        # Long polling — más eficiente
            VisibilityTimeout=30,
            AttributeNames=["All"],
        )

        mensajes = response.get("Messages", [])

        if not mensajes:
            print(f"[{servicio}] Sin mensajes nuevos. Esperando...")
            continue

        for mensaje in mensajes:
            try:
                procesar_mensaje(mensaje, servicio, accion)

                # Eliminar el mensaje de la cola después de procesarlo
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=mensaje["ReceiptHandle"],
                )
                print(f"  [SQS] Mensaje eliminado de la cola.")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"[{servicio}] Error procesando mensaje: {e}")
                # No eliminamos el mensaje para que reintente o vaya a DLQ


def main():
    parser = argparse.ArgumentParser(
        description="Consumidor SQS para el patrón SNS Fanout"
    )
    parser.add_argument(
        "--queue",
        required=True,
        choices=list(COLAS.keys()),
        help="Nombre de la cola a consumir",
    )
    args = parser.parse_args()

    consumir_cola(args.queue)


if __name__ == "__main__":
    main()

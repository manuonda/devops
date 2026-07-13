"""
productor.py — Publica un evento de nuevo pedido al topic SNS.

Uso:
    python productor.py

Requiere:
    pip install boto3
    AWS credentials configuradas (aws configure)
"""

import json
import boto3
import uuid
from datetime import datetime

# ─── Configuración ────────────────────────────────────────────────────────────
REGION = "us-east-1"
TOPIC_ARN = "arn:aws:sns:us-east-1:TU_ACCOUNT_ID:NuevoPedido-Topic"
# ──────────────────────────────────────────────────────────────────────────────


def publicar_pedido(pedido: dict) -> str:
    """Publica un pedido al topic SNS y retorna el MessageId."""
    sns = boto3.client("sns", region_name=REGION)

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="Nuevo Pedido",
        Message=json.dumps(pedido),
        MessageAttributes={
            "evento_tipo": {
                "DataType": "String",
                "StringValue": "NUEVO_PEDIDO",
            }
        },
    )

    return response["MessageId"]


def main():
    # Datos del pedido de ejemplo
    pedido = {
        "pedido_id": str(uuid.uuid4())[:8].upper(),
        "timestamp": datetime.utcnow().isoformat(),
        "cliente": {
            "id": "cli-42",
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
        },
        "producto": "Laptop",
        "cantidad": 2,
        "precio_unitario": 1200.00,
        "total": 2400.00,
        "estado": "NUEVO",
    }

    print("=" * 50)
    print("Publicando pedido al topic SNS...")
    print(f"Pedido ID : {pedido['pedido_id']}")
    print(f"Producto  : {pedido['producto']}")
    print(f"Cantidad  : {pedido['cantidad']}")
    print(f"Total     : ${pedido['total']:.2f}")
    print("=" * 50)

    message_id = publicar_pedido(pedido)

    print(f"\n✓ Mensaje publicado exitosamente")
    print(f"  MessageId : {message_id}")
    print(f"  Topic     : {TOPIC_ARN}")
    print("\nAhora las 3 colas SQS deberían haber recibido el mensaje.")
    print("Ejecutá consumidor.py en cada terminal para procesarlo.")


if __name__ == "__main__":
    main()

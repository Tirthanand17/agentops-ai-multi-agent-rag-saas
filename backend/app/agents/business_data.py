from __future__ import annotations

DEMO_CUSTOMERS = {
    "demo-retail": {
        "acme": {
            "customer_id": "cus_acme",
            "name": "Acme Retail",
            "tier": "Enterprise",
            "arr": 124000,
            "health_score": 61,
            "open_tickets": 3,
            "renewal_days": 42,
        },
        "nova": {
            "customer_id": "cus_nova",
            "name": "Nova Outfitters",
            "tier": "Growth",
            "arr": 48000,
            "health_score": 84,
            "open_tickets": 1,
            "renewal_days": 96,
        },
    }
}

DEMO_ORDERS = {
    "demo-retail": {
        "ORD-1042": {
            "order_id": "ORD-1042",
            "customer": "Acme Retail",
            "status": "Delayed",
            "value": 1890.0,
            "shipping_method": "Express",
        },
        "ORD-1048": {
            "order_id": "ORD-1048",
            "customer": "Nova Outfitters",
            "status": "Delivered",
            "value": 720.0,
            "shipping_method": "Standard",
        },
    }
}

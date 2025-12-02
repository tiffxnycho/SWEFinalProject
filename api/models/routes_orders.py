from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.orders import Order

router = APIRouter()

@router.get("/track/{tracking_num}")
def track_order(tracking_num: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.tracking_number == tracking_num).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "tracking_number": order.tracking_number,
        "status": order.status,
        "customer_name": order.customer_name,
        "order_date": order.order_date,
        "description": order.description,
    }

@router.get("/orders/{order_id}/status")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status
    db.commit()
    db.refresh(order)

    return {"message": "Status updated", "status": order.status}
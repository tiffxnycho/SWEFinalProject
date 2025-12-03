from decimal import Decimal

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import orders as model
from ..models import order_details as order_detail_model
from ..models import sandwiches as sandwich_model
from ..models import payments as payment_model
from ..controllers import promos as promo_controller



def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def pay(db: Session, item_id, request):
    # 1. Make sure order exists
    order = db.query(model.Order).filter(model.Order.id == item_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )

    # 2. Make sure it's not already paid
    if order.status == "PAID":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already paid.",
        )
    # validate promo code if provided
    promo = None
    if getattr(request, "promo_code", None):
        promo = promo_controller.get_valid_promo(db, request.promo_code)

    # 3. Validate payment amount
    try:
        payment_amount = Decimal(str(request.amount))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment amount.",
        )

    if payment_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero.",
        )

    # 4. Validate method
    if not request.method or not request.method.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment method is required.",
        )

    # 5. Load order items and compute total
    order_details = (
        db.query(order_detail_model.OrderDetail)
        .filter(order_detail_model.OrderDetail.order_id == item_id)
        .all()
    )

    if not order_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has no items to pay for.",
        )

    order_total = Decimal("0.00")
    for od in order_details:
        sandwich = (
            db.query(sandwich_model.Sandwich)
            .filter(sandwich_model.Sandwich.id == od.sandwich_id)
            .first()
        )
        if not sandwich:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sandwich with id {od.sandwich_id} not found.",
            )
        order_total += Decimal(str(sandwich.price)) * od.amount

    if payment_amount != order_total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount must equal order total ({order_total}).",
        )

    # 6. Create payment and update order status
    new_payment = payment_model.Payment(
        order_id=item_id,
        amount=payment_amount,
        method=request.method.strip(),
        status="COMPLETED",
    )

    try:
        db.add(new_payment)
        order.status = "PAID"
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_payment


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
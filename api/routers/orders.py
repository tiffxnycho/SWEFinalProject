from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import orders as controller
from ..schemas import orders as schema
from ..schemas import payments as payment_schema
from ..dependencies.database import get_db
from ..dependencies.employee_auth import require_employee_code

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
)

employee_router = APIRouter(
    tags=["Employee Orders"],
    prefix="/employee/orders",
    dependencies=[Depends(require_employee_code)],
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.post("/{item_id}/pay", response_model=payment_schema.Payment)
def pay_order(
    item_id: int, request: payment_schema.PaymentCreate, db: Session = Depends(get_db)
):
    return controller.pay(db=db, item_id=item_id, request=request)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@employee_router.get("/", response_model=list[schema.Order])
def employee_read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@employee_router.get("/{item_id}", response_model=schema.Order)
def employee_read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)
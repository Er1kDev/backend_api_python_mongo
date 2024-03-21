from fastapi import APIRouter

router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"description": "Not found"}}
)

product_list = ["product1", "product2", "product3", "product4", "product5"]


@router.get("/")
async def products():
    return product_list


@router.get("/{id}")
async def products(id: int):
    return product_list[id - 1]

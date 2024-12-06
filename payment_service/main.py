from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PaymentRequest(BaseModel):
    user_id: str
    status: int  # 0 for failure, 1 for success

@app.post("/authorize")
async def authorize(payment_request: PaymentRequest):
    """
    Mock endpoint to authorize payments.
    Args:
        payment_request (PaymentRequest): The payment data.

    Returns:
        dict: Confirmation of the payment authorization status.
    """
    if payment_request.status == 1:
        return {"status": "authorized", "user_id": payment_request.user_id}
    elif payment_request.status == 0:
        raise HTTPException(status_code=400, detail="Payment authorization failed.")
    else:
        raise HTTPException(status_code=422, detail="Invalid status value. Use 0 or 1.")
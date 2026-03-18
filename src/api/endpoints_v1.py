from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import Depends
from src.api.schemas import BlacklistV1Request, BlacklistV1Response
from src.api.security import verify_bearer_token
router = APIRouter()


# ===========================================
# 1.) Mock Blacklist
# ===========================================

@router.post("/mock/blacklist",
             tags = ["mock"],
             response_model = BlacklistV1Response)
async def blacklist(request: Request,
                    request_model: BlacklistV1Request,
                    # auth = Depends(verify_bearer_token)
):
    
    # [1] Define Variable
    body = request_model.model_dump(mode = "json")
    id_number = body.get("id_number", None)
    status = False
    mock_blacklist_data = ["1111111111111", "3333333333333", "1341486039218"]

    # [2] Check wheter id number from request is in list or not
    if id_number in mock_blacklist_data:
        status = True

    return BlacklistV1Response(ref_id = request.state.ref_no,
                               blacklist_status = status)

# *******************************************
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import Depends
from src.api.schemas import BlacklistV1Request, BlacklistV1Response
from src.api.security import verify_bearer_token
router = APIRouter()


# ===========================================
# 1.) Blacklist
# ===========================================

@router.post("/blacklist",
             tags = ["blacklist_v1"],
             response_model = BlacklistV1Response)
async def blacklist(request: Request,
                    request_model: BlacklistV1Request,
                    auth = Depends(verify_bearer_token)):
    
    body = request_model.model_dump_json()

    provider = []
    status = True
    return BlacklistV1Response(ref_id = request.state.ref_no,
                               provider = provider,
                               status = status)

# *******************************************
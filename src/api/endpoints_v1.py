from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import Depends
from src.api.schemas import BlacklistV1Request, BlacklistV1Response
from src.api.security import verify_bearer_token
from src.database import get_mock_database
from src.database.mockdb import MockConnector
router = APIRouter()


# ===========================================
# 1.) Mock Blacklist
# ===========================================

@router.post("/mock/blacklist",
             tags = ["mock"],
             response_model = BlacklistV1Response)
async def blacklist(request: Request,
                    request_model: BlacklistV1Request,
                    auth = Depends(verify_bearer_token),
                    database: MockConnector = Depends(get_mock_database)):
    
    status = False
    body = request_model.model_dump(mode = "json")
    id_card = body["id_number"]

    result = await database.fetch_all("")

    for record in result:
        if record["id_card"] == id_card:
            status = True
            break

    return BlacklistV1Response(ref_id = request.state.ref_no,
                               status = status)

# *******************************************
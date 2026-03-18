from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import json
import uuid
import time
import logging
from src.log.log_config import setup_logging
from src.api.route import all_router
from src.database import postgres_database, mongo_database, redis_database
from contextlib import asynccontextmanager
from src.config import get_env
env = get_env()

setup_logging()
logger = logging.getLogger(__name__)


# ===========================================
# 1.) Lifespan
# ===========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        
        logger.info("Service start...")

        yield

    except Exception as e:

        pass

    finally:

        logger.info("Service shutdown...")


# *******************************************

# ===========================================
# 2.) FastAPI Instance
# ===========================================

app = FastAPI(title = env.APP_NAME,
              lifespan = lifespan)

app.include_router(all_router)

# *******************************************

# ===========================================
# 3.) Middleware
# ===========================================

@app.middleware("http")
async def request_middleware(request: Request, call_next):

    try:

        logger.debug("Start request_middleware")

        # [1] Define response first to prevent variable error
        response = None

        # [2] Add ref_no to request
        request.state.ref_no = str(uuid.uuid4())

        # [3] Get the start time for measuring performance
        start_time = time.perf_counter()

        # [4] Call next (Send to Endpoint)
        response = await call_next(request)

        # [5] Measure the performance time
        process_time = (time.perf_counter() - start_time) * 1000

        # [6] Add process timeto response header
        response.headers["X-Process-Time"] = f"{process_time:.2f} ms"

        logger.debug("Finish request_middleware")

        return response

    except HTTPException as e:
        logger.error(e)
        return JSONResponse(status_code = e.status_code,
                            content = e.detail)
    
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code = 500,
                            content = str(e))

# *******************************************

# ===========================================
# 4.) Request Validation
# ===========================================

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, e: RequestValidationError):

    body_byte = await request.body()
    body = json.loads(body_byte)

    error_details = json.dumps(e.errors(), ensure_ascii = False, indent = 2, default = str)
    error_details = json.loads(error_details)

    logger.error(f"Request : {body}")
    logger.error(f"Error : {error_details}")

    return JSONResponse(status_code = 422,
                        content = error_details)

# *******************************************








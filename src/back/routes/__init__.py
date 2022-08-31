import json

import requests
from fastapi import APIRouter, HTTPException
from urllib.parse import urljoin

from pydantic import ValidationError

from back.models.models import (NodalCalcResponse, VlpIprCalcResponse,
                                WellModelCalcRequest, WellModelCalcResponse)
from back.routes.request_formers import (form_ipr_request,
                                         form_nodal_request,
                                         form_vlp_request)
from back.config import Settings

main_router = APIRouter(prefix="/well_model", tags=["WellModel"])


def check_correct_data(data: WellModelCalcRequest):
    pass
def general_requests(data: WellModelCalcRequest):
    try:
        vlp_data = form_vlp_request(data)
    except ValidationError:
        return False
    vlp = requests.post(url="http://localhost:8001/vlp/calc", json=vlp_data)
    ipr_data = form_ipr_request(data)
    ipr = requests.post(url="http://localhost:8002/ipr/calc", json=ipr_data)
    nodal_data = form_nodal_request(vlp.json(), ipr.json())
    nodal = requests.post(url="http://localhost:8003/nodal/calc", json=nodal_data)
    return {"vlp": vlp, "ipr": ipr, "nodal": nodal}


@main_router.put("/calc", response_model=WellModelCalcResponse)
def my_profile(data: WellModelCalcRequest):

    former_data = general_requests(data)
    if former_data == False:
        raise HTTPException(status_code=404, detail="Item not found")
    return WellModelCalcResponse(ipr=former_data["ipr"].json(), vlp=former_data["vlp"].json(),
                                 nodal=former_data["nodal"].json())

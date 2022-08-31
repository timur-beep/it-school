from back.models.models import (PVT, IprCalcRequest, NodalCalcRequest,
                                VlpCalcRequest, WellModelCalcRequest, VlpIprCalcResponse)


def form_vlp_request(well_model_request: WellModelCalcRequest):
    inclinometry = well_model_request.inclinometry
    casing = well_model_request.casing
    tubing = well_model_request.tubing
    pvt = well_model_request.pvt
    p_wh = well_model_request.p_wh
    geo_grad = well_model_request.geo_grad
    h_res = well_model_request.h_res
    return VlpCalcRequest(inclinometry=inclinometry, casing=casing,
                          tubing=tubing, pvt=pvt, p_wh=p_wh, geo_grad=geo_grad,
                          h_res=h_res).dict()


def form_ipr_request(well_model_request:WellModelCalcRequest):
    p_res = well_model_request.p_res
    wct = well_model_request.pvt.wct
    pi = well_model_request.pi
    pb = well_model_request.pvt.pb
    return IprCalcRequest(p_res=p_res, wct=wct, pi=pi, pb=pb).dict()


def form_nodal_request(vlp_result, ipr_result):
    return NodalCalcRequest(vlp=vlp_result, ipr=ipr_result).dict()

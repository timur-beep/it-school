from typing import List

from pydantic import BaseModel, Field, confloat, conlist, validator


class IprCalcRequest(BaseModel):
    p_res: confloat(gt=0) = Field(title="Пластовое давление, атм")
    wct: confloat(ge=0, le=100) = Field(title="Обводненность, %")
    pi: confloat(ge=0) = Field(title="Коэффициент продуктивности, м3/сут/атм")
    pb: confloat(ge=0) = Field(title="Давление насыщения, атм")


class Inclinometry(BaseModel):
    MD: conlist(
        unique_items=True,
        item_type=float) = Field(title="Измеренная по стволу глубина, м")
    TVD: List[float] = Field(title="Вертикальная глубина, м")


class Pipeline(BaseModel):
    d: confloat(gt=0) = Field(title="Диаметр трубы, м")


class Tubing(Pipeline):
    h_mes: confloat(gt=0) = Field(title="Глубина спуска НКТ, м")


class PVT(BaseModel):
    wct: confloat(ge=0, le=100) = Field(title="Обводненность, %")
    rp: confloat(ge=0) = Field(title="Газовый фактор, м3/т")
    gamma_oil: confloat(ge=0.6, le=1) = Field(title="Отн. плотность нефти")
    gamma_gas: confloat(ge=0.5, le=1) = Field(title="Отн. плотность газа")
    gamma_wat: confloat(ge=0.98, le=1.2) = Field(title="Отн. плотность воды")
    t_res: confloat(ge=10, le=500) = Field(title="Пластовая температура, C")


class VlpCalcRequest(BaseModel):
    inclinometry: Inclinometry = Field(title="Инклинометрия")
    casing: Pipeline = Field(title="Данные по ЭК")
    tubing: Tubing = Field(title="Данные по НКТ")
    pvt: PVT = Field(title="PVT")
    p_wh: confloat(ge=0) = Field(title="Буферное давление, атм")
    geo_grad: confloat(ge=0) = Field(title="Градиент температуры, C/100 м")
    h_res: confloat(ge=0) = Field(title="Глубина Верхних Дыр Перфорации, м")


class VlpIprCalcResponse(BaseModel):
    q_liq: List[float] = Field(title="Дебиты жидкости, м3/сут")
    p_wf: List[float] = Field(title="Забойное давление, атм")

    @validator("q_liq", "p_wf")
    def round_result(cls, v):
        return [round(val, 2) for val in v]


class WellModelPvt(PVT):
    pb: confloat(ge=0) = Field(title="Давление насыщения, атм")


class  WellModelCalcRequest(VlpCalcRequest):
    pvt: WellModelPvt = Field(title="PVT")
    p_res: confloat(gt=0) = Field(title="Пластовое давление, атм")
    pi: confloat(ge=0) = Field(title="Коэффициент продуктивности, м3/сут/атм")

    class Config:
        schema_extra = {
            "example": {
                "inclinometry": {
                    "MD": [0, 1000, 1500],
                    "TVD": [0, 1000, 1100]
                },
                "casing": {
                    "d": 0.1
                },
                "tubing": {
                    "d": 0.062,
                    "h_mes": 1000
                },
                "pvt": {
                    "wct": 50,
                    "rp": 100,
                    "gamma_oil": 0.8,
                    "gamma_gas": 0.7,
                    "gamma_wat": 1,
                    "t_res": 90,
                    "pb": 150
                },
                "p_wh": 10,
                "geo_grad": 3,
                "h_res": 1500,
                "p_res": 200,
                "pi": 1
            }
        }


class NodalCalcDecision(BaseModel):
    p_wf: confloat(gt=0) = Field(title="Забойное давление, атм")
    q_liq: confloat(ge=0) = Field(title="Дебит жидкости, м3/сут")

    @validator("q_liq", "p_wf")
    def round_result(cls, v):
        return round(v, 2)


class NodalCalcResponse(BaseModel):
    __root__: List[NodalCalcDecision]


class NodalCalcRequest(BaseModel):
    ipr: VlpIprCalcResponse = Field(title="IPR")
    vlp: VlpIprCalcResponse = Field(title="VLP")


class WellModelCalcResponse(NodalCalcRequest):
    nodal: NodalCalcResponse = Field(title="Рабочие режимы скважины")

    class Config:
        schema_extra = {
            "example": {
                "vlp": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 190, 180, 175, 185, 200]
                },
                "ipr": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 180, 160, 140, 120, 100]
                },
                "nodal": [{
                    "p_wf": 150,
                    "q_liq": 100
                }, {
                    "p_wf": 160,
                    "q_liq": 90
                }]
            }
        }

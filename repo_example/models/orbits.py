from models.base import RepoBaseModel, RepoBaseIdModel


class CreateOrbitModel(RepoBaseModel):
    x: float
    z: float
    v: float
    alpha: float
    t_period: float
    l1_r: float
    l2_r: float
    l3_r: float
    l4_r: float
    l5_r: float
    l6_r: float
    l1_im: float
    l2_im: float
    l3_im: float
    l4_im: float
    l5_im: float
    l6_im: float
    ax: float
    ay: float
    az: float
    dist_primary: float
    dist_secondary: float
    dist_curve: float
    cj: float
    stable: bool
    stability_order: int


class OrbitModel(CreateOrbitModel):
    id: int


class UpdateOrbitModel(RepoBaseIdModel):
    x: float | None = None
    z: float | None = None
    v: float | None = None
    alpha: float | None = None
    t_period: float | None = None
    l1_r: float | None = None
    l2_r: float | None = None
    l3_r: float | None = None
    l4_r: float | None = None
    l5_r: float | None = None
    l6_r: float | None = None
    l1_im: float | None = None
    l2_im: float | None = None
    l3_im: float | None = None
    l4_im: float | None = None
    l5_im: float | None = None
    l6_im: float | None = None
    ax: float | None = None
    ay: float | None = None
    az: float | None = None
    dist_primary: float | None = None
    dist_secondary: float | None = None
    dist_curve: float | None = None
    cj: float | None = None
    stable: bool | None = None
    stability_order: int | None = None

from sqlalchemy.orm import Mapped

from tables.base import Base


class OrbitsTable(Base):
    x: Mapped[float]
    z: Mapped[float]
    v: Mapped[float]
    alpha: Mapped[float]
    t_period: Mapped[float]

    l1_r: Mapped[float]
    l2_r: Mapped[float]
    l3_r: Mapped[float]
    l4_r: Mapped[float]
    l5_r: Mapped[float]
    l6_r: Mapped[float]
    l1_im: Mapped[float]
    l2_im: Mapped[float]
    l3_im: Mapped[float]
    l4_im: Mapped[float]
    l5_im: Mapped[float]
    l6_im: Mapped[float]

    ax: Mapped[float]
    ay: Mapped[float]
    az: Mapped[float]
    dist_primary: Mapped[float]
    dist_secondary: Mapped[float]
    dist_curve: Mapped[float]
    cj: Mapped[float]
    stable: Mapped[bool]
    stability_order: Mapped[int]

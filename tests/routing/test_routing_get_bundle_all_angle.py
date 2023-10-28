from __future__ import annotations

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf

pytestmark = pytest.mark.filterwarnings("ignore:Port")


def test_get_bundle_all_angle(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    c = gf.Component()

    mmi = gf.components.mmi2x2(width_mmi=10, gap_mmi=3)
    mmi1 = c << mmi
    mmi2 = c << mmi

    mmi2.move((100, 10))
    mmi2.rotate(30)

    routes = gf.routing.get_bundle_all_angle(
        mmi1.get_ports_list(orientation=0),
        [mmi2.ports["o2"], mmi2.ports["o1"]],
        connector=None,
    )
    lengths = {}
    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = float(route.length)

    if check:
        data_regression.check(lengths)


if __name__ == "__main__":
    gf.CONF.enforce_ports_on_grid = False
    c = gf.Component("demo")

    mmi = gf.components.mmi2x2(width_mmi=10, gap_mmi=3)
    mmi1 = c << mmi
    mmi2 = c << mmi

    mmi2.move((100, 10))
    mmi2.rotate(30)

    routes = gf.routing.get_bundle_all_angle(
        mmi1.get_ports_list(orientation=0),
        [mmi2.ports["o2"], mmi2.ports["o1"]],
        connector=None,
    )
    for route in routes:
        c.add(route.references)
    c = c.flatten_invalid_refs()
    c.show(show_ports=True)

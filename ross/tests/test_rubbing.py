import os
from pathlib import Path
from tempfile import tempdir

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_almost_equal

import ross as rs
from ross.defects.misalignment import MisalignmentFlex
from ross.units import Q_

steel2 = rs.Material(name="Steel", rho=7850, E=2.17e11, Poisson=0.2992610837438423)

#  Rotor with 6 DoFs, with internal damping, with 10 shaft elements, 2 disks and 2 bearings.
i_d = 0
o_d = 0.019
n = 33

# fmt: off
L = np.array(
        [0  ,  25,  64, 104, 124, 143, 175, 207, 239, 271,
        303, 335, 345, 355, 380, 408, 436, 466, 496, 526,
        556, 586, 614, 647, 657, 667, 702, 737, 772, 807,
        842, 862, 881, 914]
        )/ 1000
# fmt: on

L = [L[i] - L[i - 1] for i in range(1, len(L))]

shaft_elem = [
    rs.ShaftElement6DoF(
        material=steel2,
        L=l,
        idl=i_d,
        odl=o_d,
        idr=i_d,
        odr=o_d,
        alpha=8.0501,
        beta=1.0e-5,
        rotary_inertia=True,
        shear_effects=True,
    )
    for l in L
]

Id = 0.003844540885417
Ip = 0.007513248437500

disk0 = rs.DiskElement6DoF(n=12, m=2.6375, Id=Id, Ip=Ip)
disk1 = rs.DiskElement6DoF(n=24, m=2.6375, Id=Id, Ip=Ip)

kxx1 = 4.40e5
kyy1 = 4.6114e5
kzz = 0
cxx1 = 27.4
cyy1 = 2.505
czz = 0
kxx2 = 9.50e5
kyy2 = 1.09e8
cxx2 = 50.4
cyy2 = 100.4553

bearing0 = rs.BearingElement6DoF(
    n=4, kxx=kxx1, kyy=kyy1, cxx=cxx1, cyy=cyy1, kzz=kzz, czz=czz
)
bearing1 = rs.BearingElement6DoF(
    n=31, kxx=kxx2, kyy=kyy2, cxx=cxx2, cyy=cyy2, kzz=kzz, czz=czz
)

rotor = rs.Rotor(shaft_elem, [disk0, disk1], [bearing0, bearing1])


@pytest.fixture
def rub():

    massunbt = np.array([5e-4, 0])
    phaseunbt = np.array([-np.pi / 2, 0])

    rubbing = rotor.run_rubbing(
        dt=0.001,
        tI=0,
        tF=0.5,
        deltaRUB=7.95e-5,
        kRUB=1.1e6,
        cRUB=40,
        miRUB=0.3,
        posRUB=12,
        speed=1200,
        massunb=massunbt,
        phaseunb=phaseunbt,
        print_progress=True,
    )

    return rubbing


def test_rub_parameters(rub):
    assert rub.dt == 0.001
    assert rub.tI == 0
    assert rub.tF == 0.5
    assert rub.deltaRUB == 7.95e-5
    assert rub.kRUB == 1.1e6
    assert rub.cRUB == 40
    assert rub.miRUB == 0.3
    assert rub.posRUB == 12
    assert rub.speed == 1200


def test_rub_forces(rub):
    assert rub.forces_rub[rub.posRUB * 6, :] == pytest.approx(
        # fmt: off
    np.array([  0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         1.33959978,   2.38449456,   2.49659676,   1.81196092,
         0.59693967,  -1.62826881,  -4.24183226,  -6.00328692,
        -6.20469077,  -4.73542742,  -2.72934246,  -2.58572889,
        -6.09380802, -11.89929423, -16.28700512, -16.40580808,
       -12.28949661,  -6.4715516 ,  -1.9219398 ,   0.03597126,
         0.1483467 ,   0.06399221,   0.18405941,   0.44370982,
         0.59170921,   0.55028863,   0.61661081,   1.15972902,
         1.99145991,   2.2827491 ,   1.21484512,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,  -0.16254596,
        -1.15328767,  -1.31402774,  -0.57077859,   0.17589894,
         0.        ,   0.        ,   0.        ,   0.        ,
         1.35177422,   4.63052083,   8.26595768,  10.77229714,
        11.33408396,   9.97185414,   7.43725544,   4.8091569 ,
         2.90279915,   1.9280518 ,   1.60783411,   1.51278525,
         1.30371098,   0.82428403,   0.11364267,  -1.19150903,
        -2.28684891,  -2.8371608 ,  -2.70293006,  -1.7191864 ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
        -0.36389397,  -0.02296953,  -0.58251754,  -1.26899237,
        -1.37833025,  -0.83533185,   0.        ,  -1.54209802,
        -3.90213044,  -5.84909057,  -5.54764546,  -2.82245046,
         0.        ,   0.        ,  -0.9813435 ,  -5.02620683,
        -7.74948602,  -7.28498629,  -4.21292376,  -0.68113248,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.49651344,   0.94005508,   1.20771384,   1.01602262,
         0.58504824,   0.42249176,   0.74712263,   1.21263464,
         1.24036134,   0.53226162,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.81085807,   2.24845489,
         2.79783564,   2.36749471,   1.48390821,   0.91606906,
         1.10872277,   1.79762142,   2.27408108,   2.02409761,
         1.09722613,   0.03554649,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,  -3.20746741,
        -5.67109902,  -5.84109266,  -3.27138013,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,  -0.94605595,
        -2.89024152,  -2.82355527,  -0.91081202,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.29208245,   0.31276202,   0.55407755,
         0.65238154,   0.38599931,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.30206142,
         1.24645948,   2.17118657,   2.79095166,   2.92291644,
         2.4997066 ,   1.57624218,   0.3448333 ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
        -0.25292217,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,  -1.16895344,  -3.13003066,
        -4.31801297,  -3.79661585,  -1.72270664,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.22784948,   0.25813886,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,  -1.0783812 ,  -1.3305057 ,
         0.04528174,   0.        ,   0.        ,   0.        ,
         0.        ,   0.        ,   0.        ,   0.        ,
         0.        ])
        # fmt: on
    )

    assert rub.forces_rub[rub.posRUB * 6 + 1, :] == pytest.approx(
        # fmt: off
    np.array([ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
       -2.04052219e+00, -4.37686754e+00, -6.57561714e+00, -8.28614638e+00,
       -9.37724617e+00, -9.76009440e+00, -9.25692987e+00, -7.68859694e+00,
       -5.19404219e+00, -2.47936767e+00, -6.07948333e-01, -1.39115180e-01,
       -2.90615182e-01,  5.97112915e-01,  3.77091904e+00,  7.17958236e+00,
        8.50566481e+00,  6.92594573e+00,  3.76719699e+00,  1.38672233e+00,
        1.14491558e+00,  2.47008298e+00,  3.68895320e+00,  3.55463037e+00,
        2.15169896e+00,  7.16172655e-01,  4.58130638e-01,  1.31722645e+00,
        2.08017814e+00,  1.73698314e+00,  3.66421390e-01,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.41608952e+00,
        3.91872725e+00,  6.08751103e+00,  6.04879589e+00,  3.34005262e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        1.32257678e+00,  4.72982449e+00,  5.65624377e+00,  3.74610313e+00,
        2.79267497e-01, -1.61571947e+00, -2.61760973e+00, -2.76295228e+00,
       -2.46754501e+00, -2.27912450e+00, -2.49834149e+00, -3.08123496e+00,
       -3.77081696e+00, -4.26182369e+00, -4.32814157e+00, -3.92465771e+00,
       -3.18784204e+00, -2.30089569e+00, -1.36585055e+00, -4.14179880e-01,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
       -2.27746914e-01, -2.70148968e+00, -3.76415772e+00, -3.18400597e+00,
       -1.61071020e+00, -1.55937047e-01,  0.00000000e+00, -3.48135704e-01,
       -1.20173785e+00, -1.41164098e+00, -8.22789836e-01,  2.22972608e-02,
        0.00000000e+00,  0.00000000e+00,  1.11826215e+00,  3.42190067e+00,
        6.43880255e+00,  7.73939551e+00,  6.02642177e+00,  2.15551882e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        1.30262708e+00,  2.86790215e+00,  2.69095371e+00,  1.30596104e+00,
        6.27355622e-02, -1.46409693e-01, -1.61596825e-03,  2.02368230e-01,
        7.76880971e-02, -1.13943983e-01,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00, -1.20894403e-01, -9.67454370e-02,
       -3.75553448e-01, -6.69880393e-01, -7.81524379e-01, -8.20393160e-01,
       -1.19541101e+00, -2.17352648e+00, -3.38963807e+00, -3.97901667e+00,
       -3.24152409e+00, -1.21249778e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -1.71167570e+00,
       -2.63258535e+00, -2.11381589e+00, -7.29071480e-01,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.55809454e-01,
       -1.33550998e-01,  1.30622371e-01,  5.14772296e-01,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  5.87400070e-01,  2.52352092e+00,  3.18829790e+00,
        2.12154931e+00,  1.96463435e-01,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -1.71590151e-01,
        8.49398637e-02, -3.92130275e-03, -3.10907319e-01, -7.32520442e-01,
       -1.04949045e+00, -1.03758926e+00, -5.57304261e-01,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
       -2.22986515e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  1.36141783e-01, -1.62089253e-01,
       -6.56719131e-02,  3.67462355e-01,  6.11527272e-01,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00, -7.23117550e-02, -4.63871628e-02,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  8.90041966e-01,  1.14524591e+00,
        4.21896347e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00])
        # fmt: on
    )
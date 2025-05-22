from momapy_draw.core import *

from momapy.sbgn.pd import *
from momapy.positioning import *

output_file_path = "test_sbgn.pdf"

init()
n1 = node(MacromoleculeLayout, (60, 60), text="n1", stroke="red")
n2 = node(MacromoleculeLayout, right_of(n1, 100), text="n2", fill="blue")
sv1 = node(
    StateVariableLayout,
    n1.angle(90),
    text="val@var",
    fit_label=True,
    font_size=8,
)
a1 = arc(
    StimulationLayout,
    n1,
    n2,
    points=[mid_of(n1, n2) + (0, 50)],
)
render(output_file_path)

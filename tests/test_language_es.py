from number_parser import parser
import pytest

LANG = 'es'


class TestNumberParser():
    @pytest.mark.parametrize(
        "expected,test_input",
        [
            pytest.param(1_432_524, "un millón cuatrocientos treinta y dos mil quinientos veinticuatro",
                         marks=pytest.mark.xfail(reason="millón missing in lang data")),

            (302, "trescientos dos"),

            (5_000_320_000_000, "cinco billones trescientos veinte millones"),

            (3_023_001_432, "tres mil veintitrés millones mil cuatrocientos treinta y dos"),

            (101, "ciento uno"),

            pytest.param(5_764_607_500_000_000_031, "cinco trillones setecientos sesenta y cuatro mil seiscientos siete billones \
            quinientos mil millones treinta y uno", marks=pytest.mark.xfail(reason="trillones missing in lang data")),

            (31, "treinta y una"),

            (26, "veintiséis"),

            (424, "cuatrocientos veinticuatro"),

            (1_000_000_000, "mil millones"),

            pytest.param(1_000_000_000, "millardo", marks=pytest.mark.xfail(reason="millardo missing in lang data")),

            (342, "trescientas cuarenta y dos"),

            (3000000024, "tres mil millones veinticuatro"),

            pytest.param(10**24, "cuatrillón", marks=pytest.mark.xfail(reason="cuatrillón missing in lang data")),

            (256, "Doscientos cincuenta y seis"),

            (666, "seiscientos sesenta y seis"),

            (2_147_483_647, "Dos mil ciento cuarenta y siete millones cuatrocientos ochenta \
                y tres mil seiscientos cuarenta y siete"),

            pytest.param(10**100, "Gúgol", marks=pytest.mark.xfail(reason="Gúgol missing in lang data")),

            pytest.param(10**600, "centillón", marks=pytest.mark.xfail(reason="centillón missing in lang data")),

            pytest.param(100000, "Cien mil", marks=pytest.mark.xfail(reason="cien missing in lang data")),
        ]
    )
    def test_parse_number(self, expected, test_input):
        assert parser.parse_number(test_input, LANG) == expected

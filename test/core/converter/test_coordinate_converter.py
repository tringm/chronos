from core.converter.coordinate_converter import EpsgCoordinateConverter
from test.tests import TestCaseCompare


class TestEpsgCoordinateConverter(TestCaseCompare):
    @classmethod
    def setUpClass(cls):
        super(TestEpsgCoordinateConverter, cls).setUpClass()
        cls.converter = EpsgCoordinateConverter()

    def test_convert_coordinate(self):
        result = self.converter.convert_coordinate(('25497346.000153500', '6673006.000000000'), '3879', '4326')
        self.assertEqual(result, ('24.95219189', '60.16992717'))

    def test_convert_multiple_coordinates(self):
        result = self.converter.convert_multiple_coordinates([('25497346.000153500', '6673006.000000000'),
                                                              ('25496148.499851000', '6673960.500000000')],
                                                             '3879', '4326')
        self.assertEqual(result, [('24.95219189', '60.16992717'), ('24.93060254', '60.17848468')])

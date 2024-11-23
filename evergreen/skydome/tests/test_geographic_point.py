from django.test import TestCase

from skydome import geographic_point


class TestGeographicPoint(TestCase):

    def test_precision_gets_rounded(self):
        point_a = geographic_point.GeographicPoint(78.567876567898765, 45.2342413)
        self.assertEqual(point_a.latitude, 78.5679)
        self.assertEqual(point_a.longitude, 45.2342)

        point_b = geographic_point.GeographicPoint(-89.452007, -23.674111)
        self.assertEqual(point_b.latitude, -89.452)
        self.assertEqual(point_b.longitude, -23.6741)

        point_c = geographic_point.GeographicPoint(-87.23456, 170.34523345)
        self.assertEqual(point_c.latitude, -87.2346)
        self.assertEqual(point_c.longitude, 170.3452)

        point_d = geographic_point.GeographicPoint(45.2356543, -179.56789999)
        self.assertEqual(point_d.latitude, 45.2357)
        self.assertEqual(point_d.longitude, -179.5679)

    def test_no_over_rounding(self):
        point_a = geographic_point.GeographicPoint(0.981, -50.78)
        self.assertEqual(point_a.latitude, 0.981)
        self.assertEqual(point_a.longitude, -50.78)

        point_b = geographic_point.GeographicPoint(7, -10.999)
        self.assertEqual(point_b.latitude, 7)
        self.assertEqual(point_b.longitude, -10.999)

    def test_wrong_inputs_value_error(self):
        with self.assertRaises(ValueError):
            geographic_point.GeographicPoint(0, 180.1)

        with self.assertRaises(ValueError):
            geographic_point.GeographicPoint(0, -180.1)

        with self.assertRaises(ValueError):
            geographic_point.GeographicPoint(-90.1, 0)

        with self.assertRaises(ValueError):
            geographic_point.GeographicPoint(90.1, 0)

    def test_dm(self):
        point_a = geographic_point.GeographicPoint(78.36, -120.98)
        self.assertEqual(point_a.latitude_degrees_minutes, "78° 21′ N")
        self.assertEqual(point_a.longitude_degrees_minutes, "120° 58′ W")

        point_b = geographic_point.GeographicPoint(-1.5678, 15)
        self.assertEqual(point_b.latitude_degrees_minutes, "1° 34′ S")
        self.assertEqual(point_b.longitude_degrees_minutes, "15° 0′ E")

        null_island = geographic_point.GeographicPoint(0, 0)
        self.assertEqual(null_island.latitude_degrees_minutes, "0° 0′")
        self.assertEqual(null_island.longitude_degrees_minutes, "0° 0′")

    def test_dms(self):
        point_a = geographic_point.GeographicPoint(45.784, 133.3665)
        self.assertEqual(point_a.latitude_degrees_minutes_seconds, "45° 47′ 2″ N")
        self.assertEqual(point_a.longitude_degrees_minutes_seconds, "133° 21′ 59″ E")

        point_b = geographic_point.GeographicPoint(-50.3456, -0.0136)
        self.assertEqual(point_b.latitude_degrees_minutes_seconds, "50° 20′ 44″ S")
        self.assertEqual(point_b.longitude_degrees_minutes_seconds, "0° 0′ 49″ W")

        null_island = geographic_point.GeographicPoint(0, 0)
        self.assertEqual(null_island.latitude_degrees_minutes_seconds, "0° 0′ 0″")
        self.assertEqual(null_island.longitude_degrees_minutes_seconds, "0° 0′ 0″")


class TestLocations(TestCase):
    def test_enum_translates_to_geographic_point_instance(self):
        for point in geographic_point.Locations:
            self.assertIsInstance(point, geographic_point.GeographicPoint)

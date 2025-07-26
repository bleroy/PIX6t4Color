import unittest
from unittest import TestCase
from pix6t4.color import Color

def assertAlmostEqual(tuple1, tuple2, places=2):
    for a, b in zip(tuple1, tuple2):
        assert abs(a - b) < 10 ** (-places), f"{a} != {b} within {places} decimal places"

class TestColor(TestCase):
    def test_color_from_integer(self):
        color = Color.fromInt(0xFF102080)
        self.assertEqual(color.red, 255)
        self.assertEqual(color.green, 16)
        self.assertEqual(color.blue, 32)
        self.assertAlmostEqual(color.alpha, 0.5, places=2)

    def test_color_components_from_rgba(self):
        color = Color.fromRGBA(100, 200, 255, 0.5)
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 200)
        self.assertEqual(color.blue, 255)
        self.assertAlmostEqual(color.alpha, 0.5, places=2)
        color2 = Color.fromRGBA(100, 200, 255, 0.5)
        self.assertEqual(color, color2)

    def test_color_from_rgb(self):
        color = Color.fromRGB(100, 200, 255)
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 200)
        self.assertEqual(color.blue, 255)
        self.assertAlmostEqual(color.alpha, 1.0, places=2)
    
    def test_can_add_transparency_to_a_color(self):
        color = Color.fromRGBA(100, 200, 255, 0.1)
        transparent_color = color.with_transparency(0.5)
        self.assertAlmostEqual(transparent_color.alpha, 0.5, places=2)
        self.assertEqual(transparent_color.red, 100)
        self.assertEqual(transparent_color.green, 200)
        self.assertEqual(transparent_color.blue, 255)

    def test_can_solidify_a_color(self):
        color = Color.fromRGBA(100, 200, 255, 0.5)
        solid_color = color.solidify()
        self.assertAlmostEqual(solid_color.alpha, 1.0, places=2)
        self.assertEqual(solid_color.red, color.red)
        self.assertEqual(solid_color.green, color.green)
        self.assertEqual(solid_color.blue, color.blue)
    
    def test_painting_with_solid_color_replaces_the_old_one(self):
        color1 = Color.fromRGB(100, 200, 255)
        color2 = Color.fromRGB(50, 100, 150)
        combined_color = color2.paint_on(color1)
        self.assertAlmostEqual(combined_color.alpha, 1.0, places=2)
        self.assertEqual(combined_color.red, color2.red)
        self.assertEqual(combined_color.green, color2.green)
        self.assertEqual(combined_color.blue, color2.blue)

    def test_painting_with_transparency_blends_colors(self):
        color1 = Color.fromRGBA(100, 200, 255, 0.75)
        color2 = Color.fromRGB(50, 100, 150)
        blended_color = color1.paint_on(color2)
        self.assertAlmostEqual(blended_color.alpha, 1.0, places=2)
        self.assertEqual(blended_color.red, 87)  # ~ 100 * 0.75 + 50 * 0.25
        self.assertEqual(blended_color.green, 174)  # ~ 200 * 0.75 + 100 * 0.25
        self.assertEqual(blended_color.blue, 228)  # ~ 255 * 0.75 + 150 * 0.25
    
    def test_to_rgba_conversion(self):
        color = Color.fromRGBA(100, 200, 255, 0.5)
        rgba_tuple = color.to_RGBA()
        assertAlmostEqual(rgba_tuple, (100, 200, 255, 0.5), places=2)

    def test_to_hsla_conversion(self):
        color = Color.fromRGBA(24, 98, 118, 0.5)
        hsla_tuple = color.toHSLA()
        assertAlmostEqual(hsla_tuple, (192.8, 66.2, 27.9, 0.5), places=1)
    
    def test_from_hsla_conversion(self):
        color = Color.fromHSLA(192.8, 66.2, 27.9, 0.5)
        self.assertEqual(color.red, 24)
        self.assertEqual(color.green, 98)
        self.assertEqual(color.blue, 118)
        self.assertAlmostEqual(color.alpha, 0.5, places=2)

    def test_color_brightness(self):
        color = Color.fromRGB(100, 200, 255)
        brightened_color = color.with_brightness(0.5)
        self.assertEqual(brightened_color.red, 50)
        self.assertEqual(brightened_color.green, 100)
        self.assertEqual(brightened_color.blue, 127)
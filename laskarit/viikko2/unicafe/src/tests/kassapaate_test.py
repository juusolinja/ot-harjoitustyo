import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luodun_kassapaatteen_rahamaara_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
    
    def test_luodun_kassapaatteen_myydyt_lounaat_oikein(self):
        self.assertEqual(self.kassapaate.edulliset + self.kassapaate.maukkaat, 0)

    def test_edullinen_kateisostolla_kassa_ja_vaihtoraha_oikein_kun_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual((self.kassapaate.kassassa_rahaa, vaihtoraha), (100240, 10))

    def test_maukas_kateisostolla_kassa_ja_vaihtoraha_oikein_kun_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(450)
        self.assertEqual((self.kassapaate.kassassa_rahaa, vaihtoraha), (100400, 50))

    def test_myytyjen_lounaiden_maara_kasvaa_edullisilla_kun_kateismaksu_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_myytyjen_lounaiden_maara_kasvaa_maukkailla_kun_kateismaksu_riittava(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_riittamaton_kateismaksu_kasitellaan_oikein_edullisella_lounaalla(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        kassa = self.kassapaate.kassassa_rahaa
        edulliset = self.kassapaate.edulliset
        self.assertEqual((kassa, vaihtoraha, edulliset), (100000, 200, 0))

    def test_riittamaton_kateismaksu_kasitellaan_oikein_maukkaalla_lounaalla(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(200)
        kassa = self.kassapaate.kassassa_rahaa
        edulliset = self.kassapaate.maukkaat
        self.assertEqual((kassa, vaihtoraha, edulliset), (100000, 200, 0))

    def test_korttia_veloitetaan_oikein_kun_tarpeeksi_rahaa_ja_edullinen_lounas(self):
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual((self.maksukortti.saldo, onnistui), (760, True))

    def test_korttia_veloitetaan_oikein_kun_tarpeeksi_rahaa_ja_maukas_lounas(self):
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual((self.maksukortti.saldo, onnistui), (600, True))

    def test_jos_kortilla_tarpeeksi_rahaa_myytyjen_lounaiden_maara_kasvaa_edullisilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_jos_kortilla_tarpeeksi_rahaa_myytyjen_lounaiden_maara_kasvaa_maukkailla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_riittamaton_korttimaksu_kasitellaan_oikein_edullisella_lounaalla(self):
        kortti = Maksukortti(200)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual((kortti.saldo, self.kassapaate.edulliset, onnistui), (200, 0, False))

    def test_riittamaton_korttimaksu_kasitellaan_oikein_maukkaalla_lounaalla(self):
        kortti = Maksukortti(200)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual((kortti.saldo, self.kassapaate.maukkaat, onnistui), (200, 0, False))

    def test_kassan_rahamaara_ei_muutu_kortilla_edullista_lounasta_ostaessa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_rahamaara_ei_muutu_kortilla_maukasta_lounasta_ostaessa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_rahaa_ladattaessa_kortin_saldo_muuttuu_ja_kassa_kasvaa_ladatulla_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
        self.assertEqual((self.maksukortti.saldo, self.kassapaate.kassassa_rahaa), (2000, 101000))

    def test_negatiivista_summaa_ladattaessa_kortin_saldo_ja_kassa_ei_muutu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
        self.assertEqual((self.maksukortti.saldo, self.kassapaate.kassassa_rahaa), (1000, 100000))
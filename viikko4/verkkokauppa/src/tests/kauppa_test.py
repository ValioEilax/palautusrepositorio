import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote
import random

class TestKauppa(unittest.TestCase):
    def setUp(self):
        #Yhteinen alustus
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

        #palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42   

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "lähdevesi", 4)
            if tuote_id == 3:
                return Tuote(3, "maksamakkara", 2)
            
        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        
        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
    
    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_oikeat_argumentit_tilisiirto_ostoksen_jalkeen(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # Testi argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_kahden_saman_tuotteen_ostaminen_oikeat_argumentit(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # Testi argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_kahden_erilaisen_tuotteen_ostaminen_oikeat_argumentit(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        # Testi argumenteilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5 + 4
        )
        
    def test_aloita_uusi_ostos_nollaa_edellinen_ostos(self):
        # tehdään ensimmäiset ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # tehdään toiset ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        
        # Tarkastetaan että oikea hinta tilisiirrossa
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 4
        )

    def test_generoi_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        # Käydään läpi kolme ostostapahtumaa
        for _ in range(3):
            # Tehdään ostokset ja maksetaan
            self.kauppa.aloita_asiointi()
            self.kauppa.lisaa_koriin(1)
            self.kauppa.tilimaksu("pekka", "12345")

            # Tarkastetaan että viitegeneraattoria on kutsuttu odotetusti
            expected_call_count = _ + 1  # 1, 2, 3
            self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, expected_call_count)

    def test_poista_korista_tuotteen_poistaminen_korista(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
        "pekka", 42, "12345", "33333-44455", 0)
    
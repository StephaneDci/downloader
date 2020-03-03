# -*- coding: utf-8 -*-

import unittest
import html
from downloader.youtube_downloader import  RessourceYT, Youtube_Dl
from downloader import global_proxy
from unittest import mock


# ------------------------------------------------------------------------------------------------------
# Implémentation des Tests unitaires
# Auteur : SDI
# Date   : 15/02/2020
# Objectif : educationnal purpose only. Merci de respecter les copyrights.
# ------------------------------------------------------------------------------------------------------


class TestYoutubeDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.src= TestYoutubeDownloader.read_file_to_html("data/youtube_download_test_data.html")
        cls.YoutubeDl = Youtube_Dl("https://www.youtube.com/watch?v=HGp5UnNiLOA&list=PL4OLSC172x8p8Dy-A88_k_zhKRvpPwRgq")

    # Lecture des fichier html en utf8
    @staticmethod
    def read_file_to_html(filename):
        with open(filename) as f:
            h = f.read()
        return html.unescape(h)

    # --------------------------------------------------------------------------
    # Tests Classe RessourceFile
    # --------------------------------------------------------------------------
    def test_ressourcesYT(self):
        r1 = RessourceYT(link='https://www.youtube.com/watch?v=1', downloaded=True)
        r2 = RessourceYT(link='https://www.youtube.com/watch?v=1', downloaded=False)
        r3 = RessourceYT(link='https://www.youtube.com/watch?v=3')
        self.assertEqual(r1,r2)
        self.assertNotEqual(r2,r3)
        self.assertEqual(None, r1.titre)
        self.assertEqual(None, r2.length)

    # --------------------------------------------------------------------------
    # Tests Classe Downloader:
    # --------------------------------------------------------------------------

    @mock.patch('downloader.youtube_downloader.Youtube_Dl._get_srcpage')
    def test_get_youtube_vids_on_url(self, mockrequest):
        mockrequest.return_value = self.src
        rs = self.YoutubeDl.get_youtube_vids_on_url()
        self.assertIsInstance(rs, list)
        self.assertIsInstance(rs[0],RessourceYT)
        self.assertEqual(39, len(rs))
        self.assertIn(RessourceYT(link='https://www.youtube.com/watch?v=ua2WkSvmylw'), rs)


    @mock.patch('downloader.youtube_downloader.Youtube_Dl._get_srcpage')
    def test_get_youtube_vids_on_url_without_playlist(self, mockrequest):
        mockrequest.return_value = self.src
        yt = Youtube_Dl("https://www.youtube.com/watch?v=HGp5UnNiLOA")
        rs = yt.get_youtube_vids_on_url()
        self.assertIsInstance(rs, list)
        self.assertIsInstance(rs[0], RessourceYT)
        self.assertEqual(1, len(rs))
        self.assertEqual("https://www.youtube.com/watch?v=HGp5UnNiLOA", rs[0].link)


    def test_get_paramplaylist_from_url(self):
        self.assertEqual("PL4OLSC172x8p8Dy-A88_k_zhKRvpPwRgq", self.YoutubeDl._get_playlist_param_from_url())
        self.assertEqual("", Youtube_Dl("https://www.youtube.com/watch?v=HGp5UnNiLOA")._get_playlist_param_from_url())
        with self.assertRaises(Exception):
            self.assertEqual("", Youtube_Dl("https://www.youtube.com")._get_playlist_param._from_url())
            self.assertEqual("", Youtube_Dl("")._get_playlist_param_from_url())


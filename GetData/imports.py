# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 19:51:55 2024

@author: Francisco
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import argparse
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
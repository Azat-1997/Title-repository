import json
from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture
from TestSetUp import TestingClient

app = create_app_fixture("chem_client.py")

def test_glucose_case(app:ShinyAppProc, page: Page):
  client = TestingClient(app, page, "CO2 + H2O -> C6H12O6 + O2", "CO2;5\nH2O;1")
  client.equation_controller.expect_value("6CO2 + 6H2O -> C6H12O6 + 6O2")
  client.reagent_controller.expect_value("CO2: 2.443\nH2O: 1.0")
  client.product_controller.expect_value("C6H12O6: 1.667\nO2: 1.776")

  

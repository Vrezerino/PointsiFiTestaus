from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestPointsiFi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Alusta webdriver
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()

    def setUp(self):
        self.driver.get("https://pointsi.fi")

    def test_tyopaikkasivu_on_olemassa(self):
        print("Etusivun <title>: " + self.driver.title)

        tyonhakijalle_li = self.driver.find_element(By.XPATH, "//ul/li[2]")
        tyonhakijalle_li.click()

        self.assertIn(
            "Tuntuuko, että olet yksinäinen susi? Avoimet työpaikat Pointsilta",
            self.driver.title,
        )

    def test_testaajailmoitus_loytyy(self):
        tyonhakijalle_li = self.driver.find_element(By.XPATH, "//ul/li[2]")
        tyonhakijalle_li.click()

        # Ilmoituskortin otsikko
        testaaja_korttiotsikko = self.driver.find_element(
            By.XPATH, "//*[@data-id='375cd38']"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", testaaja_korttiotsikko
        )
        self.assertIsNotNone(testaaja_korttiotsikko)
        testaaja_korttiotsikko.click()

        wait = WebDriverWait(self.driver, 1)
        ilmoitusotsikko = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    "//h1[text()='Test Automation Engineer / Test Engineer – Liity huipputiimiimme!']",
                )
            )
        )
        self.assertIsNotNone(ilmoitusotsikko)

        print("Työpaikkailmoituksen <title>: " + self.driver.title)

    def test_koulutussivu_on_olemassa(self):
        print("Etusivun <title>: " + self.driver.title)

        koulutus_li = self.driver.find_element(By.XPATH, "//ul/li[3]")
        koulutus_li.click()

        self.assertIn(
            "Koulutukset - Pointsi",
            self.driver.title,
        )

    def test_ISO9001_koulutusilmoitus_loytyy(self):
        koulutus_li = self.driver.find_element(By.XPATH, "//ul/li[3]")
        koulutus_li.click()

        # Ilmoituskortin otsikko
        ISO9001_korttiotsikko = self.driver.find_element(
            By.XPATH, "//*[@data-id='cb945e4']"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", ISO9001_korttiotsikko
        )
        self.assertIsNotNone(ISO9001_korttiotsikko)
        ISO9001_korttiotsikko.click()

        wait = WebDriverWait(self.driver, 1)
        ilmoitusotsikko = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    "//h1[text()='ISO9001 vaatimukset, sisäinen auditointi ja laatutyökalut, 2 pv, lähi ja etätoteutus']",
                )
            )
        )
        self.assertIsNotNone(ilmoitusotsikko)

        print("Koulutusilmoituksen <title>: " + self.driver.title)

    def test_ISO9001_koulutukseen_voi_ilmoittautua(self):
        koulutus_li = self.driver.find_element(By.XPATH, "//ul/li[3]")
        koulutus_li.click()

        ISO9001_korttiotsikko = self.driver.find_element(
            By.XPATH, "//*[@data-id='cb945e4']"
        )
        ISO9001_korttiotsikko.click()

        ### Ilmoittautumislomake ###

        # Harhaanjohtava id, pitäisi olla esim. "kokonimi"
        nimikentta = self.driver.find_element(By.ID, "form-field-etunimi")
        nimikentta.send_keys("Etunimi Sukunimi")

        # Väärä id, pitäisi olla esim. "form-field-alennuskoodi"
        alennuskoodikentta = self.driver.find_element(By.ID, "form-field-sukunimi")
        alennuskoodikentta.send_keys("#1234")

        # Pitäisi olla "form-field_d1f64ae" tai ihan vaan "form-field-puhelinnumero"
        puhelinnumerokentta = self.driver.find_element(
            By.ID, "form-field-field_d1f64ae"
        )
        puhelinnumerokentta.send_keys("000 0000000")

        emailkentta = self.driver.find_element(By.ID, "form-field-email")
        emailkentta.send_keys("000 0000000")

        lisatietokentta = self.driver.find_element(By.ID, "form-field-message")
        lisatietokentta.send_keys("Abc 123")

        lomake = self.driver.find_element(By.ID, "koulutuslomake")

        # Testaa että lomakkeen lähetys toimii ilman että tietoja oikeasti lähetetään
        self.driver.execute_script(
            """
            const lomake = arguments[0];
            lomake.onsubmit = function(event) {
              event.preventDefault();
              console.log('Lomakkeen lähetys toimii');
            };
          """,
            lomake,
        )

        lomake.submit()
        print("Lomakkeen tiedot 'lähetetty'")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

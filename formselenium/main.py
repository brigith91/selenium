from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://demoqa.com/register")
    return driver


def datos_registro(driver):
    print("===========DATOS REGISTRO ========")
    print("\n llenando el nombre | firstname")
    driver.find_element(By.ID, "firstname").send_keys("Lina")
    sleep(1)
    print("\n llenando el apellido | lastname")
    driver.find_element(By.ID, "lastname").send_keys("Roncancio")
    sleep(1)
    print("\n llenando el usuario | userName")
    driver.find_element(By.ID, "userName").send_keys("Brigith")  
    sleep(1)
    print("\n llenando el password | password")
    driver.find_element(By.ID, "password").send_keys("Lina2016*") 
    sleep(1)


def click_captcha(driver):
    print("\n Haciendo clic en el CAPTCHA 'No soy un robot'")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//iframe[contains(@src, 'google.com/recaptcha')]")
        )
    )
    # espera específicamente a que el recaptcha-anchor sea clickeable
    captcha_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
    )
    captcha_checkbox.click() # Clic en el CAPTCHA, esperando intervención manual.
    sleep(10)  # Tiempo para resolver el captcha manualmente
    driver.switch_to.default_content() # Volviendo al contenido principal después del CAPTCHA.


def click_register_button(driver):
    print("\n Haciendo clic en el botón de Registro")
    try:
        # Esperar a que el botón de registro sea clickeable, lo que significa que no está cubierto.
        register_button = WebDriverWait(driver, 15).until(  # Aumentamos la espera a 15 segundos
            EC.element_to_be_clickable((By.ID, "register"))
        )
        register_button.click()
        print("Botón de registro clicado con éxito.")
        sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.url_changes("https://demoqa.com/register"))
        sleep(2)

    except Exception as e:
        print(f"Error al hacer clic en el botón de registro: {e}")
        print("Intentando hacer clic con JavaScript como alternativa.")
        # Si la espera de clickeabilidad falla, intentamos hacer clic con JavaScript
        driver.execute_script(
            "arguments[0].click();", driver.find_element(By.ID, "register"))
        print("Clic en el botón de registro realizado con JavaScript.")
        sleep(2)  # esperar después del clic con JS, Intentar esperar la redirección nuevamente después del clic con JS
        try:
            WebDriverWait(driver, 10).until(
                EC.url_changes("https://demoqa.com/register"))
            print("Redirección detectada después de clic con JavaScript.")
        except:
            print( "No se detectó una redirección inmediata después del registro con JavaScript.")
        sleep(2) 


def iniciar_sesion(driver, username, password):
    print("\n Iniciando sesión...")
    # Verificar si ya estamos en la página de login, si no, navegar a ella.
    if "login" not in driver.current_url:
        print("No estamos en la página de login, navegando a ella...")
        driver.get("https://demoqa.com/login")
        sleep(2)

    print(f"Llenando usuario: {username}")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userName"))
    ).send_keys(username)
    sleep(1)

    print(f"Llenando contraseña: {password}")
    driver.find_element(By.ID, "password").send_keys(password)
    sleep(1)

    print("Haciendo clic en el botón de Login")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login"))
    ).click()
    sleep(5)  # Esperar a que la página de perfil cargue


def stop_driver(driver):
    print("\n Cerrando el navegador.")
    driver.quit()


def main():
    driver = start_driver()

    username = "Brigith"
    password = "Lina2016*"

    datos_registro(driver)
    driver.save_screenshot("00_datos_llenos.png")

    click_captcha(driver)
    driver.save_screenshot("01_captcha_resuelto.png")

    click_register_button(driver)
    driver.save_screenshot("02_despues_de_registro.png")

    iniciar_sesion(driver, username, password)
    driver.save_screenshot("03_despues_de_login.png")

    stop_driver(driver)


if __name__ == "__main__":
    main()

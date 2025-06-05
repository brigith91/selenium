from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://demoqa.com/dynamic-properties")
    return driver


def verificar_dynamic_properties(driver):

    # 1. Captura estado inicial
    print("estado inicial.")
    sleep(3)
    driver.save_screenshot("01_estado_inicial.png")

    # 2. Esperar a que se habilite el botón 'Will enable 5 seconds'
    try:
        print("Esperar que el botón 'Will enable 5 seconds' se habilite.")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "enableAfter"))
        )
        print("Botón habilitado.")
        sleep(3)
        driver.save_screenshot("02_boton_habilitado.png")
    except:
        print("El botón no se habilitó.")
        driver.save_screenshot("02_error_boton_no_habilitado.png")

    # 3. Verificar color del botón que cambia
    try:
        color_button = driver.find_element(By.ID, "colorChange")
        color_value = color_button.value_of_css_property("color")
        print(f"Color actual del botón: {color_value}")
        sleep(3)
        driver.save_screenshot("03_boton_color_change.png")
    except:
        print("No se pudo obtener el color.")
        driver.save_screenshot("03_error_color.png")

    # 4. Verificar visibilidad del botón 'Visible After 5 Seconds'
    try:
        print("Esperar que el botón 'Visible After 5 Seconds' sea visible.")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "visibleAfter"))
        )
        print("Botón visible.")
        sleep(3)
        driver.save_screenshot("04_boton_visible.png")
    except:
        print("El botón no apareció.")
        driver.save_screenshot("04_error_boton_no_visible.png")


def stop_driver(driver):
    print(" Cerrando navegador...")
    driver.quit()


def main():
    driver = start_driver()
    verificar_dynamic_properties(driver)
    print("Captura final ")
    driver.save_screenshot("05_final_completo.png")
    stop_driver(driver)


if __name__ == "__main__":
    main()



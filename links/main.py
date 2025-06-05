from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time


def marcar_elemento(driver, element, mensaje):
    # Inserta un borde rojo y un mensaje visible al pasar el mouse
    driver.execute_script(
        "arguments[0].style.border='3px solid red'; arguments[0].title=arguments[1];",
        element, mensaje
    )


def validar_y_marcar_links(driver):
    elementos = driver.find_elements(By.TAG_NAME, "a")
    for i, elemento in enumerate(elementos, start=1):
        url = elemento.get_attribute("href")
        if url:
            try:
                respuesta = requests.head(url, timeout=5)
                if respuesta.status_code >= 400:
                    print(f" Roto link {i}: {url}")
                    marcar_elemento(driver, elemento,
                                    f"Link roto: {respuesta.status_code}")
                else:
                    print(f" Válido link {i}: {url}")
            except Exception as e:
                print(f" Link {i} error: {url}")
                marcar_elemento(driver, elemento, "Error al validar link")
        else:
            print(f" Link {i} sin URL válida")
            marcar_elemento(driver, elemento, "No tiene href")


def validar_y_marcar_imagenes(driver):
    imagenes = driver.find_elements(By.TAG_NAME, "img")
    for i, imagen in enumerate(imagenes, start=1):
        src = imagen.get_attribute("src")
        if src:
            try:
                respuesta = requests.head(src, timeout=5)
                if respuesta.status_code >= 400:
                    print(f" Rota imagen {i}: {src}")
                    marcar_elemento(
                        driver, imagen, f"Imagen rota: {respuesta.status_code}")
                else:
                    print(f" Válida imagen {i}: {src}")
            except Exception as e:
                print(f" Imagen {i} error: {src}")
                marcar_elemento(driver, imagen, "Error al validar imagen")
        else:
            print(f" Imagen {i} sin src")
            marcar_elemento(driver, imagen, "No tiene src")


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get("https://demoqa.com/broken")

    time.sleep(3)  # Esperar a que cargue

    validar_y_marcar_imagenes(driver)
    validar_y_marcar_links(driver)

    print(" Verificar el navegador para ver los errores.")
    time.sleep(15)  # Espera para ver el resultado
    driver.quit()


if __name__ == "__main__":
    main()

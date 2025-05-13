import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password

email = valid_email
password = valid_password

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

def test_show_all_pets(driver):
    # вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)

    driver.implicitly_wait(10)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_count_my_pets(driver):
    wait = WebDriverWait(driver, 5)
    assert wait.until(EC.visibility_of_element_located((By.ID, 'email')))
    assert wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    # Переходим на страницу мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')


    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    print(pets_number)
    pets_count = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr")
    assert int(pets_number) == len(pets_count)

def test_half_pets_has_photo(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    #Проверяем, что у половины питомцев есть фото
    images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > th > img')
    names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td')
    images_count = 0
    list_names = []
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    for i in range(len(pets_count)):
        list_names.append(names[i].text)
        if images[i].get_attribute('src') != '':
            images_count += 1
        else:
            images_count += 0
    if len(pets_count) == 0:
        print("No pets")
    else:
        assert images_count / len(pets_count) >= 0.5

def test_pets_has_attributes(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td')
    breeds = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-of-type(2)')
    ages = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-of-type(3)')

    for i in range(len(names)):
        assert names[i].text != '', "Отсуствует Атрибут"
        assert breeds[i].text != '', "Отсуствует Атрибут"
        assert ages[i].text != '', "Отсуствует Атрибут"

def test_pets_has_unique_names(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')
    pet_names = []
    for pet in pets:
        name_element = pet.find_element(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td')
        pet_names.append(name_element.text)

    unique_names = set(pet_names)
    assert len(unique_names) == len(pet_names), "Обнаружены повторяющиеся имена питомцев"

def test_unique_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу мои питомцы
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Находим все строки таблицы
    pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')

    # Собираем данные каждого питомца как кортеж (имя, порода, возраст)
    pet_data = []
    for pet in pets:
        cells = pet.find_elements(By.TAG_NAME, 'td')
        if len(cells) >= 3:  # Проверяем, что есть все три столбца
            name = cells[0].text.strip()
            breed = cells[1].text.strip()
            age = cells[2].text.strip()
            pet_data.append((name, breed, age))

    # Проверяем, что все питомцы уникальны
    assert len(pet_data) == len(set(pet_data)), "В списке есть повторяющиеся питомцы"
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from groups import get_exact_group
import undetected_chromedriver as uc
from telebot import TeleBot

bot = TeleBot(token='second bot token here')


def selenium_whatsapp_get_site(user_id, msg, geo):
    options = webdriver.ChromeOptions()
    options.add_argument('--headers')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(r"--user-data-dir=Default")
    driver = uc.Chrome(options=options)
    driver.get('https://web.whatsapp.com')
    print('Поиск qr кода')
    time.sleep(8)
    try:
        loading_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Загрузка чатов')]")
        bot.send_message(user_id, 'Загрузка чатов\nПодождите следующего уведомления от этого бота')
        time.sleep(secs=300)
        bot.send_message(user_id, 'Вернитесь в бота и нажмите \start')
    except Exception as e:
        try:
            qr_code_element = driver.find_element(By.XPATH,
                                                  '//canvas[@aria-label="Scan this QR code to link a device!"]')
            qr_code_screenshot = qr_code_element.screenshot_as_png
            bot.send_photo(user_id, photo=qr_code_screenshot,
                           caption='Отсканируйте QR код и вернитесь в основной бот и начините заново через /start')
        except Exception:
            print('Пользователь уже залогинен')
            try:
                time.sleep(1.5)
                groups = get_exact_group(geo=geo)
                print(groups)
                for group in groups:
                    try:
                        time.sleep(1)
                        search_box = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Текстовое поле поиска']"))
                        )
                        time.sleep(1)
                        search_box.click()
                        js_input_search = """
                        var elm = arguments[0], txt = arguments[1];
                        elm.focus();  

                        document.execCommand("insertText", false, txt);

                        elm.dispatchEvent(new Event('input', { bubbles: true }));
                        elm.dispatchEvent(new Event('change', { bubbles: true }));
                        elm.dispatchEvent(new Event('keydown', { bubbles: true }));
                        elm.dispatchEvent(new Event('keyup', { bubbles: true }));
                        """
                        driver.execute_script(js_input_search, search_box, group)
                        search_box.send_keys(Keys.RETURN)
                        print(f"Текст '{group}' успешно введён и поиск выполнен!")

                        group_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{group}')]"))
                        )
                        group_element.click()
                        print(f"Элемент '{group}' найден и нажат успешно!")
                        group_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{group}')]"))
                        )
                        group_element.click()
                        print(f"Элемент '{group}' найден и нажат через JS!")
                        try:
                            time.sleep(5)
                            message_input = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Введите сообщение']"))
                            )
                            message_input.click()
                            for char in msg:
                                js_input_msg = """
                                                    var elm = arguments[0], txt = arguments[1];
                                                    elm.focus();  

                                                    document.execCommand("insertText", false, txt);

                                                    elm.dispatchEvent(new Event('input', { bubbles: true }));
                                                    elm.dispatchEvent(new Event('change', { bubbles: true }));
                                                    elm.dispatchEvent(new Event('keydown', { bubbles: true }));
                                                    elm.dispatchEvent(new Event('keyup', { bubbles: true }));
                                                    """
                                driver.execute_script(js_input_msg, message_input, char)
                                time.sleep(0.2)
                            message_input.send_keys(Keys.RETURN)
                            time.sleep(1.5)
                            close_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="x-alt"]')))
                            close_button.click()
                            print("Сообщение успешно отправлено!")
                        except Exception as e:
                            print(f'Ошибка при вводе сообщения: {e}')
                    except Exception as e:
                        print(f'Ошибка при поиске группы {group}: {e}')
                        krestik = driver.find_element(By.XPATH, "//span[@data-icon='x-alt']")
                        krestik.click()
                        continue
                bot.send_message(user_id, 'Рассылка окончена, можете дальше пользоваться ботом')
            except Exception as e:
                print(f'Ошибка при взаимодействии с интерфейсом: {e}')
            finally:
                driver.quit()
                print('Драйвер закрыт')
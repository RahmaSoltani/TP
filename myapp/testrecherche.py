
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.example.com")
search_box = driver.find_element_by_id("search-box")
search_box.send_keys("article")
search_button = driver.find_element_by_id("search-button")
search_button.click()
results = driver.find_elements_by_class_name("search-result")
if len(results) > 0:
    print("La recherche a réussi. Des articles ont été trouvés.")
else:
    print("La recherche n'a pas retourné de résultats.")

# Fermer le navigateur
driver.quit()
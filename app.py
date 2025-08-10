import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

st.title("TikTok Live Shopping Extractor")

# User inputs
live_url = st.text_input("Enter TikTok Live URL (e.g., https://www.tiktok.com/@example/live)", "https://www.tiktok.com/@example/live")
email = st.text_input("TikTok Email (for login, if needed)")
password = st.text_input("TikTok Password", type="password")

if st.button("Extract Shopping Basket"):
    with st.spinner("Scraping... This may take a moment."):
        try:
            # Set up Selenium
            options = Options()
            options.add_argument("--headless")  # Run headless for efficiency
            options.add_argument("--no-sandbox")  # Needed for some environments
            options.add_argument("--disable-dev-shm-usage")  # For cloud stability
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Open the page
            driver.get(live_url)
            time.sleep(5)

            # Handle login if credentials provided
            if email and password:
                try:
                    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
                    login_button.click()
                    time.sleep(2)
                    email_input = driver.find_element(By.NAME, "email")
                    email_input.send_keys(email)
                    password_input = driver.find_element(By.NAME, "password")
                    password_input.send_keys(password)
                    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                    submit_button.click()
                    time.sleep(5)
                except Exception as e:
                    st.warning(f"Login issue: {e}")

            # Click shopping bag and extract products
            shopping_bag = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".shopping-bag-icon, .cart-icon")))  # Adjust selector
            shopping_bag.click()
            time.sleep(3)

            products = driver.find_elements(By.CSS_SELECTOR, ".product-item")  # Adjust to match elements
            product_list = []
            for product in products:
                name = product.find_element(By.CSS_SELECTOR, ".product-name").text
                price = product.find_element(By.CSS_SELECTOR, ".product-price").text
                product_list.append(f"{name} - {price}")

            driver.quit()

            if product_list:
                st.success("Products found:")
                for item in product_list:
                    st.write(item)
            else:
                st.info("No products found or extraction failed.")
        except Exception as e:
            st.error(f"Error: {e}")

import time
from selenium import webdriver
import pandas as pd


def convert_staked_amount(amount_string):
    if amount_string[-1] == 'M':
        final_amount = float(amount_string.replace('M', '')) * 1000000
        return final_amount
    if amount_string[-1] == 'K':
        final_amount = float(amount_string.replace('K', '')) * 1000
        return final_amount


url = 'https://atomscan.com/terra2/validators/'
read_validators_list = pd.read_csv('operator_addresses.csv')
browser = webdriver.Chrome('C:\\Users\\Zanyar\\Downloads\\chromedriver.exe')
browser.get(url)
browser.maximize_window()
time.sleep(0.5)
base_query = ""

for i in range(130):
    element = browser.find_element_by_xpath(
        f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[2]/span/span/a")
    operator_address = str(element.get_attribute('href'))[39:]
    validator_name = element.get_attribute('title')
    # print(validator_name)
    # print(operator_address)

    validator_commission = browser.find_elements_by_xpath \
        (f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i + 1}]")[0].text.splitlines()
    commission = validator_commission[0].split()[-2].replace('%', '')
    # print(float(commission))

    voting_power = browser.find_elements_by_xpath \
        (f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[7]")[0].text
    voting_power = float(voting_power.replace('%', ''))

    staked_amount = browser.find_elements_by_xpath \
        (f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[6]")[0].text
    staked_amount = staked_amount.split()[0]
    staked_amount = convert_staked_amount(amount_string=staked_amount)
    # print(staked_amount)

    status = browser.find_elements_by_xpath \
        (f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i + 1}]/td[5]/span")[0].text
    # print(status)
    if i < 129:
        base_query += f"select '{operator_address}' as operator_address, '{validator_name}' as validator_name," \
                      f" {staked_amount} as staked_amount, {voting_power} as voting_power, {commission} as commission," \
                      f" '{status}' as status\n union all\n"
    if i == 129:
        base_query += f"select '{operator_address}' as operator_address, '{validator_name}' as validator_name," \
                      f" {staked_amount} as staked_amount, {voting_power} as voting_power, {commission} as commission," \
                      f" '{status}' as status\n"
    print(f"validator {i+1} saved!")

f = open("validators_from_atomscan.sql", "w", encoding="utf-8")
f.write(base_query)
f.close()


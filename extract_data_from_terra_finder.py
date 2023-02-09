import time
from selenium import webdriver
import pandas as pd

base_url = 'https://finder.terra.money/mainnet/validator/'
read_validators_list = pd.read_csv('operator_addresses.csv')
base_query = ""
for i in read_validators_list.index:

    operator_address = read_validators_list['OPERATOR_ADDRESS'][i]

    url_on_terra_finder = base_url + operator_address

    browser = webdriver.Chrome('C:\\Users\\Zanyar\\Downloads\\chromedriver.exe')
    browser.get(url_on_terra_finder)
    browser.maximize_window()
    time.sleep(25)

    name_and_status = browser.find_elements_by_class_name('Header_moniker__ALDVD')[0].text.splitlines()

    validator_specifications_2 = browser.find_elements_by_class_name("card-body")[1].text.splitlines()

    validator_specifications_1 = browser.find_elements_by_class_name("card-body")[0].text.splitlines()

    voting_power = float(validator_specifications_1[1].replace('%', ''))

    staked_amount_number = validator_specifications_1[2].replace(' Luna', '')
    staked_amount_number = float(staked_amount_number.replace(',', ''))

    self_delegation_amount = validator_specifications_1[5].replace(' Luna', '')
    self_delegation_amount = float(self_delegation_amount.replace(',', ''))

    commission = float(validator_specifications_1[7].replace('%', ''))

    if i < len(read_validators_list) - 1:
        base_query += f"select '{name_and_status[0]}' as validator_name, '{name_and_status[1]}' as status," \
                      f" '{validator_specifications_2[1]}' as operator_address, '{validator_specifications_2[3]}' as" \
                      f"account_address, {voting_power} as voting_power," \
                      f" {staked_amount_number} as staked_amount, {self_delegation_amount} as self_delegation_amount" \
                      f", {commission} as  commission\nunion all\n "

    else:
        base_query += f"select '{name_and_status[0]}' as validator_name, '{name_and_status[1]}' as status," \
                      f" '{validator_specifications_2[1]}' as operator_address, '{validator_specifications_2[3]}' as" \
                      f"account_address, {voting_power} as voting_power," \
                      f" {staked_amount_number} as staked_amount, {self_delegation_amount} as self_delegation_amount" \
                      f", {commission} as  commission"

f = open("validator_details_terra_finder.sql", "w", encoding="utf-8")
f.write(base_query)
f.close()

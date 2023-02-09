import pandas as pd

validators_list_from_terra_finder = pd.read_excel("validators_list_from_terra_finder.xlsx")
validators_list_from_atom_scan = pd.read_excel("validators_list_from_atom_scan.xlsx")

base_query = ""

for i in validators_list_from_atom_scan.index:
    for j in validators_list_from_terra_finder.index:
        if validators_list_from_atom_scan['OPERATOR_ADDRESS'][i] == \
                validators_list_from_terra_finder['OPERATOR_ADDRESS'][j]:

            validator_name = validators_list_from_atom_scan['VALIDATOR_NAME'][i]
            operator_address = validators_list_from_atom_scan['OPERATOR_ADDRESS'][i]
            staked_amount = round(validators_list_from_atom_scan['STAKED_AMOUNT'][i], 1)
            voting_power = validators_list_from_atom_scan['VOTING_POWER'][i]
            status = validators_list_from_atom_scan['STATUS'][i]
            commission = validators_list_from_atom_scan['COMMISSION'][i]

            account_address = validators_list_from_terra_finder['ASACCOUNT_ADDRESS'][j]
            self_delegation_amount = validators_list_from_terra_finder['SELF_DELEGATION_AMOUNT'][j]

            if i < 129:
                base_query += f"select '{validator_name}' as validator_name, '{operator_address}' as operator_address, " \
                              f"'{account_address}' as account_address, {staked_amount} as staked_amount," \
                              f" {voting_power} as voting_power, {self_delegation_amount} as self_delegation_amount," \
                              f" {commission} as commission, '{status}' as status\nunion all\n "
            if i == 129:
                base_query += f"select '{validator_name}' as validator_name, '{operator_address}' as operator_address, " \
                              f"'{account_address}' as account_address, {staked_amount} as staked_amount," \
                              f" {voting_power} as voting_power, {self_delegation_amount} as self_delegation_amount," \
                              f" {commission} as commission, '{status}' as status\n"

f = open("active_validators.sql", "w", encoding="utf-8")
f.write(base_query)
f.close()

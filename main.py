import requests
import json
import pandas as pd
from bot import get_auth_token


def scrape(url, no_variants):
    try:
        try:
            print('Extracting token from "access_token.txt"')
            try:
                with open('access_token.txt', 'r') as file:
                    for line in file:
                        if line.lower().startswith('authorization:'):
                            access_token = line.split(': ', 1)[1].strip()
            except FileNotFoundError as errr:
                print('File Not Found:- "access_token.txt"')
                print('Please restart the script!')
                exit()

            headers = {
                'Authorization': access_token,
            }
            response = requests.get(url, headers=headers)
            raw_json = response.json()
            json_data = json.dumps(raw_json)
            json_data = json.loads(json_data)
            data = json_data['data']
        except KeyError as e:
            access_token = json_data['token']
            updated_headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url, headers=updated_headers)
            raw_json = response.json()
            json_data = json.dumps(raw_json)
            json_data = json.loads(json_data)
            data = json_data['data']

        product_details = data['aeop_ae_product_s_k_us']['aeop_ae_product_sku']
        output = []
        # extracted attributed
        if no_variants:
            for product in product_details:
                output.append([product['sku_price']])
        else:
            for product in product_details:
                product_sku_code = product['sku_code']
                product_variant_sku_code = product['id']
                cost = product['sku_price']
                price = cost
                variant_columns = product['aeop_s_k_u_propertys']['aeop_sku_property']

                output.append([product_sku_code, product_variant_sku_code, cost, price, variant_columns])

        return output

    except KeyError as er:
        print('Token needs to be refreshed')


def main(sales_order_number, sales_variant_option_name, url):
    # get all product details for given url
    try:
        print(f'Starting scrapping for url - {product_url}')
        if sales_variant_option_name:
            product_details = scrape(url, False)
        else:
            product_details = scrape(url, True)
    except KeyError as err:
        get_auth_token()
        print(f'Restarting scrapping for url - {product_url}')
        if sales_variant_option_name:
            product_details = scrape(url, False)
        else:
            product_details = scrape(url, True)

    if sales_variant_option_name:
        sales_variant_option_name = sales_variant_option_name.lower()
        b_column = sales_variant_option_name.split(', ')

        counter = 0
        output = []
        variants = []
        duplicates = []
        for product in product_details:

            variant = ""
            values = []
            for i in range(len(product[4])):
                value = product[4][i]['sku_property_value']
                value = value.lower()
                values.append(value)
                variant += product[4][i]['sku_property_value']
                variant += " "

            if variant in variants:
                duplicates.append(variant)
            else:
                variants.append(variant)

            if product[1] == None or product[1] == '':
                none_flag = 'No Variant Names'
            else:
                none_flag = ''

            b_column.sort()
            values.sort()

            if b_column == values:
                B = sales_variant_option_name
                D = sales_variant_option_name
                E = product[1]
            else:
                B = ''
                D = ''
                E = ''

            data = {
                    'Sales Order Number': sales_order_number,                                           # A
                    'Sales Variant Option Name': B,                                                     # B
                    'Product URL': product_url,                                                         # C
                    'Match "Sales Variant Option Name" and retrieve Dsers Product Variant Name(s)': D,  # D
                    'Match "Sales Variant Option Name" and retrieve Dsers Product SKU Code': E,         # E
                    'All Possible Dsers Product SKU Code': product[0].lower(),                          # F
                    'All Dsers Product Variant SKU Codes': product[1],                                  # G
                    'Dsers Cost $': product[2],                                                         # H
                    'Dsers Price $': product[3],                                                        # I
                    'Duplicate variant names in Dser (all variant columns)': variant,                   # J
                    'Dsers No Variants': none_flag                                                      # K
            }

            counter += 1
            print(f'Collecting product:- {counter}')
            output.append(data)

        for product in output:
            if product['Duplicate variant names in Dser (all variant columns)'] in duplicates:
                product['Duplicate variant names in Dser (all variant columns)'] = 'Duplicate Names'
            else:
                product['Duplicate variant names in Dser (all variant columns)'] = ''

    # No variant name
    else:
        print('No Variant names for this product')
        output = []
        for product in product_details:
            data = {
                    'Sales Order Number': sales_order_number,                                                   # A
                    'Sales Variant Option Name': sales_variant_option_name,                                     # B
                    'Product URL': product_url,                                                                 # C
                    'Match "Sales Variant Option Name" and retrieve Dsers Product Variant Name(s)': '<none>',   # D
                    'Match "Sales Variant Option Name" and retrieve Dsers Product SKU Code': '<none>',          # E
                    'All Possible Dsers Product SKU Code': '<none>',                                            # F
                    'All Dsers Product Variant SKU Codes': '<none>',                                            # G
                    'Dsers Cost $': product[0],                                                                 # H
                    'Dsers Price $': product[0],                                                                # I
                    'Duplicate variant names in Dser (all variant columns)': '',                                # J
                    'Dsers No Variants': 'No Variant Names'                                                     # K
            }
        output.append(data)

    return output


if __name__ == "__main__":
    BASE_URL = 'https://ac.dsers.com/api/v1/prod/ali?url='

    # provided attributes
    details = [
        ['987654', 'RED', 'https://www.aliexpress.com/item/1005005231485559.html'],
        ['123', 'Warm White, DC12V', 'https://www.aliexpress.com/item/32859100702.html'],
        ['456', 'For GoPro', 'https://www.aliexpress.com/item/10000377765814.html'],
        ['46', '1 SET', 'https://www.aliexpress.com/item/1005003591027724.html'],
        ['554546', 'China', 'https://www.aliexpress.com/item/4000401603675.html'],
        ['1465', '19-21mm', 'https://www.aliexpress.com/item/1005003676275417.html'],
        ['12121', 'APMT1604 M2 VP15TF, 10PCS(1BOX)', 'https://www.aliexpress.com/item/1005003335129185.html'],
        ['134564', '', 'https://www.aliexpress.com/item/32883178767.html?spm=a2g0o.order_list.order_list_main.60.21ef1802u6BABo']
    ]

    data = []
    for obj in details:
        sales_order_number = obj[0]
        sales_variant_option_name = obj[1]
        product_url = obj[2]
        url = BASE_URL + product_url
        try:
            with open('access_token.txt', 'r') as file:
                print('Found "access_token.txt"')
        except FileNotFoundError as err:
            print('File Not Found:- "access_token.txt"')
            get_auth_token()
            print('New Token Saved')

        output = main(sales_order_number, sales_variant_option_name, url)
        for dic_obj in output:
            data.append(dic_obj)

    print('All data collected saving into "output.xlsx"')
    df = pd.DataFrame(data)
    output_file = 'output.xlsx'
    df.to_excel(output_file, index=False)
    print('All data saved successfully.')


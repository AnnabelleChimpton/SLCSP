# Author: Annabelle Wright, 2024

import sys, csv


# Takes an input csv file of zipcodes and associated areas, and returns a dictionary mapping zipcodes
# to a tuple (STATE_CODE, RATE_AREA). See 'Considerations' section in README.md file for more information
# about this section.
def open_zip_codes_and_build_dictionary(csv_zip_file_path: str) -> dict:
    zipcode_dictionary = {}

    with open(csv_zip_file_path, 'r') as f:
        lines = f.readlines()

        # Declaring these variables to set for the appropriate column based on the first line of the csv_zip_file.
        zipcode_index = 0
        state_index = 0
        rate_area_index = 0
        initial_line = lines[0].strip().split(',')
        for i in range(0, len(initial_line)):
            if initial_line[i] == 'zipcode':
                zipcode_index = i
            elif initial_line[i] == 'state':
                state_index = i
            elif initial_line[i] == 'rate_area':
                rate_area_index = i

        for i in range(1, len(lines)):
            cleaned_line = lines[i].strip().split(',')
            state_rate_area_tuple = (cleaned_line[state_index], cleaned_line[rate_area_index])

            if cleaned_line[zipcode_index] not in zipcode_dictionary.keys():
                zipcode_dictionary[cleaned_line[zipcode_index]] = state_rate_area_tuple
            else:
                # Logic for determining if there is only one zipcode per rate area
                if state_rate_area_tuple != zipcode_dictionary[cleaned_line[zipcode_index]]:
                    zipcode_dictionary[cleaned_line[zipcode_index]] = None

    return zipcode_dictionary


# Takes an input csv file of plans and returns a dictionary of the following structure:
# {(STATE_CODE, RATE_AREA): {
#       'Bronze': [RATE1, RATE2, ..],
#       'Silver': [RATE1, RATE2, ..],
#       'Gold': [RATE1, RATE2, ..],
#       'Platinum': [RATE1, RATE2, ..],
#       'Catastrophic': [RATE1, RATE2, ..],
# }}
def open_plans_and_build_dictionary(csv_plans_file_path: str) -> dict:
    plans_dictionary = {}

    with open(csv_plans_file_path, 'r') as f:
        lines = f.readlines()

        # Declaring these variables to set for the appropriate column based on the first line of the csv_plans_file.
        state_index = 0
        metal_level_index = 0
        rate_index = 0
        rate_area_index = 0
        initial_line = lines[0].strip().split(',')
        for i in range(0, len(initial_line)):
            if initial_line[i] == 'state':
                state_index = i
            elif initial_line[i] == 'metal_level':
                metal_level_index = i
            elif initial_line[i] == 'rate':
                rate_index = i
            elif initial_line[i] == 'rate_area':
                rate_area_index = i

        for i in range(1, len(lines)):
            cleaned_line = lines[i].strip().split(',')
            state_rate_area_tuple = (cleaned_line[state_index], cleaned_line[rate_area_index])

            if state_rate_area_tuple not in plans_dictionary.keys():
                plans_dictionary[state_rate_area_tuple] = {}
                plans_dictionary[state_rate_area_tuple][cleaned_line[metal_level_index]] = [cleaned_line[rate_index]]
            else:
                if cleaned_line[metal_level_index] not in plans_dictionary[state_rate_area_tuple].keys():
                    plans_dictionary[state_rate_area_tuple][cleaned_line[metal_level_index]] = [cleaned_line[rate_index]]
                else:
                    plans_dictionary[state_rate_area_tuple][cleaned_line[metal_level_index]].append(cleaned_line[rate_index])
            # if cleaned_line[zipcode_index] not in zipcode_dictionary.keys():
            #     zipcode_dictionary[cleaned_line[zipcode_index]] = [(cleaned_line[state_index], cleaned_line[rate_area_index])]
            # else:
            #     # Logic for determining if there is only one zipcode per rate area
            #     zipcode_dictionary[cleaned_line[zipcode_index]].append((cleaned_line[state_index], cleaned_line[rate_area_index]))

    return plans_dictionary


# Takes the input zip codes from the slcsp.csv file, and outputs the second lowest cost silver plan or nothing if
# there is not a valid plan available. This function also outputs the results into an .csv file passed in as an
# argument.
def process_slcsp_file(slcsp_csv_file: str, zipcode_dictionary: dict, plans_csv_file: dict, output_csv_path: str) -> None:
    csv_file = open(output_csv_path, 'w', newline='')
    with open(slcsp_csv_file, 'r') as f:
        lines = f.readlines()

        # Declaring this variable to set for the appropriate column based on the first line of the slcsp_file.
        zipcode_index = 0
        initial_line = lines[0].strip().split(',')
        for i in range(0, len(initial_line)):
            if initial_line[i] == 'zipcode':
                zipcode_index = i

        # DictWriter is used to output the data to the specified .csv file.
        output_writer = csv.DictWriter(csv_file, fieldnames=['zipcode', 'rate'])
        output_writer.writeheader()
        print('zipcode,rate')

        for i in range(1, len(lines)):
            cleaned_line = lines[i].strip().split(',')
            zipcode = cleaned_line[zipcode_index]
            if zipcode in zipcode_dictionary.keys():
                state_rate_area_tuple = zipcode_dictionary[zipcode]
                if state_rate_area_tuple is not None and state_rate_area_tuple in plans_csv_file.keys():
                    slcsp_tuple = get_slcsp_rate(plans_csv_file[state_rate_area_tuple])
                    if slcsp_tuple[0]:
                        print(str(zipcode) + ',' + f'{float(slcsp_tuple[1]):.2f}')
                        output_writer.writerow({'zipcode': str(zipcode), 'rate': f'{float(slcsp_tuple[1]):.2f}'})
                    else:
                        print(str(zipcode) + ',')
                        output_writer.writerow({'zipcode': str(zipcode)})
                else:
                    print(str(zipcode) + ',')
                    output_writer.writerow({'zipcode': str(zipcode)})
            else:
                print(str(zipcode) + ',')
                output_writer.writerow({'zipcode': str(zipcode)})


# Returns a tuple with values (boolean, float) where the boolean is if there is a valid slcsp rate and the float is
# the rate (or 0 if no valid rate)
def get_slcsp_rate(rates: dict)-> tuple:
    if 'Silver' not in rates.keys():
        return False, 0
    else:
        silver_rates = list(set(rates['Silver']))
        silver_rates.sort()
        if len(silver_rates) <= 1:
            return False, 0
        else:
            return True, silver_rates[1]


if __name__ == '__main__':
    slcsp_csv_file = sys.argv[1]
    zips_csv_file = sys.argv[2]
    plans_csv_file = sys.argv[3]
    output_csv_file = sys.argv[4]

    zipcode_dictionary = open_zip_codes_and_build_dictionary(zips_csv_file)
    plans_dictionary = open_plans_and_build_dictionary(plans_csv_file)

    process_slcsp_file(slcsp_csv_file, zipcode_dictionary, plans_dictionary, output_csv_file)


## Calculating the Second Lowest Cost Silver Plan
#### **Author**: Annabelle Wright, 2024

### Prequisites
* **Python 3.11** (This code was built and tested in Python 3.11, older versions may run but cannot be 
guaranteed)

### Introduction
The program `slcsp.py` computes the second lowest cost silver plan (SLCP) given a list
of zip codes and a list of plans.

Run this program using the following command:

`python3 slcsp.py ./slcsp/slcsp.csv ./slcsp/zips.csv ./slcsp/plans.csv ./output.csv`

The program accepts the following four required arguments:

* **slcsp.csv file**: This file contains a list of the zip codes for which you want to compute
    the SLCP.
* **zips.csv**: This file is a table of the information needed to compute which zipcode goes
    with each state and rate area. (See ** Additional Considerations** section for limitations and constraints)
* **plans.csv**: This file is a table of the information needed to compute which rates for each level
  of a plan go with the appropriate State, Rate area tuple. 
* **output.csv**: This file path denotes where you would like to save your output from running this program.
  By default, output will be printed to stdout as well.

This project also includes a unit testing file, `testrunner.py`. You can run the included test suite
using the following command:

`python3 testrunner.py -v`


## Additional Considerations
To focus on the explicit requirements of this program, there are a few decisions that were made in order to
keep the logic simpler and more straightforward.

In the function `open_zip_codes_and_build_dictionary(csv_zip_file_path: str) -> dict`, 
I made the decision to deal with any ambiguous ZIPCODE: (STATE, RATE_AREA) by setting the value to `None`. 
I followed this pattern to keep the data structure as simple as possible and maintain low complexity.
The following cases are ambiguous according to my assumptions of the given problem:
* If a zipcode has more than one rate_area per state
* If a zipcode has more than one state associated with it

The second decision that I made was to output the results to stdout as well as a defined csv file. Because
of the language in the requirements stating 'Fill in the second column', I interpreted this as asking for the
.csv file itself to be generated. The overhead on adding in this functionality was not too complex.


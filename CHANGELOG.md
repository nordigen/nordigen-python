# Changelog

## [1.4.1] - 2024-10-22

- Added account_selection parameter for POST /api/v2/requisitions

## [1.4.0] - 2024-02-09

- Update base URL form ob.gocardless.com to bankaccountdata.gocardless.com

## [1.3.2] - 2023-06-21

- Update URLs to represent GoCardless

## [1.3.1] - 2023-03-13

- Add the response in the response kwargs when instantiating the `HTTPError`

## [1.3.0] - 2022-08-15

- Add Premium endpoints
- Add default base url
- Update types

## [1.2.0] - 2022-07-21

- Add default timeout for requests, allow it to be changed
- Make country argument optional for `get_institutions` method to allow getting all institutions at once

## [1.1.0] - 2022-05-03

- Add date_filter for transaction endpoint
- Set client token property on token exchange

## [1.0.1] - 2022-01-13

- Update documentation
- Fix token setter
- Move `python-dotenv` to dev dependencies

## [1.0.0] - 2022-01-12

- Initial release

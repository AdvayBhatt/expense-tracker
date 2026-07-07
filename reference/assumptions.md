transfers and refunds will be a part of the bank's usage, so it should be included for this project

the process of selecting specific fields is:

'account_id'
 'account_owner'
 'amount'
 'authorized_date' 					# not needed for our analysis of spending; date is enough
 'authorized_datetime' 				# not needed for our analysis of spending; date is enough
 'category' 						# not needed since older Plaid taxonomy that personal_finance_category replaces
 'category_id' 						# not needed as complement of legacy category
 'check_number'
 'counterparties' 					# not needed
 'date'								# want to see spending habits as they change from day to night; prioritize datetime then see this if null
 'datetime'							
 'iso_currency_code' 				# not needed
 'location':
	- 'address'
	- 'city'
    - 'country'
    - 'lat'
    - 'lon'
    - 'postal_code'
    - 'region'
    - 'store_number'
 'logo_url' 						# not needed
 'merchant_entity_id'				# not needed
 'merchant_name'					# Plaid's clean version of the merchant name
 'name'								# fallback in-case merchant_name is null
 'payment_channel'
 'payment_meta':                    # not needed too granular for our analysis
	- 'by_order_of'
	- 'payee'
	- 'payer'
	- 'payment_method'
    - 'payment_processor'
    - 'ppd_id'
    - 'reason'
    - 'reference_number'
 'pending'
 'pending_transaction_id'
 'personal_finance_category':
	- 'confidence_level'
	- 'detailed'						
	- 'primary'							# would prefer more detail
	- 'version' 						# not needed this is metadata about taxonomy
 'personal_finance_category_icon_url' 	# not needed?
 'transaction_code' 					# not needed mostly null for consumers
 'transaction_id'
 'transaction_type'
 'unofficial_currency_code'   			# not needed
 'website'								# not needed



TRIMMED

 'account_id'
 'amount'
 'date'
 'datetime'
 'location':
	- 'address'
	- 'city'
    - 'country'
    - 'lat'
    - 'lon'
    - 'postal_code'
    - 'region'
    - 'store_number'
 'merchant_name'	
 'name'
 'payment_channel'
 'pending'
 'personal_finance_category':
	- 'confidence_level'
	- 'detailed'
	- 'primary'
 'transaction_id'
 'transaction_type'
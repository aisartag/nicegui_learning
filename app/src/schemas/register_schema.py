from typing import Self

from pydantic import BaseModel, EmailStr, Field, ValidationError, model_validator


class RegisterSchema(BaseModel):
	username: str = Field(..., min_length=3)
	email: EmailStr
	password: str = Field(..., min_length=3)  # DA CORREGGERE 8==========================================
	confirm_password: str

	@model_validator(mode='after')
	def check_passwords_match(self) -> Self:
		# self contiene i dati già validati singolarmente
		if self.password != self.confirm_password:
			# Associamo l'errore specificamente al campo 'confirm_password'
			raise ValueError('Passwords do not match.')
		return self


# ERROR_MESSAGES = {
# 	'missing': 'This field is required.',
# 	'string_too_short': 'Too short. Minimum length is {limit_value} characters.',
# }

# it-IT
ERROR_MESSAGES = {
	'missing': 'Campo obbligatorio.',
	'string_too_short': 'La lunghezza minima è di {limit_value} caratteri.',  # 'Too short. Minimum length is {limit_value} characters.',
}


def get_clean_errors(e: ValidationError) -> dict[str, str]:
	# return {error['loc'][0]: error['msg'] for error in e.errors()}  # type: ignore

	clean_errors = {}

	for error in e.errors():  # type: ignore
		field_name = error['loc'][0] if len(error['loc']) > 0 else 'confirm_password'
		error_type = error['type']

		if error_type == 'string_too_short':
			limit = error.get('ctx', {}).get('min_length', '')
			msg = ERROR_MESSAGES['string_too_short'].format(limit_value=limit)
		elif field_name == 'email' and error_type == 'value_error':
			msg = (
				'Digitare un indirizzo email valido.'  # "Please enter a valid email address (e.g., name@example.com)."
			)
		elif error_type == 'value_error' and 'passwords do not match' in error.get('msg', '').lower():
			msg = 'Le password non corrispondono. Riprovare.'  # " #"Passwords do not match. Please re-enter."
			field_name = 'confirm_password'
		else:
			msg = ERROR_MESSAGES.get(error_type, error['msg'])

		clean_errors[field_name] = msg

	return clean_errors  # type: ignore

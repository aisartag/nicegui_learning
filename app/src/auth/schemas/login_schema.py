from pydantic import BaseModel, EmailStr, Field, ValidationError


class LoginSchema(BaseModel):
	email: EmailStr
	password: str = Field(..., min_length=1)


# ERROR_MESSAGES = {
# 	'missing': 'This field is required.',
# 	'string_too_short': 'Too short. Minimum length is {limit_value} characters.',
# }

# it-IT
ERROR_MESSAGES = {
	'missing': 'Campo obbligatorio.',
	# 'string_too_short': 'Campo obbligatorio.',
}


def get_clean_errors(e: ValidationError) -> dict[str, str]:
	# return {error['loc'][0]: error['msg'] for error in e.errors()}  # type: ignore

	clean_errors = {}

	for error in e.errors():
		field_name = error['loc'][0]
		error_type = error['type']

		if error_type == 'missing':
			msg = ERROR_MESSAGES['missing']
		elif field_name == 'email' and error_type == 'value_error':
			msg = 'Digitare un indirizzo email valido.'
		elif error_type == 'string_too_short' and field_name == 'password':
			msg = ERROR_MESSAGES['missing']
		else:
			msg = ERROR_MESSAGES.get(error_type, error['msg'])

		clean_errors[field_name] = msg

	return clean_errors  # type: ignore

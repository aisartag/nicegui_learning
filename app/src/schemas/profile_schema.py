from typing import Union

from pydantic import BaseModel, Field, ValidationError


class ProfileSchema(BaseModel):
	bio: Union[str, None] | str = Field(max_length=300)


ERROR_MESSAGES = {
	'missing': 'Campo obbligatorio.',
	'string_too_long': 'La lunghezza massima è di {limit_value} caratteri.',
}


def get_clean_errors(e: ValidationError) -> dict[str, str]:
	# return {error['loc'][0]: error['msg'] for error in e.errors()}  # type: ignore

	clean_errors = {}

	for error in e.errors():
		field_name = error['loc'][0]
		error_type = error['type']

		if error_type == 'string_too_long':
			limit = error.get('ctx', {}).get('max_length', '')
			msg = ERROR_MESSAGES['string_too_long'].format(limit_value=limit)
		else:
			msg = ERROR_MESSAGES.get(error_type, error['msg'])

		clean_errors[field_name] = msg

	return clean_errors  # type: ignore

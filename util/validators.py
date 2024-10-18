import re
from datetime import date
from typing import Any


def add_error(field_name: str, msg: str, errors: dict) -> bool:
    if errors.get(field_name) is None:
        errors[field_name] = []
    errors[field_name].append(msg)


def is_in_range(
    field_value: int | float,
    field_name: str,
    field_label: str,
    low: int | float,
    high: int | float,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if low <= field_value <= high:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve estar entre {low} e {high}.",
            errors,
        )
        return False


def is_not_none(
    field_field_value: Any, field_name: str, field_label: str, errors: dict
) -> bool:
    if field_field_value is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> não pode ser nulo.",
            errors,
        )
        return False


def is_not_empty(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if field_value.strip() != "":
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> não pode ser vazio.",
            errors,
        )
        return False


def is_size_between(
    field_value: str,
    field_name: str,
    field_label: str,
    min_size: int,
    max_size: int,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if min_size <= len(field_value) <= max_size:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ter entre {min_size} e {max_size} caracteres.",
            errors,
        )
        return False


def is_size_equals(
    field_value: str,
    field_name: str,
    field_label: str,
    size: int,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if len(field_value) == size:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ter {size} caracteres.",
            errors,
        )
        return False


def is_max_size(
    field_value: str, field_name: str, field_label: str, max_size: int, errors: dict
) -> bool:
    if not field_value:
        return True
    if len(field_value) <= max_size:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ter no máximo {max_size} caracteres.",
            errors,
        )
        return False


def is_min_size(
    field_value: str, field_name: str, field_label: str, min_size: int, errors: dict
) -> bool:
    if not field_value:
        return True
    if len(field_value) >= min_size:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ter no mínimo {min_size} caracteres.",
            errors,
        )
        return False


def is_matching_regex(
    field_value: str, field_name: str, field_label: str, regex: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(regex, field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> está com o formato incorreto.",
            errors,
        )
        return False


def is_email(field_value: str, field_name: str, field_label: str, errors: dict) -> bool:
    if not field_value:
        return True
    if (
        re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            field_value,
        )
        is not None
    ):
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um e-mail com formato válido.",
            errors,
        )
        return False


def is_cpf(field_value: str, field_name: str, field_label: str, errors: dict) -> bool:
    if not field_value:
        return True
    if re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um CPF válido.",
            errors,
        )
        return False


def is_cnpj(field_value: str, field_name: str, field_label: str, errors: dict) -> bool:
    if not field_value:
        return True
    if re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um CNPJ válido.",
            errors,
        )
        return False


def is_phone_number(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(r"^\(\d{2}\) \d{5}-\d{4}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um telefone no formato (99) 99999-9999.",
            errors,
        )
        return False


def is_cep(field_value: str, field_name: str, field_label: str, errors: dict) -> bool:
    if not field_value:
        return True
    if re.match(r"^\d{5}-\d{3}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um CEP válido.",
            errors,
        )
        return False


def is_person_name(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(r"^[a-zA-ZÀ-ú']{2,40}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um nome válido.",
            errors,
        )
        return False


def is_person_fullname(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if (
        re.match(r"^[a-zA-ZÀ-ú']{2,40}(?:\s[a-zA-ZÀ-ú']{2,40})+$", field_value)
        is not None
    ):
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um nome completo válido.",
            errors,
        )
        return False


def is_own_name(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(r"^[\w]+(\s[\w]+)*$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um nome válido.",
            errors,
        )
        return False


def is_password(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    """
    Tenha pelo menos um caractere minúsculo.
    Tenha pelo menos um caractere maiúsculo.
    Tenha pelo menos um dígito.
    Tenha pelo menos um caractere especial dentre os especificados (@$!%*?&).
    Tenha um comprimento de pelo menos 4 e no máximo 64 caracteres.
    """
    if not field_value:
        return True
    if (
        re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{4,64}$",
            field_value,
        )
        is not None
    ):
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser uma senha válida entre 4 e 64 caracteres, contendo caracteres maiúsculos, minúsculos, dígitos e caracteres especiais (@#$!%*?&).",
            errors,
        )
        return False


def is_matching_fields(
    field_value: str,
    field_name: str,
    field_label: str,
    matching_field_value: str,
    matching_field_label: str,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value.strip() == matching_field_value.strip():
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser igual ao do campo {matching_field_label}.",
            errors,
        )
        return False


def is_selected_id_valid(
    field_value: int, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if field_value > 0:
        return True
    else:
        add_error(
            field_name,
            f"Selecione uma opção para o campo <b>{field_label}</b>.",
            errors,
        )
        return False


def is_greater_than(
    field_value: int | float,
    field_name: str,
    field_label: str,
    min_value: int | float,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value > min_value:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser maior que {min_value}.",
            errors,
        )
        return False


def is_less_than(
    field_value: int | float,
    field_name: str,
    field_label: str,
    max_value: int | float,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value < max_value:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser menor que {max_value}.",
            errors,
        )
        return False


def is_greater_than_or_equal(
    field_value: int | float,
    field_name: str,
    field_label: str,
    min_value: int | float,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value >= min_value:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser maior ou igual a {min_value}.",
            errors,
        )
        return False


def is_less_than_or_equal(
    field_value: int | float,
    field_name: str,
    field_label: str,
    max_value: int | float,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value <= max_value:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser menor ou igual a {max_value}.",
            errors,
        )
        return False


def is_date_between(
    field_value: date,
    field_name: str,
    field_label: str,
    min_date: date,
    max_date: date,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if min_date <= field_value <= max_date:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve estar entre {min_date.strftime('%d/%m/%Y')} e {max_date.strftime('%d/%m/%Y')}.",
            errors,
        )
        return False


def is_date_greater_than(
    field_value: date,
    field_name: str,
    field_label: str,
    min_date: date,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value > min_date:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser maior que {min_date.strftime('%d/%m/%Y')}.",
            errors,
        )
        return False


def is_date_less_than(
    field_value: date,
    field_name: str,
    field_label: str,
    max_date: date,
    errors: dict,
) -> bool:
    if not field_value:
        return True
    if field_value < max_date:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser menor que {max_date.strftime('%d/%m/%Y')}.",
            errors,
        )
        return False


def is_only_digits(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(r"^\d+$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve conter apenas dígitos.",
            errors,
        )
        return False


def is_only_letters_or_space(
    field_value: str, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if re.match(r"^[a-zA-ZÀ-ú\s]+$", field_value) is not None:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve conter apenas letras ou espaços.",
            errors,
        )
        return False


def is_positive_integer(
    field_value: int, field_name: str, field_label: str, errors: dict
) -> bool:
    if not field_value:
        return True
    if field_value > 0:
        return True
    else:
        add_error(
            field_name,
            f"O valor do campo <b>{field_label}</b> deve ser um número inteiro positivo.",
            errors,
        )
        return False


# data normalization
def capitalize_own_names(name: str) -> str:
    name = name.lower()
    ignoreds = ["de", "da", "do", "di", "das", "com", "dos"]
    words = name.split()
    capitalized_words = [
        word.capitalize() if word.lower() not in ignoreds else word.lower()
        for word in words
    ]
    return " ".join(capitalized_words)

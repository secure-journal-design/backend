from django.core.exceptions import ValidationError

def validate_title(value: str) -> None:
    if len(value) < 3:
        raise ValidationError('Title must be at least 3 characters long.')
    
def validate_body(value: str) -> None:
    if len(value) < 3:
        raise ValidationError('Body must be at least 3 characters long.')

def validate_topic(value: str) -> None:
    if len(value) < 3:
        raise ValidationError('Topic must be at least 3 characters long.')

from django.core.exceptions import ValidationError

def validate_title(value: str) -> None:
    if len(value) < 5:
        raise ValidationError('Title must be at least 5 characters long.')
    
def validate_body(value: str) -> None:
    if len(value) < 20:
        raise ValidationError('Body must be at least 20 characters long.')
    if len(value) > 1000:
        raise ValidationError('Body must be at most 1000 characters long.')

def validate_topic(value: str) -> None:
    if len(value) < 3:
        raise ValidationError('Topic must be at least 3 characters long.')
    
def validate_subheading(value: str) -> None:
    if len(value) < 5:
        raise ValidationError('Subheading must be at least 5 characters long.')


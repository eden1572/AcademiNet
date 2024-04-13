from django.core.exceptions import ValidationError

def validate_file_extension(filename):
    valid_extensions = ['.pdf', '.png', '.docx']
    if not any(filename.endswith(ext) for ext in valid_extensions):
        raise ValidationError(f"Invalid file extension: {filename}")

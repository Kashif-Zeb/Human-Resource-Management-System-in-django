from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)
class validations:
    @staticmethod
    def no_space(key):
        def validation(value: str):
            logger.info(f"Validating {key} with value: '{value}'")
            if isinstance(value.startswith(" "),str):
                logger.error(f"{key} starts with white space")
                raise serializers.ValidationError(f"{key} cannot start with white space")
            if value.endswith(" "):
                logger.error(f"{key} ends with white space")
                raise serializers.ValidationError(f"{key} cannot end with white space")
        return validation
        
    @staticmethod
    def salary_range(key):
        def validation(value):
            if not isinstance(value,dict) or "minimum" not in value or "maximum" not in value:
                raise serializers.ValidationError("salary_range must be a dictionary with 'minimum' and 'maximum' keys.")
            if value["minimun"] < 1 or value["maximum"] > 99999999:
                raise serializers.ValidationError("minimum value cannot be less than 1 and maximum value can't be greater than 99999999")
            if value["minimun"] > value["maximum"]:
                raise serializers.ValidationError("minimum value cannot be greater than maximum value")
        return validation
    
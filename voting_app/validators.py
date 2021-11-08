from rest_framework import serializers


def answers_unique_validator(values_list):
    if len(values_list) != len(set(values_list)):
        raise serializers.ValidationError('The answers must be unique!')

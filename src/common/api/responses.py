from decimal import Decimal

from ninja import Schema
from phonenumbers import PhoneNumber


class PhoneNumberSchema(PhoneNumber):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v.is_valid():
            raise TypeError("invalid phone")
        return v.as_international


class CurrencySchema(Schema):
    code: str


class MoneySchema(Schema):
    amount: Decimal
    currency: CurrencySchema

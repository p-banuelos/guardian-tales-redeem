import os
from classes.GuardianTales import GuardianTales

guardian_tales = GuardianTales(os.getenv('user_id'))

def list_and_redeem():
    coupons = guardian_tales.list_codes()
    for coupon in coupons:
        guardian_tales.redeem(coupon)

if __name__ == "__main__":
    list_and_redeem()

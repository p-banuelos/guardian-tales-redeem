import os
from helpers.GuardianTales import GuardianTales

def main():
    guardian_tales = GuardianTales(os.getenv('user_id'))
    coupons = guardian_tales.list_codes()
    for coupon in coupons:
        guardian_tales.redeem(coupon)

if __name__ == "__main__":
    main()

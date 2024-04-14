import os
from helpers.GuardianTales import GuardianTales

def main():
    guardian_tales = GuardianTales(
        user_id=os.environ.get('user_id'),
        region='EU'
    )
    for coupon in guardian_tales.list_codes():
        guardian_tales.redeem(coupon)

if __name__ == "__main__":
    main()
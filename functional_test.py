import motorpy
import os


def test_run_script():
    auth = motorpy.Auth(
        api_key=os.environ.get("API_KEY"),
        api_secret=os.environ.get("API_SECRET"),
    )

    with motorpy.Motor(org_id=os.environ.get("ORG_ID"),
                       auth=auth,
                       url=os.environ.get("API_URL")) as motor:
        driver = motor.get_driver("b4b31e00-1ee2-4ad4-bb64-4e7574c96444")
        print(driver)
        bas = driver.list_billing_accounts()
        print(bas)
        primary_ba = driver.get_primary_billing_account()
        print(primary_ba)


if __name__ == "__main__":
    test_run_script()

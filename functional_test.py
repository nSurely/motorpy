import motorpy
import time
import datetime


def test_run_script():
    auth = motorpy.Auth(
        api_key="",
        api_secret="",
    )

    with motorpy.Motor(org_id='',
                       auth=auth,
                       url="") as motor:

        print(f"\n{'*'*20}\n Listing Drivers \n{'*'*20}\n")
        drivers = [
            d for d in motor.list_drivers(
                first_name=motorpy.Search("joe", "ilike"),
                last_name=motorpy.Search("biden", "ilike"),
                dob=motorpy.Search(datetime.date(1942, 11, 20), "eq"),
                max_records=10
            )
        ]
        for d in drivers:
            print(d.id, d.first_name, d.last_name, d.date_of_birth)

        print(f"\n{'*'*20}\n Fetching Driver \n{'*'*20}\n")
        driver = motor.get_driver(drivers[0].id)
        print(driver)

        print(f"\n{'*'*20}\n Listing Driver Billing Account \n{'*'*20}\n")
        bas = driver.list_billing_accounts()
        print(bas)

        print(f"\n{'*'*20}\n Fetching Driver Primary Billing Account \n{'*'*20}\n")
        primary_ba = driver.get_primary_billing_account()
        print(primary_ba)

        print(f"\n{'*'*20}\n Fetching Drivers Fleets \n{'*'*20}\n")
        fleets = driver.list_fleets(full=True)
        print(fleets)
        for fleet in fleets:
            print(fleet.id, fleet.name)

        print(f"\n{'*'*20}\n{'*'*20}\n Fleets \n{'*'*20}\n")
        fleets = [f for f in motor.list_fleets(max_records=10)]
        print(fleets)
        for fleet in fleets:
            print(fleet.id, fleet.display, fleet.get_tags(), fleet.get_display('fr'), fleet.get_description('ar'))

            if fleet.has_parent():
                parent = fleet.get_parent()
                print("parent", parent.id, parent.display)
        
        current_fleet = fleets[0]
        old = current_fleet.display
        new = "Fleet 1"
        print(f"\n{'*'*20}\n Updating Fleet \n{'*'*20}\n")
        print(f"old: {old}, new: {new}")
        current_fleet.update(display=new)
        print(current_fleet.display, current_fleet.display == new)
        current_fleet.save()
        print("saved")
        time.sleep(1)
        current_fleet.refresh()
        print(current_fleet.display, current_fleet.display == new)
        current_fleet.update(display=old)
        current_fleet.refresh()


if __name__ == "__main__":
    test_run_script()

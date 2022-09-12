from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_curreny(currency="USD")
        # bot.select_place_to_go(input("Where you want to go? "))
        # bot.select_dates(check_in_date=input("What is the check in date? (2022-09-20) "),
        #                  check_out_date=input("What is the check out date? (2022-09-20) "))
        # bot.select_adult(int(input("How many people? ")))
        bot.select_place_to_go("Bali")
        bot.select_dates(check_in_date="2022-09-20",
                         check_out_date="2022-09-28")
        bot.select_adult(4)
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh() #refresh first before take the data
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from Command Line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '   set PATH=%PATH$;C:\path-to-your-folder \n'
            'Linux: \n'
            '   PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise

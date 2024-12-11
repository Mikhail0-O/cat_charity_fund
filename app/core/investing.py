from datetime import datetime


def the_logic_of_investing(all_uninvested_projects, new_donation):
    for project in all_uninvested_projects:
        donation_change = (
            new_donation.full_amount - new_donation.invested_amount
        )
        project_change = project.full_amount - project.invested_amount

        if donation_change >= project_change:
            new_donation.invested_amount += project_change
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.now()
        else:
            project.invested_amount += donation_change
            new_donation.invested_amount = new_donation.full_amount
            new_donation.fully_invested = True
            new_donation.close_date = datetime.now()
            break
from models.case import Case

class CaseController:
    def __init__(self):
        self.table_name = "case_records"

    def search_case(self, search_criteria, search_query):
        if search_criteria == "Case Number":
            return Case.search_by_case_number(search_query, self.table_name)
        else:
            return Case.search_by_case_title(search_query, self.table_name)

    def add_new_case(self, case_data):
        # Implement the logic to add a new case
        pass

    def update_cases(self, case_data):
        Case.update_case_data(case_data, self.table_name)

    def get_todays_cases(self):
        return Case.get_todays_case_list(self.table_name)

    def get_cases_by_date(self, selected_date):
        return Case.get_cases_by_date(selected_date, self.table_name)

    def get_pending_cases(self):
        return Case.get_pending_cases(self.table_name)

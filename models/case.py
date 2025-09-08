from .database import get_connection
from datetime import date

class Case:

    @staticmethod
    def add_case(case_data):
        sheets_service = get_connection()
        return sheets_service.add_case(case_data)

    # @staticmethod
    # def case_number_exists(case_number, location, table_name):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #     cur.execute(f"SELECT 1 FROM {table_name} WHERE case_number = %s AND location = %s", (case_number, location, table_name))
    #     exists = cur.fetchone() is not None
    #     cur.close()
    #     conn.close()
    #     return exists

    @staticmethod
    def case_number_exists(case_number, location, table_name):
        sheets_service = get_connection()
        return sheets_service.case_number_exists(case_number, location)


    @staticmethod
    def search_by_case_number(case_number, table_name):
        sheets_service = get_connection()
        return sheets_service.search_by_case_number(case_number)

    @staticmethod
    def search_by_case_title(case_title, table_name):
        sheets_service = get_connection()
        return sheets_service.search_by_case_title(case_title)

    # @staticmethod
    # def case_number_exists(case_number, location, table_name):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #     cur.execute(f"SELECT 1 FROM {table_name} WHERE case_number = %s AND location = %s", (case_number, location))
    #     exists = cur.fetchone() is not None
    #     cur.close()
    #     conn.close()
    #     return exists

    @staticmethod
    def get_cases_by_date(selected_date, table_name):
        sheets_service = get_connection()
        return sheets_service.get_cases_by_date(selected_date)

    @staticmethod
    def get_todays_case_list(table_name):
        sheets_service = get_connection()
        return sheets_service.get_todays_case_list()

    @staticmethod
    def get_pending_cases(table_name):
        sheets_service = get_connection()
        return sheets_service.get_pending_cases()

    @staticmethod
    def update_case_data(case_id, upcoming_date, table_name):
        sheets_service = get_connection()
        return sheets_service.update_case_data(case_id, upcoming_date)
        # conn = get_connection()
        # cur = conn.cursor()
        # for _, row in case_data.iterrows():
        #     update_query = f"""
        #         UPDATE {table_name} SET
        #             case_number = %s,
        #             case_title = %s,
        #             case_type = %s,
        #             location = %s,
        #             company_name = %s,
        #             upcoming_date = %s,
        #             previous_dates = %s,
        #             stage = %s,
        #             remarks = %s,
        #             status = %s,
        #             claimant_advocate_name = %s,
        #             claimant_advocate_mobile_number = %s
        #         WHERE id = %s
        #     """
        #     cur.execute(update_query, (
        #         row["Case Number"], row["Case Title"], row["Case Type"], row["Location"],
        #         row["Company Name"], row["Upcoming Date"], row["Previous Dates"], row["Stage"],
        #         row["Remarks"], row["Status"], row["Claimant Advocate Name"],
        #         row["Claimant Advocate Mobile Number"], row["ID"]
        #     ))
        #
        # conn.commit()
        # cur.close()
        # conn.close()

    @staticmethod
    def search_by_company_name(company_name, table_name):
        sheets_service = get_connection()
        return sheets_service.search_by_company_name(company_name)
    
    @staticmethod
    def get_case_by_number_or_title(search_query, table_name):
        sheets_service = get_connection()
        return sheets_service.get_case_by_number_or_title(search_query)

    @staticmethod
    def update_case(case_id, case_data, table_name):
        sheets_service = get_connection()
        return sheets_service.update_case(case_id, case_data)
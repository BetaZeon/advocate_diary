from .database import get_connection
from datetime import date

class Case:

    @staticmethod
    def add_case(case_data):
        conn = get_connection()
        cur = conn.cursor()
        insert_query = """
            INSERT INTO case_records (
                case_number, case_title, case_type, location, company_name, 
                upcoming_date, stage, remarks, status, 
                claimant_advocate_name, claimant_advocate_mobile_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        parameters = (
            case_data["case_number"], case_data["case_title"], case_data["case_type"], case_data["location"], 
            case_data["company_name"], case_data["upcoming_date"], case_data["stage"], case_data["remarks"], 
            case_data["status"], case_data["claimant_advocate_name"], case_data["claimant_advocate_mobile_number"]
        )
        cur.execute(insert_query, parameters)
        conn.commit()
        cur.close()
        conn.close()

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
        conn = get_connection()
        cur = conn.cursor()
        # Safely include table_name using f-string and use parameterized query for other variables
        cur.execute(f"SELECT 1 FROM {table_name} WHERE case_number = %s AND location = %s", (case_number, location))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists


    @staticmethod
    def search_by_case_number(case_number, table_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE case_number = %s", (case_number,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def search_by_case_title(case_title, table_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE case_title ILIKE %s", ('%' + case_title + '%',))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

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
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE upcoming_date = %s", (selected_date,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_todays_case_list(table_name):
        today = date.today()
        return Case.get_cases_by_date(today, table_name)

    @staticmethod
    def get_pending_cases(table_name):
        today = date.today()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE upcoming_date <= %s", (today,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def update_case_data(case_id, upcoming_date, table_name):
        conn = get_connection()  # Assuming get_connection() is defined to connect to your PostgreSQL DB
        cur = conn.cursor()

        # Fetch the existing upcoming_date and previous_dates
        fetch_query = f"""
                SELECT upcoming_date, previous_dates
                FROM {table_name}
                WHERE id = %s
            """
        cur.execute(fetch_query, (case_id,))
        result = cur.fetchone()

        if result is not None:
            current_upcoming_date, previous_dates = result

            # Convert previous_dates to a list
            if previous_dates:
                previous_dates_list = previous_dates.split(", ")
            else:
                previous_dates_list = []

            # Check if the upcoming date is in the previous dates list
            if str(current_upcoming_date) not in previous_dates_list:
                previous_dates_list.append(str(current_upcoming_date))

            # Check if the new upcoming date is not already in the previous dates list
            if str(upcoming_date) in previous_dates_list:
                return "The upcoming date is already present in the previous dates list."

            # Update the previous_dates and upcoming_date columns
            update_query = f"""
                    UPDATE {table_name} SET
                        upcoming_date = %s,
                        previous_dates = %s
                    WHERE id = %s
                """
            cur.execute(update_query, (
                upcoming_date,
                ", ".join(previous_dates_list),
                case_id
            ))

            conn.commit()
            cur.close()
            conn.close()

            return "Case updated successfully."
        else:
            cur.close()
            conn.close()
            return "Case not found."
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

    def search_by_company_name(company_name, table_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE company_name ILIKE %s", ('%' + company_name + '%',))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    
    @staticmethod
    def get_case_by_number_or_title(search_query, table_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE case_number = %s OR case_title ILIKE %s", (search_query, f"%{search_query}%"))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def update_case(case_id, case_data, table_name):
        conn = get_connection()
        cur = conn.cursor()
        update_query = f"""
            UPDATE {table_name} SET
                case_number = %s, case_title = %s, case_type = %s, location = %s,
                company_name = %s, upcoming_date = %s, stage = %s, remarks = %s,
                status = %s, claimant_advocate_name = %s, claimant_advocate_mobile_number = %s
            WHERE id = %s
        """
        cur.execute(update_query, (
            case_data["case_number"], case_data["case_title"], case_data["case_type"],
            case_data["location"], case_data["company_name"], case_data["upcoming_date"],
            case_data["stage"], case_data["remarks"], case_data["status"],
            case_data["claimant_advocate_name"], case_data["claimant_advocate_mobile_number"],
            case_id
        ))
        conn.commit()
        cur.close()
        conn.close()
        return "Case updated successfully."
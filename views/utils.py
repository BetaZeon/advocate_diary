import streamlit as st
from models.database import get_connection
from controllers.case_controller import CaseController
import config_loader
import pandas as pd
def go_to_main_page_button():
    st.button("Go to Main Page", on_click=lambda: st.session_state.update(page="home"))

def update_case_dates(case_id, upcoming_date, table_name="case_records"):
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

def update_cases_and_previous_dates(self, edited_df, selected_date):
    if edited_df is not None:
        if "df_value" in st.session_state:
            # Create an instance of CaseController to call its methods
            controller = CaseController()
            # Update cases in the database
            update_status = ""
            for _, row in edited_df.iterrows():
                case_id = row['ID']  # Replace 'ID' with the actual column name for case IDs
                new_upcoming_date = row['Upcoming Date']  # Replace 'Upcoming Date' with the actual column name for upcoming dates
                update_status = controller.update_cases(case_id, new_upcoming_date)  # Use the instance to call the method

            # Refresh the case data after update
            updated_cases = controller.get_cases_by_date(selected_date)  # Fetch updated data
            if updated_cases:
                st.session_state.df_value = pd.DataFrame(updated_cases, columns=config_loader.load_config()['headers'])
                st.write("Cases updated successfully.")
            else:
                st.write(f"No cases found for {selected_date}.")
            st.write(update_status)
        else:
            st.write("No changes detected.")


import streamlit as st
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

person_one_db = r"muelvzdatabase.db"
person_two_db = r"aldredatabase.db"

tags = ["Transportation", "Necessities", "Academics", "Food", "Social", "Personal"]

class FinanceBackend():
    def __init__(self, get_database):
        self.database = get_database

    def add(self, get_amount, get_category):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO finance (category, amount) VALUES (?,?)", (get_category, get_amount))
            conn.commit()

    def graph(self):
        data = {}

        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, amount FROM finance")
            result = cursor.fetchall()

            trans_list = 0
            nece_list = 0
            acad_list = 0
            food_list = 0
            soci_list = 0
            pers_list = 0

            for row in result:
                match row[0]:
                    case "Transportation":
                        trans_list += row[1]

                    case "Necessities":
                        nece_list += row[1]

                    case "Academics":
                        acad_list += row[1]

                    case "Personal":
                        pers_list += row[1]

                    case "Food":
                        food_list += row[1]

                    case "Socials":
                        soci_list += row[1]

            for row in result:
                data[row[0]] = row[1]
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie([trans_list, nece_list, acad_list, food_list, soci_list, pers_list], labels=tags, autopct='%1.1f%%', startangle=90)
            ax.set_title("Expenses Chart")
            
            return st.pyplot(fig)

    def view(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM finance")
            result = cursor.fetchall()
            return result
        
    def delete(self, get_id):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM finance WHERE id = ?",(get_id,))
            conn.commit()


class FinanceFrontend():
    def __init__(self):
        self.muel_database = person_one_db
        self.al_database = person_two_db

        self.muel_finance_backend = FinanceBackend(person_one_db)
        self.al_finance_backend = FinanceBackend(person_two_db)

    def run_web(self):

        st.markdown("<div style='text-align: center;'>"
                    "<h1>Expense Dashboard</h1>"
                    "</div>", unsafe_allow_html=True)
        
        Aldred, Muelvin = st.columns(2)

        with Aldred:
            if self.al_finance_backend not in st.session_state:
                st.session_state.al_finance_backend = FinanceBackend(person_two_db)

            st.markdown("<div style='text-align: center;'>"
                        "<h1>Aldred</h1>"
                        "</div>", unsafe_allow_html=True)
            
            with st.form("Aldred's Expenses"):
                aldred_amount = st.number_input("Enter the amount:")
                aldred_category = st.selectbox("Enter category: ", tags)
                save_aldred_data = st.form_submit_button("Save")

                if save_aldred_data:
                    self.al_finance_backend.add(aldred_amount, aldred_category)
                    st.success(f"{aldred_amount} is added in the {aldred_category}")

            st.session_state.al_finance_backend.graph()

            aldred_amount_entries = st.session_state.al_finance_backend.view()

            if aldred_amount_entries:
                for row in aldred_amount_entries:
                    id1 = row[0]
                    st.write(row[2])
                    st.write(row[1])
                    delete_clicked = st.button("Delete", key=f"delete{row[0]}")
                    if delete_clicked:
                        st.session_state.al_finance_backend.delete(id1)
            
        with Muelvin:
            if self.muel_finance_backend not in st.session_state:
                st.session_state.muel_finance_backend = FinanceBackend(person_one_db)

            st.markdown("<div style='text-align: center;'>"
                        "<h1>Muelvin</h1>"
                        "</div>", unsafe_allow_html=True)
            
            with st.form("Muelvin's Expenses"):
                muelvin_amount = st.number_input("Enter the amount:")
                muelvin_category = st.selectbox("Enter category: ", tags)
                save_muelvin_data = st.form_submit_button("Save")

                if save_muelvin_data:
                    self.muel_finance_backend.add(muelvin_amount, muelvin_category)
                    st.success(f"{muelvin_amount} is added in the {muelvin_category}")

            st.session_state.muel_finance_backend.graph()

            aldred_amount_entries = st.session_state.muel_finance_backend.view()

            if aldred_amount_entries:
                for row in aldred_amount_entries:
                    id1 = row[0]
                    st.write(row[2])
                    st.write(row[1])
                    delete_clicked = st.button("Delete", key=f"delete{row[0]}")
                    if delete_clicked:
                        st.session_state.muel_finance_backend.delete(id1)

if __name__ == "__main__":
    finance_frontend = FinanceFrontend()

    finance_frontend.run_web()
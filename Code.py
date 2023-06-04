import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
import re

os.environ['OPENAI_API_KEY'] = "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"
db = SQLDatabase.from_uri("mysql+pymysql://root:redaredaredareda@127.0.0.1/REDA")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

window = tk.Tk()
window.title("Test")

label = tk.Label(window, text="Interface de test", font=("Arial", 18, "bold"))
label.pack(pady=10)

entry = tk.Entry(window, width=50, font=("Arial", 12))
entry.pack(pady=10)

figure_canvas = None
text_label = None

def extract_number(string):
    pattern = r'\d+\.?\d*'  # Expression régulière d'un nombre

    match = re.search(pattern, string)
    if match:
        return float(match.group())
    else:
        return None

def process_input():
    global figure_canvas, text_label
    
    # Supprimer le graphique précédemment ajouté s'il existe
    if figure_canvas is not None:
        figure_canvas.get_tk_widget().destroy()
        figure_canvas = None
    
    # Supprimer le texte précédemment ajouté s'il existe
    if text_label is not None:
        text_label.destroy()
        text_label = None
    
    user_input = entry.get()
    request = user_input
    response = db_chain.run(request)
    if '%' in response or 'pourcentage' in request or '%' in request :
        percentage = extract_number(response)
        labels = ['Pourcentage recherché', 'le reste']
        sizes = [percentage, 100 - percentage]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        figure_canvas = FigureCanvasTkAgg(fig, master=window)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().pack(pady=10)
    else:
        text_label = tk.Label(window, text=response, font=("Arial", 12))
        text_label.pack(pady=10)

button = tk.Button(window, text="Soumettre", command=process_input, font=("Arial", 12))
button.pack(pady=10)

window.mainloop()


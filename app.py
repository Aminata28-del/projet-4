from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Création de la base de données et des tables si elles n'existent pas
def init_db():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Création de la table des dépenses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL
        )
    ''')

    # Création de la table des revenus
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL
        )
    ''')

    # Vérification si la table des dépenses est vide et ajout des valeurs par défaut
    cursor.execute('SELECT COUNT(*) FROM expenses')
    if cursor.fetchone()[0] == 0:  # Si le tableau est vide
        default_expenses = [
            ('Nourriture', 40000),
            ('Loyer', 30000),
            ('Transport', 10000)
        ]
        cursor.executemany('INSERT INTO expenses (title, amount) VALUES (?, ?)', default_expenses)

    conn.commit()
    conn.close()

# Route principale
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    # Récupération des dépenses
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    # Récupération des revenus
    cursor.execute('SELECT * FROM incomes')
    incomes = cursor.fetchall()

    # Calcul du total des dépenses et des revenus
    total_expenses = sum([expense[2] for expense in expenses])
    total_income = sum([income[2] for income in incomes])
    total_budget = total_income
    balance = total_budget - total_expenses

    conn.close()

    return render_template('index.html', expenses=expenses, total_budget=total_budget, total_expenses=total_expenses, balance=balance)

# Ajout d'un revenu
@app.route('/add_income', methods=['POST'])
def add_income():
    title = request.form['title']
    amount = int(request.form['amount'])

    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO incomes (title, amount) VALUES (?, ?)', (title, amount))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Ajout d'une dépense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = int(request.form['amount'])

    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (title, amount) VALUES (?, ?)', (title, amount))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Suppression d'une dépense
@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialisation de la base de données avec les valeurs par défaut
    app.run(debug=True)

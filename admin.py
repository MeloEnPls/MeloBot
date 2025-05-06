import os
import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)
# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), "jail.db")


def get_db():
    """
    Retourne une connexion SQLite stockée dans le contexte g.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    """
    Ferme la connexion SQLite en fin de requête.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Crée les tables 'sanctions' et 'logs' si elles n'existent pas.
    """
    conn = sqlite3.connect(
        DB_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    cursor = conn.cursor()
    # Table des sanctions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sanctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            issuer_id INTEGER NOT NULL,
            ore_count INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Table des logs
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            user_id INTEGER,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

# Initialise la base avant de démarrer l'application
init_db()


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/sanctions')
def sanctions():
    """
    Affiche la liste des sanctions triées par date décroissante.
    """
    db = get_db()
    rows = db.execute(
        """
        SELECT id, user_id, issuer_id, ore_count, timestamp
        FROM sanctions
        ORDER BY timestamp DESC
        """
    ).fetchall()
    return render_template('sanctions.html', rows=rows)


@app.route('/logs')
def logs():
    """
    Affiche les 200 derniers logs d'événements.
    """
    db = get_db()
    rows = db.execute(
        """
        SELECT id, event_type, user_id, description, timestamp
        FROM logs
        ORDER BY timestamp DESC
        LIMIT 200
        """
    ).fetchall()
    return render_template('logs.html', rows=rows)


if __name__ == "__main__":
    # Démarre le serveur Flask
    app.run(host="0.0.0.0", port=5000, debug=True)

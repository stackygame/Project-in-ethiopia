import sqlite3

class CommandHandler:
    def __init__(self, db_path='variables.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS vars (name TEXT PRIMARY KEY, value TEXT)''')
        conn.commit()
        conn.close()

    def set_var(self, name, value):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('REPLACE INTO vars (name, value) VALUES (?, ?)', (name, value))
        conn.commit()
        conn.close()

    def get_var(self, name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT value FROM vars WHERE name=?', (name,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def parse_and_run(self, command):
        if command.startswith('/set '):
            parts = command.split(' ', 2)
            if len(parts) == 3:
                self.set_var(parts[1], parts[2])
                print(f"Set {parts[1]} = {parts[2]}")
            else:
                print("Usage: /set [name] [value]")
        elif command.startswith('/get '):
            name = command.split(' ', 1)[1]
            value = self.get_var(name)
            print(value if value else "Variable not found.")
        elif command.startswith('/print '):
            expr = command[7:].strip()
            if expr.startswith("str:"):
                print(expr[4:])
            elif expr.startswith("int:"):
                try:
                    result = eval(expr[4:])
                    print(result)
                except Exception as e:
                    print("Error in integer expression:", e)
            else:
                print("Use str: or int:")
        elif command == '/exit':
            print("Goodbye.")
            return False
        else:
            print("Unknown command.")
        return True

class Shell(CommandHandler):
    def run(self):
        print("Mini Shell Interpreter Started. Use /exit to quit.")
        running = True
        while running:
            try:
                cmd = input(">> ")
                running = self.parse_and_run(cmd)
            except KeyboardInterrupt:
                print("\nInterrupted. Use /exit to quit.")
            except EOFError:
                break

if __name__ == "__main__":
    Shell().run()

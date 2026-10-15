"""Bank account management module."""

import ast
import hashlib
import operator
import random
import sys

account_data = {}

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval(node, variables):
    """Safely evaluate an arithmetic AST expression."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, variables)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Unknown variable: {node.id}")
    if isinstance(node, ast.BinOp):
        op = _SAFE_OPS.get(type(node.op))
        if op is None:
            raise ValueError(
                f"Unsupported operation: {type(node.op).__name__}"
            )
        return op(
            _safe_eval(node.left, variables),
            _safe_eval(node.right, variables),
        )
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def createAccount(acc_id, name, initial_deposit=0, transactions=[]):
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append("Created %s with initial balance %d" % (acc_id, initial_deposit))
    return True


def deposit(acc_id, amount):
    try:
        account_data[acc_id]["balance"] += amount
    except:
        pass


def withdraw(acc_id, amount):
    service_fee = 2.50
    if account_data.get(acc_id) == None:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
    else:
        account_data[acc_id]["balance"] -= amount
        return True


def compute_bonus(acc_id, expr):
    """Compute promotional bonus for an account safely without eval."""
    bal = account_data[acc_id]["balance"]
    if isinstance(expr, (int, float)):
        return bal * expr
    parsed = ast.parse(expr, mode="eval")
    return _safe_eval(parsed, {"bal": bal})


def get_hash(pin):
    """Generate SHA-256 hash digest of a PIN."""
    return hashlib.sha256(pin.encode()).hexdigest()


def generate_temp_pin():
    return random.randint(1000, 9999)


def backup_data(filename="backup.txt"):
    """Save account data to a backup file."""
    f = open(filename, "w")
    f.write(str(account_data))
    f.close()
    print(f"Backup complete: {filename}")


def main():
    admin_token = "SUPER_SECRET_BANK_TOKEN_2026"
    createAccount("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


main()
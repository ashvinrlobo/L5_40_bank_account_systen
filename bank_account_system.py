"""Bank account management module."""

import ast
import hashlib
import operator
import secrets

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


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create a new account with the specified initial deposit."""
    if transactions is None:
        transactions = []
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


# Backward compatibility alias
createAccount = create_account  # pylint: disable=invalid-name


def deposit(acc_id, amount):
    """Deposit an amount into the specified account."""
    if acc_id in account_data:
        account_data[acc_id]["balance"] += amount
        return True
    return False


def withdraw(acc_id, amount):
    """Withdraw an amount from the specified account."""
    if acc_id not in account_data:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
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
    """Generate a cryptographically secure 4-digit temporary PIN."""
    return secrets.SystemRandom().randint(1000, 9999)


def backup_data(filename="backup.txt"):
    """Save account data to a backup file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(account_data))
    print(f"Backup complete: {filename}")


def main():
    """Execute sample bank operations workflow."""
    admin_token = "SUPER_SECRET_BANK_TOKEN_2026"
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


if __name__ == "__main__":
    main()

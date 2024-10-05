import string
import getpass
import math

# Load commonly used passwords from a file
def load_blacklist(filename='password_blacklist.txt'):
    with open(filename) as f:
        return set(line.strip() for line in f)

# Estimate password entropy
def calculate_entropy(password):
    char_set_size = 0
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in string.punctuation for c in password):
        char_set_size += len(string.punctuation)
    entropy = len(password) * math.log2(char_set_size) if char_set_size > 0 else 0
    return entropy

# Check password strength
def check_password_strength(password, blacklist):
    # Initialize flags and counters
    has_upper = has_lower = has_digit = has_special = False
    feedback = []

    # Check if password is in blacklist
    if password in blacklist:
        return "Weak password!", 1, "Password is too common. Avoid common passwords.", 0

    # Check password length first for efficiency
    length = len(password)
    if length < 8:
        feedback.append("Password should be at least 8 characters long.")
    else:
        # Traverse the password only once
        for char in password:
            if char.islower():
                has_lower = True
            elif char.isupper():
                has_upper = True
            elif char.isdigit():
                has_digit = True
            elif char in string.punctuation:
                has_special = True

            if all([has_lower, has_upper, has_digit, has_special]):
                break

    # Calculate the score
    score = sum([has_lower, has_upper, has_digit, has_special])

    # Provide feedback based on missing elements
    if not has_lower:
        feedback.append("Add at least one lowercase letter.")
    if not has_upper:
        feedback.append("Add at least one uppercase letter.")
    if not has_digit:
        feedback.append("Add at least one number.")
    if not has_special:
        feedback.append("Add at least one special character.")

    entropy = calculate_entropy(password)

    # Final password strength assessment
    if score == 4 and length >= 8:
        return "Strong password!", score + 1, feedback, entropy
    elif score >= 2:
        return "Moderate password.", score + 1, feedback, entropy
    else:
        return "Weak password!", score + 1, feedback, entropy

# Load blacklist
blacklist = load_blacklist()

# Get password securely from user (hidden input for security)
password = getpass.getpass("Enter your password: ")
strength, score, feedback, entropy = check_password_strength(password, blacklist)

# Output the results
print(f"Password strength: {strength}")
print(f"Score: {score}/5")
print(f"Entropy: {entropy:.2f} bits")
if feedback:
    print("Suggestions to improve your password:")
    for suggestion in feedback:
        print(f"- {suggestion}")
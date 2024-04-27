import re
import dns
try:
    import dns.resolver
except ImportError:
    dns = None

def validate_email(email):
    
    pattern = r'^[a-z0-9]+@[a-z0-9.-]+\.[a-z]{2,}$' # Regular expression pattern for email validation
    
    # Using re.match to check if the email matches the pattern
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    # Split email address into username and domain parts
    username, domain = email.split('@')

    # Check if domain exists and has an MX record
    if dns:
        try:
            # Use DNS resolver to check MX records for the domain
            dns.resolver.resolve(domain, 'MX')
        except dns.resolver.NoAnswer:
            return False, "Domain does not exist"
        except dns.resolver.NXDOMAIN:
            return False, "Domain does not exist"
        except dns.resolver.NoNameservers:
            return False, "No nameservers found for the domain"
        except Exception as e:
            return False, f"Error checking domain: {str(e)}"
    else:
        return False, "DNS resolver module is not available"

    return True, "Valid email address"

# Example usage:
email = input("Enter an email address: ")
valid, message = validate_email(email)
print(message)

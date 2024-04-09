import uuid
import hashlib


def generate_machine_code():
    # Get the MAC address of the first network interface
    mac_address = ":".join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))

    # You can use the MAC address directly as the machine code or perform additional processing if needed
    machine_code = mac_address
    return machine_code


def generate_registration_code(machine_code):
    # Use a simple hash algorithm to generate the registration code
    registration_code = hashlib.md5(machine_code.encode()).hexdigest()
    return registration_code


def save_to_file(machine_code, registration_code, file_path='registration_info.txt'):
    with open(file_path, 'w') as file:
        file.write(f'Machine Code: {machine_code}\n')
        file.write(f'Registration Code: {registration_code}\n')

# Generate machine code and registration code
machine_code = generate_machine_code()

registration_code = generate_registration_code(machine_code)

# Save to a text file
save_to_file(machine_code, registration_code)

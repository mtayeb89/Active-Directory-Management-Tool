import ldap3

class ActiveDirectoryManager:
    def __init__(self, server_address, admin_username, admin_password):
        self.server_address = server_address
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.server = ldap3.Server(self.server_address, get_info=ldap3.ALL)
        self.connection = None

    def connect(self):
        try:
            self.connection = ldap3.Connection(
                self.server,
                user=self.admin_username,
                password=self.admin_password,
                auto_bind=True
            )
            print("Connection successful!")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def search_user(self, search_base, search_filter):
        try:
            self.connection.search(
                search_base=search_base,
                search_filter=search_filter,
                attributes=ldap3.ALL_ATTRIBUTES
            )
            for entry in self.connection.entries:
                print(entry)
        except Exception as e:
            print(f"Failed to search: {e}")

    def add_user(self, dn, attributes):
        try:
            self.connection.add(dn, attributes=attributes)
            print("User added successfully!")
        except Exception as e:
            print(f"Failed to add user: {e}")

    def close(self):
        if self.connection:
            self.connection.unbind()
            print("Connection closed!")

# Example usage:
if __name__ == "__main__":
    server = "ldap://your-ad-server"
    admin_user = "CN=Administrator,CN=Users,DC=example,DC=com"
    admin_password = "your_password"

    ad_manager = ActiveDirectoryManager(server, admin_user, admin_password)
    ad_manager.connect()

    # Search for a user
    search_base = "CN=Users,DC=example,DC=com"
    search_filter = "(sAMAccountName=jdoe)"  # Replace 'jdoe' with the username to search
    ad_manager.search_user(search_base, search_filter)

    # Add a new user
    dn = "CN=John Doe,CN=Users,DC=example,DC=com"
    attributes = {
        'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
        'cn': 'John Doe',
        'sn': 'Doe',
        'givenName': 'John',
        'displayName': 'John Doe',
        'userPrincipalName': 'johndoe@example.com',
        'sAMAccountName': 'johndoe'
    }
    ad_manager.add_user(dn, attributes)

    ad_manager.close()

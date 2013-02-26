# List of all SVN commands required
def log(client, url):
    return client.log(url, discover_changed_paths=True, strict_node_history=True)

def list(client, url):
    return client.list(url, recurse=True)
from opensearchpy import OpenSearch

host = 'api.novasearch.org'
port = 443
user = 'user201' # Add your user name here.
password = 'Lrr1531' # Add your user password here. For testing only. Don't store credentials in code. 
index_name = user

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = (user, password),
    url_prefix = 'opensearch',
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

def get_data():
    return client, index_name
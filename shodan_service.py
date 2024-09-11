import shodan

class ShodanService:
    def __init__(self):
        pass

    def search(self, ip_address, api_key):
        try:
            api = shodan.Shodan(api_key)
            host_info = api.host(ip_address)

            # Format results
            results = f"IP: {host_info['ip_str']}\n-----------------\n"
            for item in host_info['data']:
                results += f"Port: {item['port']}\n"
                if 'product' in item:
                    results += f"Product: {item['product']}\n"
                if 'data' in item:
                    data_preview = item['data'].split('/n')[0][:100] + '...'
                    results += f"Data: {data_preview}\n"
                results += "-----------------\n"
            
            if 'vulns' in host_info:
                results += "Vulnerabilities:\n"
                for vuln in host_info['vulns']:
                    results += f"{vuln}\n"
                results += "-----------------\n"

            return results
        except shodan.APIError as e:
            return f"Shodan API error: {e}"
        except Exception as e:
            return f"An unexpected error occured: {e}"

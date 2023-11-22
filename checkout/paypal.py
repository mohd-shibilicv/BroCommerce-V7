from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AZxmiYdjz_BkDYAtPkm2z73UfODEkJn1k_1591OlodkTEzEKT2PXzIY6sy3FChurOOCHl1_fsTbDnnw7"
        self.client_secret = "EOymw0o9sX2KzAuTxtdzOA7FF_HzBXFvwxToTyYHCE6JSTFa7OD14wgJbtG2PiexDlWuvKO3Rmdf2Z2c"
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.client = PayPalHttpClient(self.environment)

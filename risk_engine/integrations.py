import requests
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class BallerineIntegration:
    """Integration with Ballerine for case management"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = self.config.BALLERINE_API_URL
        self.api_key = self.config.BALLERINE_API_KEY
    
    def create_case(self, transaction_data, risk_score, risk_reasons):
        """Create a case in Ballerine for analyst review"""
        try:
            # Prepare payload for Ballerine workflow
            payload = {
                "workflowId": "transaction_review_workflow",
                "context": {
                    "entity": {
                        "ballerineEntityId": transaction_data['transaction_id'],
                        "type": "transaction",
                        "data": {
                            "transactionId": transaction_data['transaction_id'],
                            "customerId": transaction_data['customer_id'],
                            "amount": float(transaction_data['amount']),
                            "currency": transaction_data.get('currency', 'KES'),
                            "merchantName": transaction_data.get('merchant_name', ''),
                            "transactionType": transaction_data.get('transaction_type', ''),
                            "location": transaction_data.get('location', ''),
                            "channel": transaction_data.get('channel', ''),
                            "riskScore": risk_score,
                            "riskReasons": risk_reasons,
                            "timestamp": str(transaction_data.get('timestamp', ''))
                        }
                    }
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
            }
            
            # For now, we'll simulate the API call since Ballerine setup is complex
            # In production, uncomment the actual API call below
            
            # response = requests.post(
            #     f"{self.base_url}/workflows/run",
            #     json=payload,
            #     headers=headers,
            #     timeout=30
            # )
            
            # Simulate successful response
            logger.info(f"[SIMULATED] Created Ballerine case for transaction {transaction_data['transaction_id']}")
            return {
                "success": True,
                "case_id": f"BAL_{transaction_data['transaction_id']}",
                "workflow_id": "transaction_review_workflow"
            }
            
            # Actual implementation would be:
            # if response.status_code == 201:
            #     result = response.json()
            #     logger.info(f"Created Ballerine case: {result.get('id')}")
            #     return {"success": True, "case_id": result.get('id')}
            # else:
            #     logger.error(f"Failed to create Ballerine case: {response.text}")
            #     return {"success": False, "error": response.text}
            
        except Exception as e:
            logger.error(f"Error creating Ballerine case: {e}")
            return {"success": False, "error": str(e)}

class CISOAssistantIntegration:
    """Integration with CISO Assistant for risk register management"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = self.config.CISO_API_URL
        self.api_token = self.config.CISO_API_TOKEN
    
    def log_risk_event(self, risk_type, title, description, severity="medium"):
        """Log a risk event to CISO Assistant risk register"""
        try:
            payload = {
                "name": title,
                "description": description,
                "risk_category": risk_type.upper(),
                "severity": severity,
                "status": "open",
                "likelihood": self._map_severity_to_likelihood(severity),
                "impact": self._map_severity_to_impact(severity)
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Token {self.api_token}" if self.api_token else ""
            }
            
            # Simulate API call for now
            logger.info(f"[SIMULATED] Logged risk event to CISO Assistant: {title}")
            return {"success": True, "risk_id": f"RISK_{hash(title) % 10000}"}
            
            # Actual implementation:
            # response = requests.post(
            #     f"{self.base_url}/risks/",
            #     json=payload,
            #     headers=headers,
            #     timeout=30
            # )
            
        except Exception as e:
            logger.error(f"Error logging risk event: {e}")
            return {"success": False, "error": str(e)}
    
    def _map_severity_to_likelihood(self, severity):
        """Map severity to likelihood scale"""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return mapping.get(severity.lower(), 2)
    
    def _map_severity_to_impact(self, severity):
        """Map severity to impact scale"""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return mapping.get(severity.lower(), 2)

class TazamaIntegration:
    """Integration with Tazama for real-time fraud detection"""
    
    def __init__(self):
        self.base_url = "http://localhost:4001"  # Default Tazama port
    
    def submit_transaction(self, transaction_data):
        """Submit transaction to Tazama for real-time fraud detection"""
        try:
            # Convert to ISO20022-like format for Tazama
            payload = {
                "TxTp": transaction_data.get('transaction_type', 'TRANSFER'),
                "Amt": {
                    "Amt": float(transaction_data['amount']),
                    "Ccy": transaction_data.get('currency', 'KES')
                },
                "CdtrAcct": {
                    "Id": transaction_data.get('account_number', '')
                },
                "Cdtr": {
                    "Nm": transaction_data.get('merchant_name', ''),
                    "Id": transaction_data.get('customer_id', '')
                },
                "CreDtTm": str(transaction_data.get('timestamp', '')),
                "EndToEndId": transaction_data['transaction_id']
            }
            
            # Simulate Tazama response
            logger.info(f"[SIMULATED] Submitted transaction to Tazama: {transaction_data['transaction_id']}")
            
            # Simulate fraud score based on amount
            fraud_score = min(float(transaction_data['amount']) / 10000000, 1.0)
            
            return {
                "success": True,
                "fraud_score": fraud_score,
                "typologies": ["Large Transaction"] if fraud_score > 0.5 else [],
                "recommendation": "BLOCK" if fraud_score > 0.8 else "REVIEW" if fraud_score > 0.5 else "APPROVE"
            }
            
        except Exception as e:
            logger.error(f"Error submitting to Tazama: {e}")
            return {"success": False, "error": str(e)}
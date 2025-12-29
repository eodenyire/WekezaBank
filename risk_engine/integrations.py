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
        self.enabled = self.config.is_production and bool(self.api_key)
    
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
            
            if self.enabled:
                # Production API call
                try:
                    response = requests.post(
                        f"{self.base_url}/workflows/run",
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        result = response.json()
                        logger.info(f"Created Ballerine case: {result.get('id', 'unknown')}")
                        return {"success": True, "case_id": result.get('id')}
                    else:
                        logger.error(f"Failed to create Ballerine case: {response.status_code} - {response.text}")
                        return {"success": False, "error": f"HTTP {response.status_code}"}
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Network error creating Ballerine case: {e}")
                    return {"success": False, "error": str(e)}
            else:
                # Development/simulation mode
                logger.info(f"[SIMULATED] Created Ballerine case for transaction {transaction_data['transaction_id']}")
                return {
                    "success": True,
                    "case_id": f"BAL_{transaction_data['transaction_id']}",
                    "workflow_id": "transaction_review_workflow"
                }
            
        except Exception as e:
            logger.error(f"Error creating Ballerine case: {e}")
            return {"success": False, "error": str(e)}

class CISOAssistantIntegration:
    """Integration with CISO Assistant for risk register management"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = self.config.CISO_API_URL
        self.api_token = self.config.CISO_API_TOKEN
        self.enabled = self.config.is_production and bool(self.api_token)
    
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
                "impact": self._map_severity_to_impact(severity),
                "treatment": "mitigate",
                "owner": "risk_engine",
                "created_at": "auto"
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Token {self.api_token}" if self.api_token else ""
            }
            
            if self.enabled:
                # Production API call
                try:
                    response = requests.post(
                        f"{self.base_url}/risks/",
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        result = response.json()
                        logger.info(f"Logged risk event to CISO Assistant: {result.get('id', 'unknown')}")
                        return {"success": True, "risk_id": result.get('id')}
                    else:
                        logger.error(f"Failed to log risk event: {response.status_code} - {response.text}")
                        return {"success": False, "error": f"HTTP {response.status_code}"}
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Network error logging risk event: {e}")
                    return {"success": False, "error": str(e)}
            else:
                # Development/simulation mode
                logger.info(f"[SIMULATED] Logged risk event to CISO Assistant: {title}")
                return {"success": True, "risk_id": f"RISK_{hash(title) % 10000}"}
            
        except Exception as e:
            logger.error(f"Error logging risk event: {e}")
            return {"success": False, "error": str(e)}
    
    def _map_severity_to_likelihood(self, severity):
        """Map severity to likelihood scale (1-5)"""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return mapping.get(severity.lower(), 2)
    
    def _map_severity_to_impact(self, severity):
        """Map severity to impact scale (1-5)"""
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
        self.config = Config()
        self.base_url = self.config.TAZAMA_API_URL
        self.api_key = self.config.TAZAMA_API_KEY
        self.enabled = self.config.is_production and bool(self.api_key)
    
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
                "EndToEndId": transaction_data['transaction_id'],
                "InstrId": transaction_data['transaction_id']
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
            }
            
            if self.enabled:
                # Production API call
                try:
                    response = requests.post(
                        f"{self.base_url}/evaluate",
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        logger.info(f"Tazama evaluation completed for {transaction_data['transaction_id']}")
                        return {
                            "success": True,
                            "fraud_score": result.get('score', 0.0),
                            "typologies": result.get('typologies', []),
                            "recommendation": result.get('recommendation', 'APPROVE'),
                            "alerts": result.get('alerts', [])
                        }
                    else:
                        logger.error(f"Tazama API error: {response.status_code} - {response.text}")
                        return {"success": False, "error": f"HTTP {response.status_code}"}
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Network error with Tazama: {e}")
                    return {"success": False, "error": str(e)}
            else:
                # Development/simulation mode
                logger.info(f"[SIMULATED] Submitted transaction to Tazama: {transaction_data['transaction_id']}")
                
                # Simulate fraud score based on amount and patterns
                amount = float(transaction_data['amount'])
                fraud_score = 0.0
                typologies = []
                
                # High amount transactions
                if amount > 10000000:  # 10M KES
                    fraud_score += 0.4
                    typologies.append("Large Transaction")
                
                # Unknown merchants
                if transaction_data.get('merchant_name', '').lower() in ['unknown', 'suspicious']:
                    fraud_score += 0.3
                    typologies.append("Unknown Merchant")
                
                # Unusual locations
                if transaction_data.get('location', '').lower() == 'unknown':
                    fraud_score += 0.2
                    typologies.append("Unusual Location")
                
                # Round-number amounts (potential structuring)
                if amount % 1000000 == 0 and amount > 1000000:
                    fraud_score += 0.1
                    typologies.append("Round Amount")
                
                fraud_score = min(fraud_score, 1.0)
                
                recommendation = "BLOCK" if fraud_score > 0.8 else "REVIEW" if fraud_score > 0.5 else "APPROVE"
                
                return {
                    "success": True,
                    "fraud_score": fraud_score,
                    "typologies": typologies,
                    "recommendation": recommendation,
                    "alerts": [{"type": t, "severity": "high" if fraud_score > 0.7 else "medium"} for t in typologies]
                }
            
        except Exception as e:
            logger.error(f"Error submitting to Tazama: {e}")
            return {"success": False, "error": str(e)}
    
    def get_transaction_status(self, transaction_id):
        """Get the status of a transaction from Tazama"""
        try:
            if self.enabled:
                response = requests.get(
                    f"{self.base_url}/transactions/{transaction_id}",
                    headers={"Authorization": f"Bearer {self.api_key}" if self.api_key else ""},
                    timeout=30
                )
                
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": f"HTTP {response.status_code}"}
            else:
                # Simulation mode
                return {
                    "success": True,
                    "data": {
                        "transaction_id": transaction_id,
                        "status": "processed",
                        "alerts": []
                    }
                }
                
        except Exception as e:
            logger.error(f"Error getting transaction status: {e}")
            return {"success": False, "error": str(e)}
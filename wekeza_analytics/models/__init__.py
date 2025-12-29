"""
Data models for Wekeza Bank analytics
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class Customer(BaseModel):
    """Customer data model"""
    customer_id: str = Field(..., description="Unique customer identifier")
    name: str = Field(..., description="Customer name")
    email: str = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Customer phone number")
    account_type: str = Field(..., description="Account type (savings, checking, etc.)")
    registration_date: datetime = Field(..., description="Account registration date")
    credit_score: Optional[int] = Field(None, ge=300, le=850, description="Credit score")
    monthly_income: Optional[float] = Field(None, ge=0, description="Monthly income")
    country: str = Field(..., description="Country of residence")
    risk_category: Optional[str] = Field(None, description="Risk category (low, medium, high)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST001",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "account_type": "savings",
                "registration_date": "2023-01-15T10:00:00",
                "credit_score": 720,
                "monthly_income": 5000.0,
                "country": "USA",
                "risk_category": "low"
            }
        }


class Transaction(BaseModel):
    """Transaction data model"""
    transaction_id: str = Field(..., description="Unique transaction identifier")
    customer_id: str = Field(..., description="Customer identifier")
    transaction_date: datetime = Field(..., description="Transaction date and time")
    amount: float = Field(..., description="Transaction amount")
    transaction_type: str = Field(..., description="Transaction type (debit, credit, transfer)")
    category: str = Field(..., description="Transaction category (shopping, bills, salary, etc.)")
    merchant: Optional[str] = Field(None, description="Merchant name")
    location: Optional[str] = Field(None, description="Transaction location")
    status: str = Field(..., description="Transaction status (completed, pending, failed)")
    is_fraudulent: bool = Field(False, description="Fraud flag")
    
    @validator('amount')
    def amount_must_be_nonzero(cls, v):
        if v == 0:
            raise ValueError('Transaction amount cannot be zero')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "TXN001",
                "customer_id": "CUST001",
                "transaction_date": "2023-06-15T14:30:00",
                "amount": 150.50,
                "transaction_type": "debit",
                "category": "shopping",
                "merchant": "Example Store",
                "location": "New York",
                "status": "completed",
                "is_fraudulent": False
            }
        }


class Account(BaseModel):
    """Account data model"""
    account_id: str = Field(..., description="Unique account identifier")
    customer_id: str = Field(..., description="Customer identifier")
    account_type: str = Field(..., description="Account type")
    balance: float = Field(..., ge=0, description="Current balance")
    currency: str = Field(default="USD", description="Currency code")
    opening_date: datetime = Field(..., description="Account opening date")
    status: str = Field(..., description="Account status (active, dormant, closed)")
    interest_rate: Optional[float] = Field(None, ge=0, le=100, description="Interest rate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "account_id": "ACC001",
                "customer_id": "CUST001",
                "account_type": "savings",
                "balance": 15000.50,
                "currency": "USD",
                "opening_date": "2023-01-15T10:00:00",
                "status": "active",
                "interest_rate": 2.5
            }
        }


class AnalyticsResult(BaseModel):
    """Analytics result model"""
    analysis_type: str = Field(..., description="Type of analysis performed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    metrics: dict = Field(..., description="Analysis metrics and results")
    insights: List[str] = Field(default_factory=list, description="Key insights")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "customer_segmentation",
                "timestamp": "2023-06-15T10:00:00",
                "metrics": {
                    "total_customers": 1000,
                    "segments": 4
                },
                "insights": ["High-value customers represent 20% of the base"],
                "recommendations": ["Focus retention efforts on high-value segment"]
            }
        }

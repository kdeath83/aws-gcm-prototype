"""
GCM Principle 1: Runtime Control Coherence Detector - REMEDIATED
Fixes: Input validation (1), Error handling (8), Decimal serialization (7)
"""

import json
import os
import re
import boto3
import logging
from datetime import datetime, timezone
from decimal import Decimal

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACES_TABLE'])
events_client = boto3.client('events')

# Fix 1: Input validation
VALIDATION_SCHEMA = {
    'executionId': {'type': str, 'pattern': r'^[a-zA-Z0-9-_]{1,128}$', 'required': True},
    'timestamp': {'type': str, 'required': True}
}

class DecimalEncoder(json.JSONEncoder):
    """Fix 7: Handle Decimal serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def validate_event(event):
    """Validate event structure."""
    detail = event.get('detail', {})
    
    # Check required fields
    for field, rules in VALIDATION_SCHEMA.items():
        if rules.get('required') and field not in detail:
            raise ValueError(f"Missing required field: {field}")
        
        if field in detail:
            value = detail[field]
            if not isinstance(value, rules['type']):
                raise ValueError(f"Field {field} must be {rules['type'].__name__}")
            
            if 'pattern' in rules and not re.match(rules['pattern'], value):
                raise ValueError(f"Field {field} format invalid")
    
    return detail

class CoherenceAnalyzer:
    """Analyzes control loop interactions for coherence violations."""
    
    def __init__(self):
        self.violations = []
        self.coherence_score = 100.0
    
    def detect_scheduler_conflicts(self, execution_data):
        """Detect when multiple schedulers compete for resources."""
        schedulers = execution_data.get('schedulers', [])
        if len(schedulers) > 1:
            # Check for timing conflicts
            for i, s1 in enumerate(schedulers):
                for s2 in schedulers[i+1:]:
                    if s1.get('priority') == s2.get('priority'):
                        self.violations.append({
                            'type': 'scheduler_conflict',
                            'severity': 'medium',
                            'description': f"Schedulers {s1['name']} and {s2['name']} have equal priority",
                            'timestamp': datetime.now(timezone.utc).isoformat()
                        })
                        self.coherence_score -= 15
    
    def detect_policy_layer_incoherence(self, execution_data):
        """Detect when policy layers produce conflicting outputs."""
        policies = execution_data.get('policy_decisions', [])
        
        # Check for contradictory decisions
        allow_count = sum(1 for p in policies if p.get('decision') == 'ALLOW')
        block_count = sum(1 for p in policies if p.get('decision') == 'BLOCK')
        
        if allow_count > 0 and block_count > 0:
            self.violations.append({
                'type': 'policy_incoherence',
                'severity': 'high',
                'description': f"Conflicting policy decisions: {allow_count} ALLOW vs {block_count} BLOCK",
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            self.coherence_score -= 25
    
    def detect_circuit_breaker_abuse(self, execution_data):
        """Detect frequent circuit breaker triggers indicating instability."""
        triggers = execution_data.get('circuit_breaker_triggers', [])
        
        if len(triggers) > 3:
            self.violations.append({
                'type': 'circuit_breaker_abuse',
                'severity': 'high',
                'description': f"Excessive circuit breaker triggers: {len(triggers)} in single execution",
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            self.coherence_score -= 30
        elif len(triggers) > 0:
            self.violations.append({
                'type': 'circuit_breaker_triggered',
                'severity': 'low',
                'description': f"Circuit breaker triggered {len(triggers)} times",
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            self.coherence_score -= 10
    
    def analyze(self, execution_data):
        """Run all coherence checks."""
        self.detect_scheduler_conflicts(execution_data)
        self.detect_policy_layer_incoherence(execution_data)
        self.detect_circuit_breaker_abuse(execution_data)
        
        # Ensure score doesn't go below 0
        self.coherence_score = max(0.0, self.coherence_score)
        
        return {
            'coherence_score': Decimal(str(self.coherence_score)),
            'violations': self.violations,
            'violations_count': len(self.violations),
            'status': 'COHERENT' if self.coherence_score >= 80 else 'DEGRADED' if self.coherence_score >= 50 else 'INCOHERENT'
        }

def handler(event, context):
    """Fix 8: Lambda handler with comprehensive error handling."""
    logger.info(f"Processing event: {json.dumps(event, cls=DecimalEncoder)}")
    
    try:
        # Fix 1: Validate input
        execution_data = validate_event(event)
        execution_id = execution_data.get('executionId', 'unknown')
        
        # Analyze coherence
        analyzer = CoherenceAnalyzer()
        coherence_result = analyzer.analyze(execution_data)
        
        # Store in DynamoDB
        trace_item = {
            'executionId': execution_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ttl': int((datetime.now(timezone.utc).timestamp() + 2592000)),
            'principle': 'COHERENCE',
            'coherence_score': coherence_result['coherence_score'],
            'violations': coherence_result['violations'],
            'violations_count': coherence_result['violations_count'],
            'status': coherence_result['status']
        }
        
        table.put_item(Item=trace_item)
        
        # Emit high-severity violations as events
        high_severity = [v for v in coherence_result['violations'] if v['severity'] in ['high', 'critical']]
        if high_severity:
            try:
                events_client.put_events(
                    Entries=[{
                        'Source': 'gcm.coherence.violation',
                        'DetailType': 'CoherenceViolation',
                        'Detail': json.dumps({
                            'executionId': execution_id,
                            'violations': high_severity,
                            'coherence_score': float(coherence_result['coherence_score'])
                        }, cls=DecimalEncoder),
                        'EventBusName': os.environ['EVENT_BUS']
                    }]
                )
            except Exception as e:
                logger.error(f"Failed to emit events: {e}")
        
        return {
            'statusCode': 200,
            'executionId': execution_id,
            'coherence_score': float(coherence_result['coherence_score']),
            'violations_count': coherence_result['violations_count']
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {'statusCode': 400, 'error': str(e), 'errorType': 'ValidationError'}
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise  # Trigger DLQ retry

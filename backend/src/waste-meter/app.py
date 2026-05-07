"""
GCM Principle 3: Structural Waste Meter
Measures the gap between model capability and system productivity.
"""

import json
import os
import boto3
from datetime import datetime, timezone
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACES_TABLE'])

class WasteAnalyzer:
    """Analyzes structural waste in agent executions."""
    
    def __init__(self):
        self.waste_metrics = {
            'latency_waste': 0.0,
            'cost_waste': 0.0,
            'token_waste': 0.0,
            'retry_waste': 0.0
        }
        self.waste_indicators = []
    
    def calculate_latency_waste(self, execution_data):
        """Calculate time spent without productive output."""
        total_duration = execution_data.get('total_duration_ms', 0)
        productive_time = execution_data.get('productive_time_ms', 0)
        
        if total_duration > 0:
            waste_ratio = (total_duration - productive_time) / total_duration
            self.waste_metrics['latency_waste'] = waste_ratio * 100
            
            if waste_ratio > 0.5:
                self.waste_indicators.append({
                    'type': 'latency_waste',
                    'severity': 'high',
                    'description': f"{waste_ratio*100:.1f}% of execution time was non-productive",
                    'metric': f"{total_duration - productive_time}ms wasted"
                })
    
    def calculate_cost_waste(self, execution_data):
        """Calculate cost per unit of useful output."""
        total_cost = execution_data.get('total_cost_usd', 0)
        outputs_generated = execution_data.get('outputs_generated', 0)
        
        if outputs_generated > 0:
            cost_per_output = total_cost / outputs_generated
            self.waste_metrics['cost_waste'] = cost_per_output
            
            if cost_per_output > 0.10:  # $0.10 per output
                self.waste_indicators.append({
                    'type': 'cost_waste',
                    'severity': 'medium',
                    'description': f"High cost per output: ${cost_per_output:.4f}",
                    'metric': f"${total_cost:.4f} total for {outputs_generated} outputs"
                })
    
    def calculate_token_waste(self, execution_data):
        """Calculate tokens spent without meaningful state change."""
        tokens_used = execution_data.get('tokens_used', 0)
        state_changes = execution_data.get('state_changes', 0)
        
        if state_changes > 0:
            tokens_per_change = tokens_used / state_changes
            
            if tokens_per_change > 10000:  # More than 10k tokens per meaningful change
                self.waste_metrics['token_waste'] = tokens_per_change
                self.waste_indicators.append({
                    'type': 'token_waste',
                    'severity': 'medium',
                    'description': f"Excessive tokens per state change: {tokens_per_change:.0f}",
                    'metric': f"{tokens_used} tokens for {state_changes} state changes"
                })
    
    def calculate_retry_waste(self, execution_data):
        """Calculate waste from repeated attempts."""
        retry_count = execution_data.get('retry_count', 0)
        total_attempts = execution_data.get('total_attempts', 1)
        
        retry_ratio = retry_count / total_attempts if total_attempts > 0 else 0
        self.waste_metrics['retry_waste'] = retry_ratio * 100
        
        if retry_ratio > 0.3:  # More than 30% retries
            self.waste_indicators.append({
                'type': 'retry_waste',
                'severity': 'high',
                'description': f"High retry rate: {retry_ratio*100:.1f}% of attempts failed",
                'metric': f"{retry_count} retries out of {total_attempts} attempts"
            })
    
    def calculate_capability_productivity_gap(self, execution_data):
        """Calculate the gap between model capability and realized productivity."""
        # Capability score (0-100 based on model benchmarks)
        capability_score = execution_data.get('model_capability_score', 85)
        
        # Productivity score (0-100 based on successful outputs vs potential)
        outputs_generated = execution_data.get('outputs_generated', 0)
        potential_outputs = execution_data.get('potential_outputs', 1)
        productivity_score = (outputs_generated / potential_outputs) * 100 if potential_outputs > 0 else 0
        
        gap = capability_score - productivity_score
        
        return {
            'capability_score': capability_score,
            'productivity_score': productivity_score,
            'gap': gap,
            'gap_percentage': (gap / capability_score) * 100 if capability_score > 0 else 0
        }
    
    def analyze(self, execution_data):
        """Run all waste analyses."""
        self.calculate_latency_waste(execution_data)
        self.calculate_cost_waste(execution_data)
        self.calculate_token_waste(execution_data)
        self.calculate_retry_waste(execution_data)
        
        gap_analysis = self.calculate_capability_productivity_gap(execution_data)
        
        total_waste_score = (
            self.waste_metrics['latency_waste'] * 0.3 +
            min(self.waste_metrics['cost_waste'] * 1000, 100) * 0.3 +  # Normalize
            min(self.waste_metrics['token_waste'] / 100, 100) * 0.2 +  # Normalize
            self.waste_metrics['retry_waste'] * 0.2
        )
        
        return {
            'waste_metrics': {
                'latency_waste_percent': Decimal(str(self.waste_metrics['latency_waste'])),
                'cost_per_output_usd': Decimal(str(self.waste_metrics['cost_waste'])),
                'tokens_per_change': Decimal(str(self.waste_metrics['token_waste'])),
                'retry_waste_percent': Decimal(str(self.waste_metrics['retry_waste']))
            },
            'waste_indicators': self.waste_indicators,
            'indicators_count': len(self.waste_indicators),
            'capability_productivity_gap': {
                'capability_score': Decimal(str(gap_analysis['capability_score'])),
                'productivity_score': Decimal(str(gap_analysis['productivity_score'])),
                'gap': Decimal(str(gap_analysis['gap'])),
                'gap_percentage': Decimal(str(gap_analysis['gap_percentage']))
            },
            'total_waste_score': Decimal(str(min(total_waste_score, 100))),
            'status': 'CRITICAL' if total_waste_score > 70 else 'DEGRADED' if total_waste_score > 40 else 'EFFICIENT'
        }

def handler(event, context):
    """Lambda handler for waste detection."""
    
    detail = event.get('detail', {})
    execution_id = detail.get('executionId', 'unknown')
    
    # Analyze waste
    analyzer = WasteAnalyzer()
    waste_result = analyzer.analyze(detail)
    
    # Store in DynamoDB
    trace_item = {
        'executionId': execution_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'ttl': int((datetime.now(timezone.utc).timestamp() + 2592000)),
        'principle': 'WASTE_DETECTION',
        'waste_metrics': waste_result['waste_metrics'],
        'indicators_count': waste_result['indicators_count'],
        'waste_indicators': waste_result['waste_indicators'],
        'capability_gap': waste_result['capability_productivity_gap'],
        'total_waste_score': waste_result['total_waste_score'],
        'status': waste_result['status']
    }
    
    table.put_item(Item=trace_item)
    
    return {
        'statusCode': 200,
        'executionId': execution_id,
        'total_waste_score': float(waste_result['total_waste_score']),
        'indicators_count': waste_result['indicators_count'],
        'status': waste_result['status']
    }

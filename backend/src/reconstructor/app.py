"""
GCM Principle 4: Execution Reconstructor
Full audit trail with replay capability for multi-step planning.
"""

import json
import os
import io
import logging
import boto3
from datetime import datetime, timezone
from decimal import Decimal

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table(os.environ['TRACES_TABLE'])
ARCHIVE_BUCKET = os.environ['ARCHIVE_BUCKET']

class DecimalEncoder(json.JSONEncoder):
    """Fix 7: Handle Decimal serialization for S3 upload."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class ExecutionReconstructor:
    """Reconstructs agent execution traces for audit and replay."""
    
    def __init__(self):
        self.timeline = []
        self.decision_points = []
        self.interventions = []
    
    def build_timeline(self, execution_events):
        """Build chronological timeline of execution."""
        sorted_events = sorted(execution_events, key=lambda x: x.get('timestamp', ''))
        
        for event in sorted_events:
            timeline_item = {
                'timestamp': event.get('timestamp'),
                'type': event.get('type', 'unknown'),
                'description': event.get('description', ''),
                'data': event.get('data', {})
            }
            self.timeline.append(timeline_item)
            
            # Identify decision points
            if event.get('type') in ['decision', 'branch', 'tool_selection']:
                self.decision_points.append({
                    'timestamp': event.get('timestamp'),
                    'decision_type': event.get('type'),
                    'input_state': event.get('data', {}).get('input_state'),
                    'output_state': event.get('data', {}).get('output_state'),
                    'rationale': event.get('data', {}).get('rationale', 'No rationale provided')
                })
            
            # Identify interventions
            if event.get('type') in ['circuit_breaker', 'policy_block', 'human_review']:
                self.interventions.append({
                    'timestamp': event.get('timestamp'),
                    'intervention_type': event.get('type'),
                    'trigger': event.get('data', {}).get('trigger'),
                    'action_taken': event.get('data', {}).get('action'),
                    'outcome': event.get('data', {}).get('outcome')
                })
    
    def generate_replay_script(self, execution_id):
        """Generate a script that can replay the execution."""
        replay_steps = []
        
        for item in self.timeline:
            if item['type'] == 'tool_call':
                replay_steps.append({
                    'action': 'invoke_tool',
                    'tool': item['data'].get('tool_name'),
                    'parameters': item['data'].get('parameters'),
                    'expected_result': item['data'].get('result')
                })
            elif item['type'] == 'llm_call':
                replay_steps.append({
                    'action': 'llm_inference',
                    'prompt': item['data'].get('prompt'),
                    'expected_response': item['data'].get('response')
                })
        
        return {
            'execution_id': execution_id,
            'replay_format_version': '1.0',
            'steps': replay_steps,
            'can_replay': len(replay_steps) > 0
        }
    
    def generate_audit_report(self, execution_id, coherence_data, tool_data, waste_data):
        """Generate compliance-ready audit report."""
        return {
            'execution_id': execution_id,
            'audit_timestamp': datetime.now(timezone.utc).isoformat(),
            'reconstruction_complete': True,
            'summary': {
                'total_events': len(self.timeline),
                'decision_points': len(self.decision_points),
                'interventions': len(self.interventions),
                'duration_ms': self.calculate_duration(),
                'status': 'AUDITABLE'
            },
            'timeline': self.timeline,
            'decision_points': self.decision_points,
            'interventions': self.interventions,
            'gcm_analysis': {
                'coherence_score': coherence_data.get('coherence_score', 'N/A'),
                'tool_graph_depth': tool_data.get('graph_depth', 'N/A'),
                'waste_score': waste_data.get('total_waste_score', 'N/A')
            },
            'compliance_notes': self.generate_compliance_notes()
        }
    
    def calculate_duration(self):
        """Calculate total execution duration from timeline."""
        if len(self.timeline) < 2:
            return 0
        
        try:
            start = datetime.fromisoformat(self.timeline[0]['timestamp'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(self.timeline[-1]['timestamp'].replace('Z', '+00:00'))
            return int((end - start).total_seconds() * 1000)
        except:
            return 0
    
    def generate_compliance_notes(self):
        """Generate notes relevant for compliance audit."""
        notes = []
        
        if self.interventions:
            notes.append(f"{len(self.interventions)} automated interventions occurred during execution")
        
        if len(self.decision_points) > 10:
            notes.append("High decision density - complex multi-step planning detected")
        
        for intervention in self.interventions:
            if intervention['intervention_type'] == 'circuit_breaker':
                notes.append("Circuit breaker triggered - system instability detected")
            elif intervention['intervention_type'] == 'human_review':
                notes.append("Human review required - decision escalated")
        
        return notes

import io

def handler(event, context):
    """Fix 5, 9, 13: Idempotency, batch queries, streaming to S3."""
    logger.info(f"Processing {len(event.get('Records', []))} stream records")
    
    processed_records = 0
    
    # Process DynamoDB stream records
    for record in event.get('Records', []):
        if record.get('eventName') not in ['INSERT', 'MODIFY']:
            continue
        
        new_image = record.get('dynamodb', {}).get('NewImage', {})
        execution_id = new_image.get('executionId', {}).get('S', 'unknown')
        sequence_number = record.get('dynamodb', {}).get('SequenceNumber', '')
        
        # Fix 5: Idempotency check
        idempotency_key = f"{execution_id}-{sequence_number}"
        
        try:
            # Check if already processed
            check_response = table.get_item(
                Key={
                    'executionId': f"_processed:{execution_id}",
                    'timestamp': sequence_number
                }
            )
            if 'Item' in check_response:
                logger.info(f"Skipping already processed record: {idempotency_key}")
                continue
        except Exception as e:
            logger.warning(f"Idempotency check failed: {e}")
        
        # Fix 9: Query with pagination to avoid N+1
        items = []
        last_evaluated_key = None
        
        while True:
            query_args = {
                'KeyConditionExpression': 'executionId = :eid',
                'ExpressionAttributeValues': {':eid': execution_id},
                'Limit': 100  # Page size
            }
            if last_evaluated_key:
                query_args['ExclusiveStartKey'] = last_evaluated_key
            
            response = table.query(**query_args)
            items.extend(response.get('Items', []))
            
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
        
        processed_records += 1
        
        # Extract data from different principles
        coherence_data = next((i for i in items if i.get('principle') == 'COHERENCE'), {})
        tool_data = next((i for i in items if i.get('principle') == 'TOOL_CALL_GRAPH'), {})
        waste_data = next((i for i in items if i.get('principle') == 'WASTE_DETECTION'), {})
        
        # Build execution events from timeline
        execution_events = []
        for item in items:
            if 'timeline' in item:
                execution_events.extend(item['timeline'])
        
        # Reconstruct execution
        reconstructor = ExecutionReconstructor()
        reconstructor.build_timeline(execution_events)
        
        # Generate audit report
        audit_report = reconstructor.generate_audit_report(
            execution_id, coherence_data, tool_data, waste_data
        )
        
        # Generate replay script
        replay_script = reconstructor.generate_replay_script(execution_id)
        
        # Fix 13: Stream to S3 to avoid Lambda payload limits
        archive_key = f"executions/{execution_id}/audit-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
        
        # Use DecimalEncoder for proper serialization
        json_data = json.dumps({
            'audit_report': audit_report,
            'replay_script': replay_script,
            'raw_traces': items
        }, cls=DecimalEncoder)
        
        # Stream upload
        buffer = io.BytesIO(json_data.encode('utf-8'))
        s3.upload_fileobj(
            buffer,
            ARCHIVE_BUCKET,
            archive_key,
            ExtraArgs={'ContentType': 'application/json'}
        )
        
        # Mark as processed for idempotency
        try:
            table.put_item(
                Item={
                    'executionId': f"_processed:{execution_id}",
                    'timestamp': sequence_number,
                    'ttl': int((datetime.now(timezone.utc).timestamp() + 86400))  # 1 day
                }
            )
        except Exception as e:
            logger.warning(f"Failed to mark processed: {e}")
        
        logger.info(f"Archived execution {execution_id} to {archive_key}")
        
        # Update DynamoDB with reconstruction metadata
        table.update_item(
            Key={
                'executionId': execution_id,
                'timestamp': new_image.get('timestamp', {}).get('S', datetime.now(timezone.utc).isoformat())
            },
            UpdateExpression='SET reconstruction_status = :status, archive_location = :location',
            ExpressionAttributeValues={
                ':status': 'RECONSTRUCTED',
                ':location': f"s3://{ARCHIVE_BUCKET}/{archive_key}"
            }
        )
    
    return {'statusCode': 200, 'processed_records': len(event.get('Records', []))}

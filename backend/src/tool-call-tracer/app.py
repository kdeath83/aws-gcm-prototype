"""
GCM Principle 2: Tool-Call Graph Monitor
Traces tool invocation graphs and detects expansion without progress.
"""

import json
import os
import boto3
from datetime import datetime, timezone
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACES_TABLE'])

class ToolCallGraphAnalyzer:
    """Analyzes tool-call graph expansion patterns."""
    
    def __init__(self):
        self.graph_nodes = []
        self.graph_edges = []
        self.depth = 0
        self.cycles = []
        self.dead_ends = []
    
    def build_graph(self, tool_invocations):
        """Build adjacency list representation of tool-call graph."""
        for i, invocation in enumerate(tool_invocations):
            node = {
                'id': i,
                'tool': invocation.get('tool_name', 'unknown'),
                'timestamp': invocation.get('timestamp'),
                'result': invocation.get('result_status', 'unknown'),
                'state_change': invocation.get('state_change', False)
            }
            self.graph_nodes.append(node)
            
            # Edge to previous if sequential
            if i > 0:
                self.graph_edges.append({
                    'from': i - 1,
                    'to': i,
                    'type': 'sequential'
                })
            
            # Check for recursive calls
            for j, prev_node in enumerate(self.graph_nodes[:-1]):
                if prev_node['tool'] == node['tool']:
                    self.graph_edges.append({
                        'from': j,
                        'to': i,
                        'type': 'recursive'
                    })
    
    def detect_cycles_dfs(self):
        """Fix 6: Use DFS for proper cycle detection in directed graph."""
        # Build adjacency list
        adj = {node['id']: [] for node in self.graph_nodes}
        for edge in self.graph_edges:
            if edge['from'] in adj:
                adj[edge['from']].append(edge['to'])
        
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    cycle = dfs(neighbor, path + [neighbor])
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]
            
            rec_stack.remove(node)
            return None
        
        for node in self.graph_nodes:
            if node['id'] not in visited:
                cycle = dfs(node['id'], [node['id']])
                if cycle:
                    self.cycles.append({
                        'nodes': cycle,
                        'length': len(cycle) - 1,
                        'severity': 'critical' if len(cycle) <= 3 else 'high'
                    })
    
    def detect_expansion_without_progress(self):
        """Detect when tool graph expands without meaningful state changes."""
        no_change_streak = 0
        
        for i, node in enumerate(self.graph_nodes):
            if not node.get('state_change', False):
                no_change_streak += 1
                
                if no_change_streak >= 5:
                    self.dead_ends.append({
                        'start_index': i - no_change_streak + 1,
                        'end_index': i,
                        'tool_chain': [n['tool'] for n in self.graph_nodes[i-no_change_streak+1:i+1]],
                        'severity': 'high'
                    })
                    no_change_streak = 0
            else:
                no_change_streak = 0
    
    def calculate_depth(self):
        """Calculate maximum graph depth."""
        self.depth = len(self.graph_nodes)
        return self.depth
    
    def analyze(self, tool_invocations):
        """Run all graph analyses."""
        if not tool_invocations:
            return {
                'graph_depth': 0,
                'nodes_count': 0,
                'edges_count': 0,
                'cycles_detected': [],
                'dead_ends': [],
                'expansion_without_progress': False,
                'status': 'NO_TOOLS'
            }
        
        self.build_graph(tool_invocations)
        self.detect_cycles()
        self.detect_expansion_without_progress()
        self.calculate_depth()
        
        has_expansion_without_progress = len(self.dead_ends) > 0
        
        return {
            'graph_depth': self.depth,
            'nodes_count': len(self.graph_nodes),
            'edges_count': len(self.graph_edges),
            'cycles_detected': self.cycles,
            'cycles_count': len(self.cycles),
            'dead_ends': self.dead_ends,
            'dead_ends_count': len(self.dead_ends),
            'expansion_without_progress': has_expansion_without_progress,
            'graph_data': {
                'nodes': self.graph_nodes,
                'edges': self.graph_edges
            },
            'status': 'CRITICAL' if self.cycles or has_expansion_without_progress else 'HEALTHY' if self.depth <= 10 else 'DEGRADED'
        }

def handler(event, context):
    """Lambda handler for tool-call tracing."""
    
    detail = event.get('detail', {})
    execution_id = detail.get('executionId', 'unknown')
    tool_invocations = detail.get('tool_invocations', [])
    
    # Analyze tool-call graph
    analyzer = ToolCallGraphAnalyzer()
    graph_result = analyzer.analyze(tool_invocations)
    
    # Store in DynamoDB
    trace_item = {
        'executionId': execution_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'ttl': int((datetime.now(timezone.utc).timestamp() + 2592000)),
        'principle': 'TOOL_CALL_GRAPH',
        'graph_depth': graph_result['graph_depth'],
        'nodes_count': graph_result['nodes_count'],
        'cycles_count': graph_result['cycles_count'],
        'dead_ends_count': graph_result['dead_ends_count'],
        'expansion_without_progress': graph_result['expansion_without_progress'],
        'status': graph_result['status'],
        'graph_data': graph_result.get('graph_data', {}),
        'cycles_detected': graph_result['cycles_detected'],
        'dead_ends': graph_result['dead_ends']
    }
    
    table.put_item(Item=trace_item)
    
    return {
        'statusCode': 200,
        'executionId': execution_id,
        'graph_depth': graph_result['graph_depth'],
        'cycles_count': graph_result['cycles_count'],
        'status': graph_result['status']
    }
